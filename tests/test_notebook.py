import unittest
from base import ROOT
from notebook import titulos_notebooks


class NotebookContract(unittest.TestCase):
    def setUp(self):
        self.titulos = titulos_notebooks(ROOT / "gemini-notebook.md")

    def test_38_notebooks_numerados(self):
        self.assertEqual(sorted(self.titulos), list(range(1, 39)))

    def test_cinco_fases(self):
        texto = (ROOT / "gemini-notebook.md").read_text(encoding="utf-8")
        self.assertEqual(texto.count("\n# Fase "), 5)

    def test_titulos_das_pontas(self):
        self.assertEqual(self.titulos[1], "Web Application Security Fundamentals")
        self.assertEqual(
            self.titulos[38],
            "Application Incident Response and Developer Enablement",
        )
