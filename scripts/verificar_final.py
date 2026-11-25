"""Compara o pacote final com o revisado e com o original.

Uso:
    cd scripts
    python verificar_final.py

Executado antes de arquivar os pacotes antigos.
"""

import json
import os
import sqlite3
import zipfile
from collections import Counter
from pathlib import Path

from revisao import ETAPAS, validar_ordem

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / ".archive" / "07-Cloud-Engineer.apkg"
REVISADO = ROOT / ".archive" / "07-Cloud-Engineer-Revisado.apkg"
FINAL = ROOT / "07-Cloud-Engineer-Final.apkg"
MAPA = ROOT / "MAPEAMENTO.md"

MELHORIAS = (
    # DNS
    "TTL é definido por registro",
    "cache negativo",
    # Systems Manager
    "SSM Agent precisa estar instalado",
    "conectividade de saída",
    # Terraform State
    "versionamento para recuperação",
    " locking ",
    # Kubernetes Secrets
    "RBAC controla o recurso, não chaves individuais",
    "encryption at rest protege o etcd",
    # IAM OIDC
    "aud, normalmente sts.amazonaws.com",
    "assunto (sub",
    # WAF
    "AWS Managed Rules",
    "rate-based rules",
    "associada a um ALB",
    # EKS
    "control plane (API server, etcd e scheduler)",
    "data plane são os nodes",
    # consistência interna
    "assume uma role AWS por OIDC",
)


def abrir(caminho):
    dados = zipfile.ZipFile(caminho).read("collection.anki2")
    con = sqlite3.connect(":memory:")
    con.deserialize(dados)
    decks = json.loads(con.execute("select decks from col").fetchone()[0])
    notas = {g: tuple(f.split("\x1f")) for g, f in con.execute("select guid,flds from notes")}
    cartoes = con.execute("select count(*) from cards").fetchone()[0]
    con.close()
    return decks, notas, cartoes


def frentes_duplicadas(notas):
    contador = Counter(n[0] for n in notas.values())
    return {frente: n for frente, n in contador.items() if n > 1}


def main():
    validar_ordem()
    d_orig, n_orig, c_orig = abrir(ORIGINAL)
    d_rev, n_rev, c_rev = abrir(REVISADO)
    d_fin, n_fin, c_fin = abrir(FINAL)

    assert (len(n_orig), c_orig) == (688, 688)
    assert (len(n_rev), c_rev) == (700, 700)
    assert (len(n_fin), c_fin) == (700, 700)
    assert len(d_fin) - 1 == 94

    # A estrutura e os GUIDs não podem mudar entre revisado e final.
    assert set(n_orig).issubset(set(n_fin)), "GUIDs originais perdidos no final"
    assert set(n_rev) == set(n_fin), "GUIDs divergentes entre revisado e final"
    nomes_rev = sorted(v["name"] for k, v in d_rev.items() if v["name"] != "Default")
    nomes_fin = sorted(v["name"] for k, v in d_fin.items() if v["name"] != "Default")
    assert nomes_rev == nomes_fin, "A estrutura de decks mudou"

    # A ordem das etapas continua a mesma.
    prefixos = [etapa for etapa, _ in ETAPAS] + ["11-Certificações"]
    vistos = []
    for nome in nomes_fin:
        parte = nome.split("::")[1]
        if parte.startswith("11-Certificações"):
            if not vistos or vistos[-1] != "11-Certificações":
                vistos.append("11-Certificações")
        elif parte not in vistos:
            vistos.append(parte)
    assert vistos == prefixos, "Ordem das etapas alterada: %s" % vistos

    # Repetições e contradições removidas.
    dup_rev = frentes_duplicadas(n_rev)
    dup_fin = frentes_duplicadas(n_fin)
    assert len(dup_rev) == 3, "Esperadas 3 frentes duplicadas no revisado"
    assert not dup_fin, "Ainda há frentes duplicadas no final: %s" % dup_fin

    texto_rev = "\x1f".join("\x1f".join(n) for n in n_rev.values())
    texto_fin = "\x1f".join("\x1f".join(n) for n in n_fin.values())
    assert "secrets.AWS_ACCESS_KEY_ID usado no step de deploy" in texto_rev
    assert "secrets.AWS_ACCESS_KEY_ID usado no step de deploy" not in texto_fin

    # Melhorias presentes no final.
    ausentes = [trecho for trecho in MELHORIAS if trecho not in texto_fin]
    assert not ausentes, "Melhorias ausentes: %s" % ausentes

    # Nenhum campo vazio.
    assert all(all(campo.strip() for campo in nota) for nota in n_fin.values())

    mapa = MAPA.read_text(encoding="utf-8")
    assert "07-Cloud-Engineer-Final.apkg" in mapa

    alterados = [g for g in n_rev if n_rev[g] != n_fin[g]]
    print("OK: final com 94 decks, 700 cards e GUIDs idênticos ao revisado.")
    print("Frentes duplicadas: revisado=%d, final=%d" % (len(dup_rev), len(dup_fin)))
    print("Contradição GitHub Actions removida.")
    print("Cartões reforçados em relação ao revisado: %d" % len(alterados))
    print("Estrutura de etapas e documentação preservadas.")


if __name__ == "__main__":
    main()
