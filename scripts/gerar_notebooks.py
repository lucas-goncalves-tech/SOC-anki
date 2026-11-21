"""Gera foco/07-Notebooks.apkg e MAPEAMENTO.md.

O tipo de nota é copiado de cloud-eng/foco-01-CLF-C02.apkg: mesmo ID
(1830472615), mesmos campos (Frente, Verso1, Verso2), mesmo CSS e mesmos
templates. O arquivo único contém:

- decks 01-70: um por notebook de gemini-notebook.md
- decks 71-80: extras aproveitados dos decks antigos de foco/
- decks 81-86: habilidades pedidas em vagas de Cloud Engineer
- decks CLF-C02 e SAA-C03: certificações (originais + cards de alto impacto)
"""

import hashlib
import json
import os
import re
import sqlite3
import tempfile
import time
import zipfile
from pathlib import Path

from cards_fase0 import CARDS as FASE0
from cards_fase1 import CARDS as FASE1
from cards_fase2 import CARDS as FASE2
from cards_cert import ADICOES as ADICOES_CERT
from cards_vagas import DECKS as DECKS_VAGAS

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "gemini-notebook.md"
TEMPLATE = ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg"
CERT_SOURCES = (
    ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg",
    ROOT / "cloud-eng" / "foco-02-SAA-C03.apkg",
)
OUTPUT = ROOT / "foco" / "07-Notebooks.apkg"
MAPA = ROOT / "MAPEAMENTO.md"

CARDS = {**FASE0, **FASE1, **FASE2}

EXTRAS_TITULOS = {
    71: "Azure",
    72: "Padrões de Resiliência",
    73: "SLO, SLI e Error Budget",
    74: "Consistência e Dados",
    75: "Segurança Avançada",
    76: "FinOps",
    77: "Serviços AWS Complementares",
    78: "Cenários de Entrevista",
    79: "Redes Complementar",
    80: "Fundamentos Complementares",
}

FONTES_EXTRA = (
    "cloud-eng/foco-03-Redes.apkg",
    "cloud-eng/foco-04-Entrevistas.apkg",
    "cloud-eng/foco-05-Cloud-Neutro.apkg",
    "cloud-eng/foco-06-Lacunas.apkg",
)

FORA_DA_PROVA = {71, 77, 78, 79, 80}

# Correção encontrada na auditoria: o deck antigo dizia "6 Rs".
OVERRIDES_EXTRA = {
    "Quais são os 6 Rs de migração para cloud?": (
        "Quais são os 7 Rs de migração para cloud?",
        "As sete estratégias são Rehost, Replatform, Repurchase, Refactor, Retire, Retain e Relocate.",
        "Relocate é mover para outra região ou infraestrutura sem mudar a aplicação, por exemplo sa-east-1 para us-east-1."),
}

# Card duplicado entre CLF-C02::Servicos e o notebook 31.
CARD_DUPLICADO = "AWS Site-to-Site VPN"


def titulos_notebooks():
    texto = NOTEBOOK.read_text(encoding="utf-8")
    itens = re.findall(r"^### Notebook (\d+) — (.+)$", texto, re.M)
    return {int(numero): titulo.strip() for numero, titulo in itens}


def slug(titulo):
    return re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")


def grupo_extra(frente):
    f = frente.lower()
    if any(k in f for k in (
        "azure", "az-900", "entra id", "app service", "aks", "bicep",
        "virtual machine scale sets", "cosmos db", "key vault",
    )):
        return 71
    if any(k in f for k in ("circuit breaker", "backoff", "idempotent", "timeout", "bulkhead", "degradação graciosa")):
        return 72
    if any(k in f for k in ("sli", "slo", "error budget")):
        return 73
    if any(k in f for k in ("teorema cap", "consistência", "sql e nosql", "leader/follower")):
        return 74
    if any(k in f for k in ("zero trust", "stride", "envelope encryption")):
        return 75
    if any(k in f for k in ("unit economics", "showback", "chargeback", "anomalia de custo")):
        return 76
    if f.startswith("cenário:"):
        return 78
    if any(k in f for k in ("nginx", "dnsmasq")):
        return 79
    if any(k in f for k in ("sla", "vendor lock-in")):
        return 80
    if any(k in f for k in (
        "6 rs", "landing zone", "crr", "x-ray", "boto3", "step functions",
        "session manager", "parameter store", "elastic beanstalk", "cdk",
        "cognito", "elastic ip", "api gateway", "elasticache",
        "transit gateway", "site-to-site", "ebs, efs", "aurora",
    )):
        return 77
    return None


def carregar_extras():
    extras = {numero: [] for numero in EXTRAS_TITULOS}
    for nome in FONTES_EXTRA:
        with zipfile.ZipFile(ROOT / nome) as arquivo:
            dados = arquivo.read("collection.anki2")
        fd, tmp = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        with open(tmp, "wb") as arquivo:
            arquivo.write(dados)
        con = sqlite3.connect(tmp)
        for (flds,) in con.execute("select flds from notes order by id"):
            campos = tuple(flds.split("\x1f"))
            if len(campos) != 3:
                raise SystemExit("Card com campos inesperados em %s" % nome)
            grupo = grupo_extra(campos[0])
            if grupo is not None:
                extras[grupo].append(OVERRIDES_EXTRA.get(campos[0], campos))
        con.close()
        os.remove(tmp)
    vazios = [numero for numero, cartoes in extras.items() if not cartoes]
    if vazios:
        raise SystemExit("Grupos de extras vazios: %s" % vazios)
    return extras


def carregar_certificacao():
    decks = {}
    for caminho in CERT_SOURCES:
        with zipfile.ZipFile(caminho) as arquivo:
            dados = arquivo.read("collection.anki2")
        fd, tmp = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        with open(tmp, "wb") as arquivo:
            arquivo.write(dados)
        con = sqlite3.connect(tmp)
        nomes = json.loads(con.execute("select decks from col").fetchone()[0])
        for did, flds in con.execute(
            "select c.did, n.flds from cards c join notes n on c.nid=n.id"
        ):
            nome = nomes[str(did)]["name"]
            campos = tuple(flds.split("\x1f"))
            if len(campos) != 3:
                raise SystemExit("Card com campos inesperados em %s" % caminho)
            if campos[0] == CARD_DUPLICADO:
                continue
            decks.setdefault(nome, []).append(campos)
        con.close()
        os.remove(tmp)
    for nome, cartoes in ADICOES_CERT.items():
        decks.setdefault(nome, []).extend(cartoes)
    return decks


def validar(titulos):
    if set(titulos) != set(CARDS):
        raise SystemExit(
            "Notebooks sem cards ou cards sem notebook: %s / %s"
            % (sorted(set(titulos) - set(CARDS)), sorted(set(CARDS) - set(titulos)))
        )
    total = 0
    for numero, cartoes in sorted(CARDS.items()):
        if not cartoes:
            raise SystemExit("Notebook %02d sem cards" % numero)
        for cartao in cartoes:
            if len(cartao) != 3 or not all(isinstance(c, str) and c.strip() for c in cartao):
                raise SystemExit("Card inválido no notebook %02d: %r" % (numero, cartao))
            if "\x1f" in "".join(cartao):
                raise SystemExit("Card com separador de campo no notebook %02d" % numero)
        total += len(cartoes)
    return total


def ler_modelo():
    with zipfile.ZipFile(TEMPLATE) as arquivo:
        colecao = arquivo.read("collection.anki2")
        outros = {
            nome: arquivo.read(nome)
            for nome in arquivo.namelist()
            if nome != "collection.anki2"
        }
    fd, caminho = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    with open(caminho, "wb") as arquivo:
        arquivo.write(colecao)
    return caminho, outros


def gerar(decks, total):
    caminho, outros = ler_modelo()
    con = sqlite3.connect(caminho)
    conf, models, decks_json, dconf, tags = con.execute(
        "select conf, models, decks, dconf, tags from col"
    ).fetchone()

    modelo = next(iter(json.loads(models).values()))
    if modelo["name"] != "Cloud Engineer" or [f["name"] for f in modelo["flds"]] != [
        "Frente", "Verso1", "Verso2"
    ]:
        raise SystemExit("O modelo do arquivo-base não é o esperado")

    deck_base = next(v for k, v in json.loads(decks_json).items() if k != "1")
    now = int(time.time())
    novos_decks = {"1": json.loads(decks_json)["1"]}

    con.execute("delete from notes")
    con.execute("delete from cards")
    con.execute("delete from revlog")
    con.execute("delete from graves")

    base_id = 1700000000000
    posicao = 0
    for deck_id, nome, tag_extra, cartoes in decks:
        deck = dict(deck_base)
        deck.update({"id": deck_id, "name": nome, "usn": -1, "mod": now})
        novos_decks[str(deck_id)] = deck
        tag = "cloud-engineer %s" % tag_extra
        for indice, (frente, verso1, verso2) in enumerate(cartoes, start=1):
            nota_id = base_id + posicao * 10
            guid = hashlib.md5(("%s-%02d" % (nome, indice)).encode()).hexdigest()[:12]
            con.execute(
                "insert into notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) "
                "values (?,?,?,?,?,?,?,?,?,?,?)",
                (nota_id, guid, modelo["id"], now, -1, " %s " % tag,
                 "\x1f".join((frente, verso1, verso2)), frente, 0, 0, ""),
            )
            con.execute(
                "insert into cards (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, "
                "reps, lapses, left, odue, odid, flags, data) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (nota_id + 1, nota_id, deck_id, 0, now, -1, 0, 0, posicao,
                 0, 0, 0, 0, 0, 0, 0, 0, ""),
            )
            posicao += 1

    con.execute(
        "update col set mod=?, scm=?, ls=?, conf=?, models=?, decks=?, dconf=?, tags=?",
        (now, now, now, conf, json.dumps({str(modelo["id"]): modelo}, ensure_ascii=False),
         json.dumps(novos_decks, ensure_ascii=False), dconf, tags),
    )
    con.commit()
    con.close()

    with open(caminho, "rb") as arquivo:
        colecao_nova = arquivo.read()
    os.remove(caminho)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as arquivo:
        arquivo.writestr("collection.anki2", colecao_nova)
        for nome, dados in outros.items():
            arquivo.writestr(nome, dados)
    return total


def escrever_mapa(titulos, decks):
    por_id = {d[0]: d for d in decks}
    linhas = [
        "# MAPEAMENTO — cards por notebook",
        "",
        "Arquivo único: `foco/07-Notebooks.apkg`. Todos os cards usam o mesmo tipo de nota do `foco/`",
        "(modelo `Cloud Engineer`, campos `Frente`, `Verso1` = O QUE É e `Verso2` = EXEMPLO DE USO).",
        "",
        "**Como usar:** estude o Notebook `XX` e revise o deck `Cloud Engineer::XX-...` no mesmo dia.",
        "",
        "| Grupo | Decks | Cards |",
        "|-------|-------|-------|",
        "|Notebooks 01–70 | 70 | %d |" % sum(len(por_id[2100000000+n][3]) for n in range(1, 71)),
        "|Extras 71–80 | 10 | %d |" % sum(len(por_id[2100000000+n][3]) for n in EXTRAS_TITULOS),
        "|Vagas 81–86 | 6 | %d |" % sum(len(por_id[2100000000+n][3]) for n in DECKS_VAGAS),
        "|CLF-C02 + SAA-C03 | 8 | %d |" % sum(len(c) for _, d, _, c in decks if "::CLF-C02::" in d or "::SAA-C03::" in d),
    ]
    total = sum(len(c) for _, _, _, c in decks)
    linhas += ["", "**Total: %d decks, %d cards.**" % (len(decks), total), "",
               "## Decks 01–70 — notebooks", "",
               "| Notebook | Deck | Cards |", "|----------|------|-------|"]
    for numero in sorted(titulos):
        linhas.append("| %02d — %s | `Cloud Engineer::%02d-%s` | %d |"
                      % (numero, titulos[numero], numero, titulos[numero], len(CARDS[numero])))
    linhas += ["", "## Decks 71–80 — extras", "",
               "Decks 71 e 77–80 são de entrevista/multicloud e estão fora do escopo das provas.",
               "", "| Deck | Cards |", "|------|-------|"]
    for numero in sorted(EXTRAS_TITULOS):
        linhas.append("| `Cloud Engineer::%02d-%s` | %d |"
                      % (numero, EXTRAS_TITULOS[numero], len(por_id[2100000000+numero][3])))
    linhas += ["", "## Decks 81–86 — habilidades de vagas", "",
               "| Deck | Cards |", "|------|-------|"]
    for numero in sorted(DECKS_VAGAS):
        linhas.append("| `Cloud Engineer::%02d-%s` | %d |"
                      % (numero, DECKS_VAGAS[numero][0], len(por_id[2100000000+numero][3])))
    linhas += ["", "## Decks de certificação", "",
               "Vêm depois do 80 na árvore do Anki. Incluem os cards originais e os acréscimos de alto impacto.",
               "", "| Deck | Cards |", "|------|-------|"]
    certs = sorted((d, c) for _, d, _, c in decks if "::CLF-C02::" in d or "::SAA-C03::" in d)
    for nome, cartoes in certs:
        linhas.append("| `%s` | %d |" % (nome, len(cartoes)))
    linhas += ["", "## Afinidade entre assuntos", "",
               "Git (06) com CI/CD (58–59); Dockerfile (53) com Compose (56); redes (16–23) com VPC (28–31);",
               "DNS (20) com Route 53 (40); IAM (26–27) com CloudTrail (62); Terraform (46–51) com Git (06);",
               "CloudWatch (60–61) com troubleshooting (63–64).", ""]
    MAPA.write_text("\n".join(linhas), encoding="utf-8")


def main():
    titulos = titulos_notebooks()
    validar(titulos)
    extras = carregar_extras()
    certificacao = carregar_certificacao()

    decks = []
    for numero in range(1, 71):
        decks.append((2100000000 + numero, "Cloud Engineer::%02d-%s" % (numero, titulos[numero]),
                      "nb%02d_%s" % (numero, slug(titulos[numero])), CARDS[numero]))
    for numero in EXTRAS_TITULOS:
        tag = "nb%02d_%s" % (numero, slug(EXTRAS_TITULOS[numero]))
        if numero in FORA_DA_PROVA:
            tag += " fora-da-prova"
        decks.append((2100000000 + numero, "Cloud Engineer::%02d-%s" % (numero, EXTRAS_TITULOS[numero]),
                      tag, extras[numero]))
    for numero, (titulo, cartoes) in DECKS_VAGAS.items():
        decks.append((2100000000 + numero, "Cloud Engineer::%02d-%s" % (numero, titulo),
                      "nb%02d_%s" % (numero, slug(titulo)), cartoes))
    for indice, nome in enumerate(sorted(certificacao), start=1):
        decks.append((2200000000 + indice, nome, "cert_" + slug(nome.split("::")[-1]),
                      certificacao[nome]))

    total = sum(len(cartoes) for _, _, _, cartoes in decks)
    gerar(decks, total)
    escrever_mapa(titulos, decks)
    print("OK: %d decks, %d cards" % (len(decks), total))
    print("Certificacao: %d decks, %d cards" %
          (sum(1 for _, d, *_ in decks if "::CLF-C02::" in d or "::SAA-C03::" in d),
           sum(len(c) for _, d, _, c in decks if "::CLF-C02::" in d or "::SAA-C03::" in d)))
    print("Apkg:", OUTPUT)
    print("Mapa:", MAPA)


if __name__ == "__main__":
    main()
