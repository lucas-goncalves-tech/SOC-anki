"""Gera SOC-N1-N2.apkg na raiz — pacote separado, sem tocar nos outros apkgs.

Reaproveita o tipo de nota "Cloud Engineer" (campos Frente, Verso1, Verso2) do
arquivo-base usado por gerar_notebooks.py, mantendo o CSS laranja e o modo
noturno. Deck raiz ``SOC``, com um deck por etapa no mesmo padrão do pacote 07:
``SOC::00-Rotina e Triagem N1``, ``SOC::01-Fundamentos SOC``, ...

Faixas reservadas deste pacote (documentadas para não colidir com 07/08/09):

* notas: 1770000000000 em diante, passo 10 (07 usa 1700…, 08 usa 1750…,
  09 usa 1760…);
* decks: 2400000001 em diante (07 usa 2100000000+número, 08 e 09 usam
  2300000091–98).

O GUID é calculado com ``nome_antigo`` + índice, como no pacote 07. O gerador
grava o nome visível em ``nome_antigo``, então renomear o deck ou reordenar
cards dentro dele gera GUIDs novos — exija import limpo nesse caso.
"""

import hashlib
import json
import os
import sqlite3
import time
import zipfile

from cards_soc import iter_decks
from gerar_notebooks import ROOT, ler_modelo, slug

OUTPUT = ROOT / "SOC-N1-N2.apkg"
BASE_ID = 1770000000000
BASE_DECK_ID = 2400000000
NIVEIS = ("n1", "n2")


def montar_deck(numero, titulo, nivel, secoes):
    # Os títulos já trazem o prefixo numérico (01-, 02-, ...), como no pacote 07.
    nome = "SOC::%s" % titulo
    return {
        "id": BASE_DECK_ID + numero,
        "nome": nome,
        "nome_antigo": nome,
        "nivel": nivel,
        "numero": numero,
        "secoes": secoes,
    }


def gerar(decks):
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
    for deck in decks:
        meta = dict(deck_base)
        meta.update({"id": deck["id"], "name": deck["nome"], "usn": -1, "mod": now})
        novos_decks[str(deck["id"])] = meta
        indice_deck = 0
        for secao_idx, (secao_titulo, cartoes) in enumerate(deck["secoes"], start=1):
            tag = "soc n%s etapa%02d secao%02d_%s nb%02d_%s" % (
                deck["nivel"], deck["numero"], secao_idx,
                slug(secao_titulo or "visao-geral"), deck["numero"],
                slug(deck["nome"].split("-", 1)[1]),
            )
            for frente, verso1, verso2 in cartoes:
                indice_deck += 1
                nota_id = BASE_ID + posicao * 10
                # O índice percorre o deck inteiro, não reinicia a cada seção:
                # é o que mantém os GUIDs únicos dentro do deck.
                guid = hashlib.md5(
                    ("%s-%02d" % (deck["nome_antigo"], indice_deck)).encode()
                ).hexdigest()[:12]
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
                    (nota_id + 1, nota_id, deck["id"], 0, now, -1, 0, 0, posicao,
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
    vistos = {}
    total = 0
    for numero, titulo, nivel, secoes in iter_decks():
        if nivel not in NIVEIS:
            raise SystemExit("Nível inesperado no deck %02d: %r" % (numero, nivel))
        if not titulo.strip() or not secoes:
            raise SystemExit("Deck %02d sem título ou sem seções" % numero)
        for nome_secao, cartoes in secoes:
            if not cartoes:
                raise SystemExit("Seção vazia no deck %02d: %r" % (numero, nome_secao))
            for cartao in cartoes:
                if len(cartao) != 3 or not all(isinstance(c, str) and c.strip() for c in cartao):
                    raise SystemExit("Card inválido no deck %02d: %r" % (numero, cartao))
                if "\x1f" in "".join(cartao):
                    raise SystemExit("Card com separador de campo no deck %02d" % numero)
                if cartao[2].strip().endswith("?"):
                    raise SystemExit("Verso2 não pode ser pergunta no deck %02d: %r" % (
                        numero, cartao[0]))
                frente = cartao[0].strip()
                if frente in vistos:
                    raise SystemExit("Frente duplicada: %r (decks %02d e %02d)" % (
                        frente, vistos[frente], numero))
                vistos[frente] = numero
                total += 1
    return total


def main():
    total = validar()
    decks = [montar_deck(*dados) for dados in iter_decks()]
    gerados = gerar(decks)
    if gerados != total:
        raise SystemExit("Contagem divergente: %d != %d" % (gerados, total))
    for nivel in NIVEIS:
        cartoes = sum(
            len(cartoes)
            for _, _, lvl, secoes in iter_decks() if lvl == nivel
            for _, cartoes in secoes
        )
        print("%s: %d cards" % (nivel.upper(), cartoes))
    print("OK: %d decks, %d cards" % (len(decks), total))
    print("Apkg:", OUTPUT)


if __name__ == "__main__":
    main()
