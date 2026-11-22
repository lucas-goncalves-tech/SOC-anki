import unittest
from base import ROOT
from cards import CARDS

NOMES_2025 = (
    "Broken Access Control", "Security Misconfiguration",
    "Software Supply Chain Failures", "Cryptographic Failures",
    "Injection", "Insecure Design", "Authentication Failures",
    "Software or Data Integrity Failures",
    "Security Logging and Alerting Failures",
    "Mishandling of Exceptional Conditions",
)
LEGADOS = (
    "Sensitive Data Exposure", "Security Logging and Monitoring Failures",
    "Using Components with Known Vulnerabilities", "XML External Entities",
)

class CardContract(unittest.TestCase):
    def test_38_temas_numerados(self):
        self.assertEqual(sorted(CARDS), list(range(1, 39)))

    def test_formato_dos_cards(self):
        for numero, cartoes in CARDS.items():
            self.assertTrue(4 <= len(cartoes) <= 6, numero)
            for cartao in cartoes:
                self.assertEqual(len(cartao), 3, numero)
                self.assertTrue(all(isinstance(c, str) and c.strip() for c in cartao), numero)
                self.assertNotIn("\x1f", "".join(cartao), numero)

    def test_total_near_190(self):
        self.assertTrue(180 <= sum(len(c) for c in CARDS.values()) <= 200)

    def test_frentes_unicas(self):
        frentes = [f for cartoes in CARDS.values() for f, _, _ in cartoes]
        self.assertEqual(len(frentes), len(set(frentes)))

    def test_owasp_top10_2025_taxonomy(self):
        texto = " ".join(" ".join(c) for cartoes in CARDS.values() for c in cartoes)
        for nome in NOMES_2025:
            self.assertIn(nome, texto, nome)
        for legado in LEGADOS:
            self.assertNotIn(legado, texto, legado)
