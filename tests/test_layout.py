import unittest, zipfile, sqlite3, tempfile, json
from pathlib import Path
from base import ROOT

class LayoutContract(unittest.TestCase):
    def test_raiz_appsec(self):
        for nome in ("AppSec.apkg", "README.md", "gemini-notebook.md",
                     "MAPEAMENTO.md", "assets/note-type.apkg"):
            self.assertTrue((ROOT / nome).exists(), nome)

    def test_arquivos_estao_arquivados(self):
        self.assertTrue((ROOT / ".archive/cloud/foco-01-CLF-C02.apkg").exists())
        self.assertTrue((ROOT / ".archive/cloud/07-Notebooks-Cloud.apkg").exists())
        self.assertTrue((ROOT / ".archive/aws/aws-cloud-practitioner-clf-c02.apkg").exists())
        self.assertGreater(len(list((ROOT / ".archive/cloud").glob("*.apkg"))), 20)

    def test_diretorios_antigos_fora(self):
        for nome in ("foco", "cloud-eng", "AWS"):
            self.assertFalse((ROOT / nome).exists(), nome)

    def test_sem_referencias_a_caminhos_antigos(self):
        arquivos = [ROOT / "README.md", ROOT / "MAPEAMENTO.md"]
        arquivos += sorted((ROOT / "scripts").glob("*.py"))
        for arquivo in arquivos:
            texto = arquivo.read_text(encoding="utf-8")
            self.assertNotIn("foco/AppSec.apkg", texto, str(arquivo))
            self.assertNotIn("foco/README.md", texto, str(arquivo))
            self.assertNotIn('ROOT / "foco"', texto, str(arquivo))

    def test_molde_igual_ao_arquivado(self):
        self.assertEqual((ROOT / "assets/note-type.apkg").read_bytes(),
                         (ROOT / ".archive/cloud/foco-01-CLF-C02.apkg").read_bytes())

    def test_pacote_tem_38_decks_e_190_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.anki2"
            p.write_bytes(zipfile.ZipFile(ROOT / "AppSec.apkg").read("collection.anki2"))
            con = sqlite3.connect(p)
            self.assertEqual(con.execute("select count(*) from notes").fetchone()[0], 190)
            decks = json.loads(con.execute("select decks from col").fetchone()[0])
            appsec = [k for k in decks if k != "1"]
            self.assertEqual(len(appsec), 38)
            self.assertTrue(all(k.startswith("23000000") for k in appsec))
            con.close()
