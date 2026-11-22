# Pivot para AppSec Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir o plano de Cloud Engineer por um plano de AppSec com 38 temas e gerar um pacote Anki único (`foco/AppSec.apkg`) com um deck por tema, preservando o mecanismo de memorização já existente.

**Architecture:** Os cards vivem em cinco módulos Python por fase e são agregados por `scripts/cards.py`; os títulos dos temas vêm de `gemini-notebook.md` via `scripts/notebook.py`. O gerador `scripts/gerar_notebooks.py` valida o pareamento tema ↔ cards, copia o modelo de nota do `.apkg` base, renomeia o modelo para `AppSec`, aloca decks na faixa `2300000000+` e escreve o pacote e o `MAPEAMENTO.md`. Tudo é Python puro com `unittest` para testes.

**Tech Stack:** Python 3 (stdlib: `sqlite3`, `zipfile`, `hashlib`, `json`, `re`, `tempfile`), formato Anki `.apkg` (zip contendo `collection.anki2`), `unittest`.

**Spec:** `docs/superpowers/specs/2026-11-22-appsec-pivot-design.md`

## Global Constraints

- Gerador sem dependências externas: apenas `sqlite3`, `zipfile`, `hashlib`, `json`, `re`, `tempfile`, `pathlib`.
- Tipo de nota: nome `AppSec`, campos exatamente `Frente`, `Verso1`, `Verso2`, nessa ordem; manter CSS com modo noturno e blocos `<pre class="codeblock"><code>`.
- ID do modelo de nota deve ser diferente de `1830472615` (ID do tipo `Cloud Engineer`).
- Decks nomeados `AppSec::NN-Tema`, com IDs sequenciais a partir de `2300000000`.
- Tags no formato `appsec nnNN_slug`; sem tag `fora-da-prova`.
- 38 temas em 5 fases: Fase 0 = 01–06, Fase 1 = 07–18, Fase 2 = 19–24, Fase 3 = 25–32, Fase 4 = 33–38.
- 4 a 6 cards por tema; meta ~190 cards no total (faixa aceita: 180–200).
- Cada card é uma tupla `(frente, verso1, verso2)` com `verso1` = O QUE É e `verso2` = EXEMPLO DE USO.
- Termos técnicos em inglês, explicação em português. Codificação UTF-8 em todos os arquivos de texto.
- Saída: `foco/AppSec.apkg`. Pacote antigo vai para `cloud-eng/07-Notebooks-Cloud.apkg`.
- Comandos executados na raiz do repo; arquivos de teste em `tests/`.

## Review Focus

- **Taxonomia OWASP desatualizada (2021 em vez de 2025):** se o conteúdo usar as categorias antigas, o deck ensina errado. Teste `test_owasp_top10_2025_taxonomy` na Task 1 fixa os dez nomes de 2025 e rejeita os nomes legados.
- **Colisão de IDs com a coleção Cloud existente:** note type ou decks com os mesmos IDs do pacote antigo fazem o Anki fundir/renomear decks na importação. Teste `test_gerar_sem_colisao_com_cloud` na Task 3 verifica ID do modelo e faixa dos decks.
- **Campos do modelo fora de ordem ou em número errado:** cards renderizam vazios. Teste `test_modelo_e_campos` na Task 3 fixa os três nomes e a ordem.
- **Tema sem card ou card sem tema:** quebra o pareamento estudo ↔ revisão, que é o mecanismo de memorização. Teste `test_validar_rejeita_desbalanceamento` na Task 3 cobre.
- **Regeneração repetida acumulando decks do template:** uma segunda execução pode resurrectar decks antigos. Teste `test_gerar_idempotente` na Task 3 cobre.

---

### Task 1: Cards AppSec das cinco fases

**Files:**
- Create: `tests/base.py`
- Create: `tests/test_cards.py`
- Create: `scripts/cards_fase0.py`, `scripts/cards_fase1.py`, `scripts/cards_fase2.py`, `scripts/cards_fase3.py`, `scripts/cards_fase4.py`
- Create: `scripts/cards.py`

**Interfaces:**
- Consumes: nada.
- Produces: `from cards import CARDS` — `dict[int, list[tuple[str, str, str]]]` com chaves 1–38; cada tupla é `(frente, verso1, verso2)`.

- [ ] **Step 1: Escrever os testes de contrato dos cards**

`tests/base.py`:

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
```

`tests/test_cards.py`:

```python
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
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_cards.py" -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cards'`.

- [ ] **Step 3: Criar os módulos de cards e o agregador**

Em cada `scripts/cards_faseN.py`, defina `CARDS` com as chaves daquela fase. Títulos e ordem vêm da spec, seção "Estrutura do plano": fase0 = 1–6, fase1 = 7–18, fase2 = 19–24, fase3 = 25–32, fase4 = 33–38. Escreva 4–6 cards por tema usando a documentação oficial OWASP (Top 10 2025, ASVS 5.0.0, API Top 10 e cheat sheets) como fonte principal: `Frente` é uma pergunta atômica, `Verso1` define o conceito (O QUE É), `Verso2` mostra aplicação prática em revisão de código, triagem ou pipeline (EXEMPLO DE USO). Use os nomes exatos das categorias 2025 e não reintroduza os nomes legados da lista `LEGADOS`.

`scripts/cards.py`:

```python
from cards_fase0 import CARDS as FASE0
from cards_fase1 import CARDS as FASE1
from cards_fase2 import CARDS as FASE2
from cards_fase3 import CARDS as FASE3
from cards_fase4 import CARDS as FASE4

CARDS = {**FASE0, **FASE1, **FASE2, **FASE3, **FASE4}
```

- [ ] **Step 4: Rodar o teste e confirmar que passa**

Run: `python -m unittest discover -s tests -p "test_cards.py" -v`
Expected: PASS (5 testes).

- [ ] **Step 5: Commit**

```bash
git add tests/base.py tests/test_cards.py scripts/cards.py scripts/cards_fase0.py scripts/cards_fase1.py scripts/cards_fase2.py scripts/cards_fase3.py scripts/cards_fase4.py
git commit -m "feat: add AppSec cards for the five phases"
```

---

### Task 2: Plano de estudos em Markdown e parser de títulos

**Files:**
- Modify: `gemini-notebook.md` (substituir todo o conteúdo)
- Create: `scripts/notebook.py`
- Create: `tests/test_notebook.py`

**Interfaces:**
- Consumes: nada.
- Produces: `from notebook import titulos_notebooks` — `titulos_notebooks(caminho: Path) -> dict[int, str]`, lendo linhas `### Notebook NN — Título`.

- [ ] **Step 1: Escrever os testes do plano**

`tests/test_notebook.py`:

```python
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
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_notebook.py" -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'notebook'`.

- [ ] **Step 3: Criar o parser e reescrever o notebook**

`scripts/notebook.py` exponha `titulos_notebooks(caminho: Path) -> dict[int, str]`, usando a regex `^### Notebook (\d+) — (.+)$` com `re.M` e retornando `{int(numero): titulo.strip()}`.

Reescreva `gemini-notebook.md` com `# Fase 0` a `# Fase 4` e os 38 notebooks da spec, na ordem e com os títulos exatos da seção "Estrutura do plano". Cada notebook mantém o formato atual: `### Notebook NN — Título`, `- **Objetivo:**` e `- **Estrutura do Conteúdo:**` com 5 tópicos numerados. Substitua as "Orientações gerais" por versão AppSec: documentação oficial OWASP como fonte principal, um tema por material, fundamentos antes de conceitos avançados, terminologia técnica em inglês explicada em português e nenhum tema de fase futura sem necessidade. Público-alvo: estudante em preparação para vaga de AppSec Engineer.

- [ ] **Step 4: Rodar o teste e confirmar que passa**

Run: `python -m unittest discover -s tests -p "test_notebook.py" -v`
Expected: PASS (3 testes).

- [ ] **Step 5: Commit**

```bash
git add gemini-notebook.md scripts/notebook.py tests/test_notebook.py
git commit -m "feat: replace Cloud study plan with AppSec notebook"
```

---

### Task 3: Gerador AppSec e mapeamento

**Files:**
- Modify: `scripts/gerar_notebooks.py` (substituir conteúdo)
- Create: `tests/test_gerador.py`
- Modify: `MAPEAMENTO.md` (gerado)

**Interfaces:**
- Consumes: `titulos_notebooks(caminho: Path) -> dict[int, str]` (Task 2); `CARDS` (Task 1).
- Produces: `montar_decks(titulos, cards) -> list[tuple[int, str, str, list]]`; `validar(titulos, cards) -> int`; `gerar(decks, total, *, modelo: Path, saida: Path) -> None`; `escrever_mapa(titulos, decks, *, caminho: Path) -> None`; `main() -> None`.

- [ ] **Step 1: Escrever os testes do gerador**

`tests/test_gerador.py`:

```python
import json, sqlite3, tempfile, unittest, zipfile
from pathlib import Path
from base import ROOT
from cards import CARDS
from gerar_notebooks import gerar, escrever_mapa, montar_decks, validar

TITULOS = {i: "T%d" % i for i in range(1, 39)}
CARTOS = {i: [("pergunta %d" % i, "resposta", "exemplo")] for i in range(1, 39)}

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
        self.assertEqual(validar(TITULOS, CARTOS), 38)

    def test_modelo_e_campos(self):
        with self._abrir_apkg() as con:
            modelos = json.loads(con.execute("select models from col").fetchone()[0])
            modelo = next(iter(modelos.values()))
            self.assertEqual(modelo["name"], "AppSec")
            self.assertEqual([f["name"] for f in modelo["flds"]],
                             ["Frente", "Verso1", "Verso2"])

    def test_gerar_sem_colisao_com_cloud(self):
        with self._abrir_apkg() as con:
            modelos = json.loads(con.execute("select models from col").fetchone()[0])
            self.assertNotEqual(next(iter(modelos.values()))["id"], 1830472615)
            nomes = json.loads(con.execute("select decks from col").fetchone()[0])
            ids = [int(k) for k in nomes if k != "1"]
            self.assertTrue(all(2300000001 <= i <= 2300000038 for i in ids))
            self.assertEqual(len(ids), 38)

    def test_gerar_idempotente(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            saida = tmp / "AppSec.apkg"
            decks = montar_decks(TITULOS, CARTOS)
            for _ in range(2):
                gerar(decks, 38, saida=saida)
            with zipfile.ZipFile(saida) as z:
                dados = z.read("collection.anki2")
            bruto = tmp / "collection.anki2"
            bruto.write_bytes(dados)
            con = sqlite3.connect(bruto)
            self.assertEqual(con.execute("select count(*) from notes").fetchone()[0], 38)
            con.close()

    def test_escrever_mapa(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp) / "MAPEAMENTO.md"
            escrever_mapa(TITULOS, montar_decks(TITULOS, CARTOS), caminho=caminho)
            texto = caminho.read_text(encoding="utf-8")
            self.assertIn("38 decks", texto)
            self.assertIn("AppSec::01-", texto)
            self.assertIn("Fase", texto)
            self.assertNotIn("CLF-C02", texto)
            self.assertNotIn("SAA-C03", texto)

    def _abrir_apkg(self):
        import contextlib

        @contextlib.contextmanager
        def aberto():
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                saida = tmp / "AppSec.apkg"
                gerar(montar_decks(TITULOS, CARTOS), 38, saida=saida)
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
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_gerador.py" -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'gerar_notebooks'`.

- [ ] **Step 3: Reescrever o gerador**

`scripts/gerar_notebooks.py` deve:
- importar `CARDS` de `cards` e `titulos_notebooks` de `notebook`;
- definir `ROOT`, `NOTEBOOK`, `TEMPLATE = ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg"`, `OUTPUT = ROOT / "foco" / "AppSec.apkg"`, `MAPA = ROOT / "MAPEAMENTO.md"`;
- `validar(titulos, cards)`: exigir `set(titulos) == set(cards)`, 4–6 cards por tema, tuplas de 3 strings não vazias sem `\x1f`; retornar o total;
- `slug(titulo)`: `re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")`;
- `montar_decks`: para `n` em 1–38, produzir `(2300000000 + n, "AppSec::%02d-%s" % (n, titulos[n]), "appsec nb%02d_%s" % (n, slug(titulos[n])), cards[n])`;
- `gerar`: manter a lógica atual de ler `TEMPLATE`, extrair `collection.anki2`, limpar `notes`/`cards`/`revlog`/`graves`, copiar os outros arquivos do zip e reescrever a coluna `col`; antes de serializar, trocar no modelo `modelo["name"] = "AppSec"` e atribuir `modelo["id"] = 2300000000000` (atualizar também as referências ao ID antigo nos `models`, se houver); usar faixa de IDs de notas a partir de `2400000000000` e `guid = hashlib.md5(("%s-%02d" % (nome, indice)).encode()).hexdigest()[:12]`;
- remover `FONTES_EXTRA`, `carregar_extras()`, `carregar_certificacao()`, `EXTRAS_TITULOS`, `FORA_DA_PROVA`, `OVERRIDES_EXTRA`, `CARD_DUPLICADO`, `grupo_extra()` e `CERT_SOURCES`;
- `escrever_mapa`: gerar cabeçalho com total de decks/cards, uma seção por fase (`## Fase N — ...`), tabela com `| NN — Título | \`AppSec::NN-Título\` | Cards |` e orientação "estude o Notebook NN e revise o deck AppSec::NN no mesmo dia";
- `main()`: `titulos = titulos_notebooks(NOTEBOOK)`, `validar`, `montar_decks`, `gerar`, `escrever_mapa`, e imprimir `OK: 38 decks, N cards` e os caminhos de saída.

Aceitar parâmetros nomeados `modelo` e `saida` em `gerar` e `caminho` em `escrever_mapa` para permitir os testes com diretórios temporários.

- [ ] **Step 4: Rodar todos os testes e confirmar que passam**

Run: `python -m unittest discover -s tests -v`
Expected: PASS (todos os testes das Tasks 1–3).

- [ ] **Step 5: Commit**

```bash
git add scripts/gerar_notebooks.py tests/test_gerador.py MAPEAMENTO.md
git commit -m "feat: generate AppSec Anki package and mapping"
```

---

### Task 4: Remoção do material de Cloud e documentação

**Files:**
- Delete: `scripts/cards_cert.py`, `scripts/cards_vagas.py`
- Modify (mover): `foco/07-Notebooks.apkg` → `cloud-eng/07-Notebooks-Cloud.apkg`
- Modify: `foco/README.md`
- Create: `tests/test_repo.py`

**Interfaces:**
- Consumes: nada.
- Produces: docs e árvore de arquivos finais; nenhum módulo novo.

- [ ] **Step 1: Escrever os testes de limpeza**

`tests/test_repo.py`:

```python
import unittest
from base import ROOT

class RepoContract(unittest.TestCase):
    def test_arquivos_antigos_removidos(self):
        self.assertFalse((ROOT / "scripts" / "cards_cert.py").exists())
        self.assertFalse((ROOT / "scripts" / "cards_vagas.py").exists())
        self.assertTrue((ROOT / "cloud-eng" / "07-Notebooks-Cloud.apkg").exists())
        self.assertFalse((ROOT / "foco" / "07-Notebooks.apkg").exists())

    def test_sem_referencias_a_certificacao(self):
        for nome in ("foco/README.md", "MAPEAMENTO.md",
                     "gemini-notebook.md", "scripts/gerar_notebooks.py"):
            texto = (ROOT / nome).read_text(encoding="utf-8")
            self.assertNotIn("CLF-C02", texto, nome)
            self.assertNotIn("SAA-C03", texto, nome)

    def test_readme_appsec(self):
        texto = (ROOT / "foco" / "README.md").read_text(encoding="utf-8")
        self.assertIn("AppSec", texto)
        self.assertIn("foco/AppSec.apkg", texto)
        self.assertIn("38", texto)
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_repo.py" -v`
Expected: FAIL no teste `test_arquivos_antigos_removidos`.

- [ ] **Step 3: Aplicar a limpeza e reescrever o README**

Excluir os dois módulos de certificação/vagas. Mover o pacote antigo com `git mv foco/07-Notebooks.apkg cloud-eng/07-Notebooks-Cloud.apkg`. Reescrever `foco/README.md` descrevendo: arquivo único `foco/AppSec.apkg`, 38 decks em 5 fases, o pareamento "estude o Notebook NN e revise o deck AppSec::NN no mesmo dia", o tipo de nota `AppSec` com os três campos e o comando para regenerar (`python scripts/gerar_notebooks.py`). Não mencionar CLF-C02, SAA-C03, decks extras ou `fora-da-prova`.

- [ ] **Step 4: Rodar todos os testes e confirmar que passam**

Run: `python -m unittest discover -s tests -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: remove Cloud decks and rewrite AppSec docs"
```

---

### Task 5: Geração final e verificação de ponta a ponta

**Files:**
- Modify: `foco/AppSec.apkg` (gerado)
- Modify: `MAPEAMENTO.md` (regenerado)

**Interfaces:**
- Consumes: `main()` do gerador (Task 3).
- Produces: pacote final e mapeamento final.

- [ ] **Step 1: Rodar a suíte completa**

Run: `python -m unittest discover -s tests -v`
Expected: PASS (todos os testes).

- [ ] **Step 2: Gerar o pacote**

Run: `python scripts/gerar_notebooks.py`
Expected: saída contendo `OK: 38 decks, N cards` com `180 <= N <= 200`, seguida dos caminhos de `foco/AppSec.apkg` e `MAPEAMENTO.md`.

- [ ] **Step 3: Verificar o pacote gerado**

Run:

```bash
python -c "import zipfile,sqlite3,tempfile,pathlib,json; d=tempfile.TemporaryDirectory(); p=pathlib.Path(d.name)/'c.anki2'; p.write_bytes(zipfile.ZipFile('foco/AppSec.apkg').read('collection.anki2')); c=sqlite3.connect(p); print('decks', len(json.loads(c.execute('select decks from col').fetchone()[0]))-1, 'notes', c.execute('select count(*) from notes').fetchone()[0]); c.close()"
```

Expected: `decks 38 notes N` com o mesmo N da etapa anterior.

- [ ] **Step 4: Conferir o mapa e o status**

Run: `git status --short`
Expected: apenas `foco/AppSec.apkg` e `MAPEAMENTO.md` como alterados; nenhum arquivo de Cloud modificado.

- [ ] **Step 5: Commit dos artefatos finais**

```bash
git add foco/AppSec.apkg MAPEAMENTO.md
git commit -m "build: generate final AppSec deck package"
```
