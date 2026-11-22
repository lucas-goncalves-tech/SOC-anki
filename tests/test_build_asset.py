import json, sqlite3, tempfile, unittest, zipfile
from pathlib import Path
from base import ROOT
from cards import CARDS
from gerar_notebooks import gerar, montar_decks, validar
from notebook import titulos_notebooks

class BuildAssetContract(unittest.TestCase):
    def test_molde_existe_e_valido(self):
        molde = ROOT / "assets" / "note-type.apkg"
        self.assertTrue(molde.exists())
        with zipfile.ZipFile(molde) as z:
            dados = z.read("collection.anki2")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.anki2"
            p.write_bytes(dados)
            con = sqlite3.connect(p)
            modelos = json.loads(con.execute("select models from col").fetchone()[0])
            self.assertEqual([f["name"] for f in next(iter(modelos.values()))["flds"]],
                             ["Frente", "Verso1", "Verso2"])
            con.close()

    def test_gerador_aponta_novos_caminhos(self):
        texto = (ROOT / "scripts" / "gerar_notebooks.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / "assets" / "note-type.apkg"', texto)
        self.assertIn('OUTPUT = ROOT / "AppSec.apkg"', texto)
        self.assertNotIn('ROOT / "foco"', texto)

    def test_mapa_usa_caminho_da_raiz(self):
        texto = (ROOT / "MAPEAMENTO.md").read_text(encoding="utf-8")
        self.assertIn("`AppSec.apkg`", texto)
        self.assertNotIn("foco/AppSec.apkg", texto)

    def test_gerar_apos_molde(self):
        titulos = titulos_notebooks(ROOT / "gemini-notebook.md")
        decks = montar_decks(titulos, CARDS)
        total = validar(titulos, CARDS)
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "AppSec.apkg"
            gerar(decks, total, saida=saida)
            with zipfile.ZipFile(saida) as z:
                self.assertIn("collection.anki2", z.namelist())
