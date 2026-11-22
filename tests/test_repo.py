import unittest
from base import ROOT


class RepoContract(unittest.TestCase):
    def test_arquivos_antigos_removidos(self):
        self.assertFalse((ROOT / "scripts" / "cards_cert.py").exists())
        self.assertFalse((ROOT / "scripts" / "cards_vagas.py").exists())
        self.assertTrue((ROOT / ".archive" / "cloud" / "07-Notebooks-Cloud.apkg").exists())
        self.assertFalse((ROOT / "foco" / "07-Notebooks.apkg").exists())

    def test_sem_referencias_a_certificacao(self):
        for nome in ("README.md", "MAPEAMENTO.md", "gemini-notebook.md"):
            texto = (ROOT / nome).read_text(encoding="utf-8")
            self.assertNotIn("CLF-C02", texto, nome)
            self.assertNotIn("SAA-C03", texto, nome)

    def test_readme_appsec(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        for trecho in (
            "AppSec", "AppSec.apkg", "38 decks", "190 cards",
            "AppSec::38-", "MAPEAMENTO.md", "python scripts/gerar_notebooks.py",
            "<pre class=\"codeblock\"><code>",
        ):
            self.assertIn(trecho, texto, trecho)
