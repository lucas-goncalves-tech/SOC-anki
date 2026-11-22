import re
import unittest
from base import ROOT
from cards import CARDS
from cards_fase0 import CARDS as FASE0
from cards_fase1 import CARDS as FASE1
from cards_fase2 import CARDS as FASE2
from cards_fase3 import CARDS as FASE3
from cards_fase4 import CARDS as FASE4

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

    def test_fases_por_modulo(self):
        modulos = (
            (FASE0, range(1, 7)),
            (FASE1, range(7, 19)),
            (FASE2, range(19, 25)),
            (FASE3, range(25, 33)),
            (FASE4, range(33, 39)),
        )
        for cartoes, numeros in modulos:
            self.assertEqual(sorted(cartoes), list(numeros))

    def test_campos_sem_markdown_nem_html_cru(self):
        """Campos do Anki são HTML: sem crases e sem tags não autorizadas."""
        permitidas = ("<code>", "</code>", '<pre class="codeblock">', "</pre>")
        tag_crua = re.compile(r"<[A-Za-z]")
        erros = []
        for numero, cartoes in sorted(CARDS.items()):
            for indice, cartao in enumerate(cartoes, 1):
                for campo, texto in zip(("Frente", "Verso1", "Verso2"), cartao):
                    local = "tema %02d card %d %s" % (numero, indice, campo)
                    if "`" in texto:
                        erros.append("%s: crase literal" % local)
                    resto = texto
                    for tag in permitidas:
                        resto = resto.replace(tag, "")
                    encontrada = tag_crua.search(resto)
                    if encontrada:
                        erros.append("%s: tag crua %r" % (local, encontrada.group(0)))
                    if texto.count("<code>") != texto.count("</code>"):
                        erros.append("%s: tags <code> desbalanceadas" % local)
                    if texto.count('<pre class="codeblock">') != texto.count("</pre>"):
                        erros.append("%s: tags <pre> desbalanceadas" % local)
        self.assertEqual(erros, [], "\n".join(erros))

    def test_codigo_renderizado_em_html(self):
        texto = " ".join(c for cartoes in CARDS.values()
                         for cartao in cartoes for c in cartao)
        self.assertIn("<code>", texto)
        self.assertIn('<pre class="codeblock"><code>', texto)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", texto)
        self.assertNotIn("<img", texto)

    def test_owasp_top10_2025_taxonomy(self):
        texto = " ".join(" ".join(c) for cartoes in CARDS.values() for c in cartoes)
        for nome in NOMES_2025:
            self.assertRegex(texto, r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(nome), nome)
        for legado in LEGADOS:
            self.assertNotIn(legado, texto, legado)
