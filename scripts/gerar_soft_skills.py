"""Gera 08-Soft-Skills.apkg na raiz — deck separado, sem tocar no pacote principal.

Reaproveita o tipo de nota "Cloud Engineer" (campos Frente, Verso1, Verso2) do
mesmo arquivo-base usado por gerar_notebooks.py. IDs de nota começam em
1750000000000 para não colidirem com os do pacote principal (1700000000000).
"""

import hashlib
import json
import os
import sqlite3
import tempfile
import time
import zipfile

from gerar_notebooks import ROOT, ler_modelo, slug
from cards_soft_skills import DECKS

OUTPUT = ROOT / "08-Soft-Skills.apkg"
BASE_ID = 1750000000000


def gerar():
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

    posicao = 0
    for numero, (titulo, cartoes) in sorted(DECKS.items()):
        nome = "Soft Skills::%s" % titulo
        deck_id = 2300000000 + numero
        deck = dict(deck_base)
        deck.update({"id": deck_id, "name": nome, "usn": -1, "mod": now})
        novos_decks[str(deck_id)] = deck
        tag = "soft-skills nb%02d_%s" % (numero, slug(titulo))
        for indice, (frente, verso1, verso2) in enumerate(cartoes, start=1):
            nota_id = BASE_ID + posicao * 10
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
    return posicao


def validar():
    total = 0
    for numero, (titulo, cartoes) in sorted(DECKS.items()):
        if numero < 91:
            raise SystemExit("Deck %d fora da faixa reservada (91+)" % numero)
        if not titulo.strip() or not cartoes:
            raise SystemExit("Deck %d sem título ou sem cards" % numero)
        for cartao in cartoes:
            if len(cartao) != 3 or not all(isinstance(c, str) and c.strip() for c in cartao):
                raise SystemExit("Card inválido no deck %d: %r" % (numero, cartao))
            if "\x1f" in "".join(cartao):
                raise SystemExit("Card com separador de campo no deck %d" % numero)
        total += len(cartoes)
    return total


if __name__ == "__main__":
    total = validar()
    gerar()
    print("OK: %d decks, %d cards" % (len(DECKS), total))
    print("Apkg:", OUTPUT)
