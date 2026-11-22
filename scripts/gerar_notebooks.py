"""Gera foco/AppSec.apkg e MAPEAMENTO.md a partir do plano e dos cards.

O tipo de nota é copiado de cloud-eng/foco-01-CLF-C02.apkg (campos, CSS e
templates), mas renomeado para `AppSec` e com outro ID para não colidir com o
material de Cloud. Cada Notebook do plano vira um deck `AppSec::NN-Título`.
"""

import hashlib
import json
import re
import sqlite3
import tempfile
import zipfile
from pathlib import Path

from cards import CARDS
from notebook import titulos_notebooks

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "gemini-notebook.md"
TEMPLATE = ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg"
OUTPUT = ROOT / "foco" / "AppSec.apkg"
MAPA = ROOT / "MAPEAMENTO.md"

DECK_ID_BASE = 2300000000
MODELO_ID = 2300000000000
NOTA_ID_BASE = 2400000000000

FASE_RE = re.compile(r"^# Fase (\d+) — (.+)$|^### Notebook (\d+) —", re.M)


def validar(titulos, cards):
    """Exige de 4 a 6 cards por tema e devolve o total de cards."""
    if set(titulos) != set(cards):
        raise SystemExit(
            "Notebooks sem cards ou cards sem notebook: %s / %s"
            % (sorted(set(titulos) - set(cards)), sorted(set(cards) - set(titulos)))
        )
    total = 0
    for numero, cartoes in sorted(cards.items()):
        if not 4 <= len(cartoes) <= 6:
            raise SystemExit("Notebook %02d deve ter de 4 a 6 cards" % numero)
        for cartao in cartoes:
            if len(cartao) != 3 or not all(
                isinstance(campo, str) and campo.strip() for campo in cartao
            ):
                raise SystemExit("Card inválido no notebook %02d: %r" % (numero, cartao))
            if "\x1f" in "".join(cartao):
                raise SystemExit("Card com separador de campo no notebook %02d" % numero)
        total += len(cartoes)
    return total


def slug(titulo):
    return re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")


def montar_decks(titulos, cards):
    """Monta (id, nome, tag, cards) para cada um dos 38 temas."""
    return [
        (
            DECK_ID_BASE + numero,
            "AppSec::%02d-%s" % (numero, titulos[numero]),
            "appsec nb%02d_%s" % (numero, slug(titulos[numero])),
            cards[numero],
        )
        for numero in range(1, 39)
    ]


def gerar(decks, total, *, modelo=TEMPLATE, saida=OUTPUT):
    """Reescreve o `.apkg` base com os decks e cards AppSec."""
    with zipfile.ZipFile(modelo) as arquivo:
        colecao = arquivo.read("collection.anki2")
        outros = {
            nome: arquivo.read(nome)
            for nome in arquivo.namelist()
            if nome != "collection.anki2"
        }

    with tempfile.TemporaryDirectory() as tmp:
        caminho = Path(tmp) / "collection.anki2"
        caminho.write_bytes(colecao)
        con = sqlite3.connect(caminho)
        try:
            conf, models, decks_json, dconf, tags = con.execute(
                "select conf, models, decks, dconf, tags from col"
            ).fetchone()

            modelos = json.loads(models)
            tipo = next(iter(modelos.values()))
            if tipo["name"] != "Cloud Engineer" or [f["name"] for f in tipo["flds"]] != [
                "Frente", "Verso1", "Verso2"
            ]:
                raise SystemExit("O modelo do arquivo-base não é o esperado")
            id_antigo = tipo["id"]
            tipo["name"] = "AppSec"
            tipo["id"] = MODELO_ID
            modelos = {
                (str(MODELO_ID) if chave == str(id_antigo) else chave): valor
                for chave, valor in modelos.items()
            }

            decks_base = json.loads(decks_json)
            deck_base = next(v for k, v in decks_base.items() if k != "1")
            novos_decks = {"1": decks_base["1"]}
            now = int(con.execute("select strftime('%s', 'now')").fetchone()[0])

            con.execute("delete from notes")
            con.execute("delete from cards")
            con.execute("delete from revlog")
            con.execute("delete from graves")

            posicao = 0
            for deck_id, nome, tag, cartoes in decks:
                deck = dict(deck_base)
                deck.update({"id": deck_id, "name": nome, "usn": -1, "mod": now})
                novos_decks[str(deck_id)] = deck
                for indice, (frente, verso1, verso2) in enumerate(cartoes, start=1):
                    nota_id = NOTA_ID_BASE + posicao * 10
                    guid = hashlib.md5(
                        ("%s-%02d" % (nome, indice)).encode()
                    ).hexdigest()[:12]
                    con.execute(
                        "insert into notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) "
                        "values (?,?,?,?,?,?,?,?,?,?,?)",
                        (nota_id, guid, MODELO_ID, now, -1, " %s " % tag,
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
                (now, now, now, conf,
                 json.dumps(modelos, ensure_ascii=False),
                 json.dumps(novos_decks, ensure_ascii=False), dconf, tags),
            )
            con.commit()
        finally:
            con.close()
        colecao_nova = caminho.read_bytes()

    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as arquivo:
        arquivo.writestr("collection.anki2", colecao_nova)
        for nome, dados in outros.items():
            arquivo.writestr(nome, dados)


def fases_do_notebook():
    """Devolve (número, título, notebooks) para cada fase do plano."""
    fases = []
    for match in FASE_RE.finditer(NOTEBOOK.read_text(encoding="utf-8")):
        if match.group(1):
            fases.append((int(match.group(1)), match.group(2), []))
        else:
            fases[-1][2].append(int(match.group(3)))
    return fases


def escrever_mapa(titulos, decks, *, caminho=MAPA):
    """Escreve o pareamento estudo (Notebook) ↔ revisão (deck AppSec)."""
    por_id = {deck[0]: deck for deck in decks}
    total = sum(len(cartoes) for _, _, _, cartoes in decks)
    linhas = [
        "# MAPEAMENTO — decks AppSec",
        "",
        "Arquivo único: `foco/AppSec.apkg`. Tipo de nota `AppSec`, campos `Frente`, "
        "`Verso1` = O QUE É e `Verso2` = EXEMPLO DE USO.",
        "",
        "**Como usar:** estude o Notebook NN e revise o deck AppSec::NN no mesmo dia.",
        "",
        "**Total: %d decks, %d cards.**" % (len(decks), total),
        "",
    ]
    vistos = set()
    for numero_fase, titulo_fase, numeros in fases_do_notebook():
        linhas += [
            "## Fase %d — %s" % (numero_fase, titulo_fase),
            "",
            "| Notebook | Deck | Cards |",
            "|----------|------|-------|",
        ]
        for numero in numeros:
            if numero not in titulos:
                continue
            vistos.add(numero)
            linhas.append("| %02d — %s | `AppSec::%02d-%s` | %d |" % (
                numero, titulos[numero], numero, titulos[numero],
                len(por_id[DECK_ID_BASE + numero][3]),
            ))
        linhas.append("")

    if set(titulos) - vistos:
        raise SystemExit("Notebooks sem fase no plano: %s" % sorted(set(titulos) - vistos))
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main():
    titulos = titulos_notebooks(NOTEBOOK)
    total = validar(titulos, CARDS)
    decks = montar_decks(titulos, CARDS)
    gerar(decks, total)
    escrever_mapa(titulos, decks)
    print("OK: %d decks, %d cards" % (len(decks), total))
    print("Apkg:", OUTPUT)
    print("Mapa:", MAPA)


if __name__ == "__main__":
    main()
