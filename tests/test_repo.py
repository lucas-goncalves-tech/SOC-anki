import unittest
from base import ROOT

class RepoContract(unittest.TestCase):
    def test_arquivos_antigos_removidos(self):
        self.assertFalse((ROOT / "scripts" / "cards_cert.py").exists())
        self.assertFalse((ROOT / "scripts" / "cards_vagas.py").exists())
        self.assertTrue((ROOT / "cloud-eng" / "07-Notebooks-Cloud.apkg").exists())
        self.assertFalse((ROOT / "foco" / "07-Notebooks.apkg").exists())

    def test_sem_referencias_a_certificacao(self):
        for nome in ("foco/README.md", "MAPEAMENTO.md", "gemini-notebook.md"):
            texto = (ROOT / nome).read_text(encoding="utf-8")
            self.assertNotIn("CLF-C02", texto, nome)
            self.assertNotIn("SAA-C03", texto, nome)

    def test_readme_appsec(self):
        texto = (ROOT / "foco" / "README.md").read_text(encoding="utf-8")
        self.assertIn("AppSec", texto)
        self.assertIn("foco/AppSec.apkg", texto)
        self.assertIn("38", texto)
