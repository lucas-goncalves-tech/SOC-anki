"""Contrato do gerador AppSec: ids, tipo de nota, tags e mapeamento."""

import contextlib
import json
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from base import ROOT
from cards import CARDS
from gerar_notebooks import (
    fases_do_notebook, gerar, escrever_mapa, montar_decks, validar,
)
from notebook import titulos_notebooks

TITULOS = {i: "T%d" % i for i in range(1, 39)}
CARTOS = {
    i: [("pergunta %d-%d" % (i, j), "resposta", "exemplo") for j in range(1, 6)]
    for i in range(1, 39)
}
TOTAL = 190


class GeradorContract(unittest.TestCase):
    def test_montar_decks_namespace(self):
        decks = montar_decks(TITULOS, CARTOS)
        self.assertEqual(len(decks), 38)
        self.assertEqual(decks[0][0], 2300000001)
        self.assertEqual(decks[-1][0], 2300000038)
        self.assertTrue(decks[0][1].startswith("AppSec::01-"))
        self.assertIn("appsec nb01_", decks[0][2])
        self.assertFalse(any(str(d[0]).startswith("2100000000") for d in decks))

    def test_validar_rejeita_desbalanceamento(self):
        incompleto = {k: v for k, v in CARTOS.items() if k != 5}
        with self.assertRaises(SystemExit):
            validar(TITULOS, incompleto)
        self.assertEqual(validar(TITULOS, CARTOS), TOTAL)

    def test_validar_rejeita_faixa_de_cards(self):
        poucos = {k: (v[:3] if k == 1 else v) for k, v in CARTOS.items()}
        muitos = {k: (v + [("extra", "resposta", "exemplo")] * 2 if k == 1 else v)
                  for k, v in CARTOS.items()}
        with self.assertRaises(SystemExit):
            validar(TITULOS, poucos)
        with self.assertRaises(SystemExit):
            validar(TITULOS, muitos)

    def test_validar_aceita_dados_reais(self):
        titulos = titulos_notebooks(ROOT / "gemini-notebook.md")
        self.assertEqual(validar(titulos, CARDS), sum(len(c) for c in CARDS.values()))

    def test_validar_rejeita_card_que_nao_e_tupla(self):
        primeiro = list(CARTOS[1][0])
        cartoes = {**CARTOS, 1: [primeiro, *CARTOS[1][1:]]}
        with self.assertRaises(SystemExit):
            validar(TITULOS, cartoes)

    def test_fases_do_notebook(self):
        fases = fases_do_notebook()
        self.assertEqual([fase[0] for fase in fases], [0, 1, 2, 3, 4])
        self.assertEqual([len(fase[2]) for fase in fases], [6, 12, 6, 8, 6])

    def test_fases_do_notebook_sem_cabecalho_de_fase(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp) / "sem-fase.md"
            caminho.write_text("### Notebook 99 — Sem fase", encoding="utf-8")
            with patch("gerar_notebooks.NOTEBOOK", caminho):
                with self.assertRaisesRegex(SystemExit, "Notebook sem fase"):
                    fases_do_notebook()

    def test_modelo_e_campos(self):
        with self._abrir_apkg() as con:
            modelos = json.loads(con.execute("select models from col").fetchone()[0])
            modelo = next(iter(modelos.values()))
            self.assertEqual(modelo["name"], "AppSec")
            self.assertEqual(modelo["id"], 2300000000000)
            self.assertEqual([f["name"] for f in modelo["flds"]],
                             ["Frente", "Verso1", "Verso2"])
            self.assertIn("nightMode", modelo["css"])
            self.assertIn("pre.codeblock", modelo["css"])

    def test_gerar_sem_colisao_com_cloud(self):
        with self._abrir_apkg() as con:
            modelos = json.loads(con.execute("select models from col").fetchone()[0])
            self.assertNotEqual(next(iter(modelos.values()))["id"], 1830472615)
            nomes = json.loads(con.execute("select decks from col").fetchone()[0])
            ids = [int(k) for k in nomes if k != "1"]
            self.assertTrue(all(2300000001 <= i <= 2300000038 for i in ids))
            self.assertEqual(len(ids), 38)

    def test_notas_e_tags(self):
        with self._abrir_apkg() as con:
            notas = con.execute("select id, tags, flds from notes order by id").fetchall()
            self.assertEqual(len(notas), TOTAL)
            self.assertEqual(notas[0][0], 2400000000000)
            self.assertEqual(notas[0][1], " appsec nb01_t1 ")
            self.assertEqual(notas[-1][1], " appsec nb38_t38 ")
            for _, tags, _ in notas:
                self.assertTrue(tags.strip().startswith("appsec nb"))
                self.assertNotIn("fora-da-prova", tags)
            self.assertEqual(notas[0][2], "pergunta 1-1\x1fresposta\x1fexemplo")

    def test_gerar_exige_total_compatível(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AssertionError):
                gerar(montar_decks(TITULOS, CARTOS), TOTAL - 1,
                      saida=Path(tmp) / "AppSec.apkg")

    def test_gerar_idempotente(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            saida = tmp / "AppSec.apkg"
            decks = montar_decks(TITULOS, CARTOS)
            for _ in range(2):
                gerar(decks, TOTAL, saida=saida)
            with zipfile.ZipFile(saida) as z:
                dados = z.read("collection.anki2")
            bruto = tmp / "collection.anki2"
            bruto.write_bytes(dados)
            con = sqlite3.connect(bruto)
            self.assertEqual(con.execute("select count(*) from notes").fetchone()[0], TOTAL)
            con.close()

    def test_escrever_mapa(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp) / "MAPEAMENTO.md"
            escrever_mapa(TITULOS, montar_decks(TITULOS, CARTOS), caminho=caminho)
            texto = caminho.read_text(encoding="utf-8")
            self.assertIn("38 decks", texto)
            self.assertIn("190 cards", texto)
            self.assertIn("AppSec::01-", texto)
            self.assertIn("Fase 0 — Fundamentos", texto)
            self.assertIn("estude o Notebook NN e revise o deck AppSec::NN no mesmo dia", texto)
            self.assertNotIn("CLF-C02", texto)
            self.assertNotIn("SAA-C03", texto)

    def _abrir_apkg(self):
        @contextlib.contextmanager
        def aberto():
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                saida = tmp / "AppSec.apkg"
                gerar(montar_decks(TITULOS, CARTOS), TOTAL, saida=saida)
                with zipfile.ZipFile(saida) as z:
                    dados = z.read("collection.anki2")
                bruto = tmp / "collection.anki2"
                bruto.write_bytes(dados)
                con = sqlite3.connect(bruto)
                try:
                    yield con
                finally:
                    con.close()

        return aberto()
