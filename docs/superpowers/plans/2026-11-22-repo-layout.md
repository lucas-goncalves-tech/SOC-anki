# Reorganização da árvore do repo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deixar a raiz com apenas os arquivos AppSec, mover todo o material Cloud para `.archive/` e manter o gerador funcional com o molde do tipo de nota fora do archive.

**Architecture:** Primeiro o build é deslocado para novos caminhos (`assets/note-type.apkg`, `AppSec.apkg` na raiz) com os testes verdes; depois os arquivos antigos são movidos com `git mv` e um teste de layout fixa a árvore final. Nenhum conteúdo de card, tema, deck ou ID muda.

**Tech Stack:** Python 3 (stdlib), `unittest`, `git mv`, `.apkg` (zip + SQLite).

**Spec:** `docs/superpowers/specs/2026-11-22-repo-layout-design.md`

## Global Constraints

- Mover arquivos com `git mv`; nada é apagado definitivamente do histórico do git.
- Layout final exato: `README.md`, `AppSec.apkg`, `gemini-notebook.md`, `MAPEAMENTO.md`, `assets/note-type.apkg`, `scripts/`, `tests/`, `docs/`, `.agents/` na raiz; `.archive/cloud/` e `.archive/aws/` com o material Cloud.
- `assets/note-type.apkg` é uma cópia byte-idêntica de `cloud-eng/foco-01-CLF-C02.apkg` antes do arquivamento.
- Nenhum card, tema, deck, ID ou tag muda: o pacote final continua com 38 decks e 190 cards.
- Codificação UTF-8 em arquivos de texto; comandos executados na raiz do repo.
- `gemini-notebook.md` mantém o nome.

## Review Focus

- **Gerador quebrado depois do arquivamento:** se `TEMPLATE` ainda apontar para `cloud-eng/`, a regeneração falha. Teste `test_gerador_aponta_novos_caminhos` + `test_gerar_apos_molde` na Task 1.
- **Molde corrompido ou diverso do original:** o tipo de nota deixaria de ter os três campos. Teste `test_molde_existe_e_valido` na Task 1 e `test_molde_igual_ao_arquivado` na Task 2.
- **Conteúdo alterado durante a mudança:** uma regeneração descuidada pode mudar contagens. Verificação de 38 decks / 190 cards na Task 1 e teste `test_pacote_tem_38_decks_e_190_cards` na Task 2.
- **Arquivamento incompleto:** decks de Cloud podem ficar fora do `.archive/`. Teste `test_arquivos_estao_arquivados` na Task 2.
- **Caminhos antigos espalhados em código/docs:** quebram a regeneração e confundem o usuário. Teste `test_sem_referencias_a_caminhos_antigos` na Task 2.

---

### Task 1: Novo build e referências

**Files:**
- Create: `assets/note-type.apkg` (cópia do arquivo-base)
- Create: `tests/test_build_asset.py`
- Modify: `scripts/gerar_notebooks.py` (docstring, `TEMPLATE`, `OUTPUT`, texto do mapa)
- Create: `AppSec.apkg` (gerado)
- Modify: `MAPEAMENTO.md` (regenerado)

**Interfaces:**
- Consumes: `CARDS` de `scripts/cards.py`; `titulos_notebooks()` de `scripts/notebook.py`; funções `gerar`, `montar_decks`, `validar` do próprio gerador.
- Produces: `TEMPLATE = ROOT / "assets" / "note-type.apkg"`, `OUTPUT = ROOT / "AppSec.apkg"`; nenhuma assinatura pública muda.

- [ ] **Step 1: Escrever os testes do novo build**

`tests/test_build_asset.py`:

```python
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
```

- [ ] **Step 2: Rodar o teste focado e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_build_asset.py" -v`
Expected: FAIL no `test_molde_existe_e_valido` (arquivo ausente).

- [ ] **Step 3: Copiar o molde do tipo de nota**

Copiar `cloud-eng/foco-01-CLF-C02.apkg` para `assets/note-type.apkg` preservando os bytes exatamente (por exemplo `Copy-Item` no PowerShell ou `shutil.copyfile`). Não modificar o conteúdo.

- [ ] **Step 4: Atualizar os caminhos no gerador**

Em `scripts/gerar_notebooks.py`: `TEMPLATE = ROOT / "assets" / "note-type.apkg"`; `OUTPUT = ROOT / "AppSec.apkg"`; docstring do módulo e a linha do cabeçalho de `escrever_mapa()` passam a citar `AppSec.apkg` e `assets/note-type.apkg` em vez de `foco/AppSec.apkg` e `cloud-eng/foco-01-CLF-C02.apkg`. Nenhuma outra lógica muda.

- [ ] **Step 5: Regenerar pacote e mapa**

Run: `python scripts/gerar_notebooks.py`
Expected: `OK: 38 decks, 190 cards` e saídas `AppSec.apkg` (raiz) e `MAPEAMENTO.md`.

- [ ] **Step 6: Rodar a suíte completa**

Run: `python -m unittest discover -s tests -v`
Expected: PASS (32 testes), sem mudanças em contagens de cards.

- [ ] **Step 7: Commit**

```bash
git add assets/note-type.apkg AppSec.apkg MAPEAMENTO.md scripts/gerar_notebooks.py tests/test_build_asset.py
git commit -m "build: move note template and package to root paths"
```

---

### Task 2: Arquivamento e layout final

**Files:**
- Create: `tests/test_layout.py`
- Modify: `tests/test_repo.py` (caminhos)
- Modify (mover): `foco/README.md` → `README.md`; `cloud-eng/` → `.archive/cloud/`; `AWS/` → `.archive/aws/`
- Delete: `foco/AppSec.apkg` (cópia idêntica já gerada na raiz na Task 1) e diretório `foco/`

**Interfaces:**
- Consumes: `AppSec.apkg` e `assets/note-type.apkg` da Task 1.
- Produces: árvore final; nenhuma interface de código muda.

- [ ] **Step 1: Escrever os testes do layout**

`tests/test_layout.py`:

```python
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
```

Atualizar `tests/test_repo.py`: trocar `foco/README.md` por `README.md` nas duas verificações e `cloud-eng/07-Notebooks-Cloud.apkg` por `.archive/cloud/07-Notebooks-Cloud.apkg`.

- [ ] **Step 2: Rodar o teste focado e confirmar que falha**

Run: `python -m unittest discover -s tests -p "test_layout.py" -v`
Expected: FAIL no `test_raiz_appsec` (`README.md` ausente na raiz).

- [ ] **Step 3: Mover os arquivos**

No PowerShell, na raiz do repo:
- `git mv foco/README.md README.md`
- `git rm foco/AppSec.apkg` (o pacote equivalente já está na raiz desde a Task 1)
- criar `.archive`, depois `git mv cloud-eng .archive/cloud` e `git mv AWS .archive/aws`
- remover o diretório `foco/` se ainda existir vazio

- [ ] **Step 4: Atualizar o README**

Em `README.md`, trocar qualquer referência a `foco/AppSec.apkg` por `AppSec.apkg`, ao comando de regeneração manter `python scripts/gerar_notebooks.py`, e acrescentar duas frases curtas: o material Cloud está em `.archive/` e o gerador usa `assets/note-type.apkg` como molde do tipo de nota. Não alterar o conteúdo dos 38 temas.

- [ ] **Step 5: Rodar a suíte completa**

Run: `python -m unittest discover -s tests -v`
Expected: PASS (38 testes), com o pacote da raiz ainda com 38 decks e 190 cards.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: archive Cloud material and flatten AppSec files to root"
```
