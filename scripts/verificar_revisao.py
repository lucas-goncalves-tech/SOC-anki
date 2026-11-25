"""Verificação rápida do pacote revisado contra o original.

Uso:
    cd scripts
    python verificar_revisao.py
"""

import json
import os
import re
import sqlite3
import tempfile
import zipfile
from pathlib import Path

from revisao import ETAPAS, validar_ordem

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / ".archive" / "07-Cloud-Engineer.apkg"
REVISADO = ROOT / ".archive" / "07-Cloud-Engineer-Revisado.apkg"
MAPA = ROOT / "MAPEAMENTO.md"

CORRECOES = (
    "habilitador importante",
    "não necessariamente a propriedade do hardware",
    "não garante isso",
    "/31 tem 2 endereços",
    "resolução recursiva",
    "bridge definida pelo usuário",
    "valores sensíveis",
    "VPC Endpoints",
    "us-east-1, independentemente",
    "timeout máximo é de 15 minutos",
    "Multi-AZ DB cluster",
    "hibernada ou terminada",
    "base64, que não é criptografia",
    "IRSA",
    "IAM OIDC",
    "AWS KMS",
    "AWS Config",
    "AWS WAF",
    "AWS Systems Manager",
    "AWS Secrets Manager",
    "Nginx com TLS",
    "DHCP e ARP",
    "IPv6 operacional",
    "Troubleshooting avançado de Linux",
)


def abrir(caminho):
    with zipfile.ZipFile(caminho) as arquivo:
        if arquivo.testzip() is not None:
            raise SystemExit("ZIP corrompido: %s" % caminho)
        dados = arquivo.read("collection.anki2")
    fd, tmp = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    with open(tmp, "wb") as arquivo:
        arquivo.write(dados)
    con = sqlite3.connect(tmp)
    decks = json.loads(con.execute("select decks from col").fetchone()[0])
    notas = {}
    for guid, flds in con.execute("select guid, flds from notes"):
        notas[guid] = flds.split("\x1f")
    total_cartoes = con.execute("select count(*) from cards").fetchone()[0]
    con.close()
    os.remove(tmp)
    return decks, notas, total_cartoes


def main():
    validar_ordem()
    decks_antigos, notas_antigas, cartoes_antigos = abrir(ORIGINAL)
    decks_novos, notas_novas, cartoes_novos = abrir(REVISADO)

    assert len(notas_antigas) == 688
    assert cartoes_antigos == 688
    assert len(notas_novas) == 700
    assert cartoes_novos == 700
    assert set(notas_antigas).issubset(set(notas_novas)), "GUIDs originais perdidos"
    assert len(set(notas_novas)) == 700, "GUIDs duplicados"

    for guid, campos in notas_novas.items():
        assert len(campos) == 3, "Campos inesperados em %s" % guid
        assert all(c.strip() for c in campos), "Campo vazio em %s" % guid

    nomes = sorted(v["name"] for k, v in decks_novos.items() if v["name"] != "Default")
    assert len(nomes) == 94, "Esperados 94 decks folha, encontrados %d" % len(nomes)
    prefixos = [etapa for etapa, _ in ETAPAS] + ["11-Certificações"]
    vistos = []
    for nome in nomes:
        parte = nome.split("::")[1]
        if parte.startswith("11-Certificações"):
            if not vistos or vistos[-1] != "11-Certificações":
                vistos.append("11-Certificações")
        elif parte not in vistos:
            vistos.append(parte)
    assert vistos == prefixos, "Ordem de pastas incorreta: %s" % vistos

    texto = "\x1f".join("\x1f".join(c) for c in notas_novas.values())
    ausentes = [trecho for trecho in CORRECOES if trecho not in texto]
    assert not ausentes, "Correções/lacunas ausentes: %s" % ausentes

    mapa = MAPA.read_text(encoding="utf-8")
    assert "**700**" in mapa
    assert "07-Cloud-Engineer-Final.apkg" in mapa
    ordens_saa = {int(n) for n in re.findall(r"\| SAA-C03 \| (\d+) \|", mapa)}
    ordens_clf = {int(n) for n in re.findall(r"\| CLF-C02 \| (\d+) \|", mapa)}
    assert ordens_saa == {1, 2, 3, 4}, "Ordem SAA-C03 incorreta: %s" % ordens_saa
    assert ordens_clf == {1, 2, 3, 4}, "Ordem CLF-C02 incorreta: %s" % ordens_clf

    print("OK: 94 decks, 700 cards, 688 GUIDs preservados, 12 novos.")
    print("Ordem das etapas e correções verificadas.")


if __name__ == "__main__":
    main()
