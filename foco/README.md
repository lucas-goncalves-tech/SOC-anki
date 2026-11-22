# Conjunto focado de decks — AppSec Engineer

`foco/` contém **um único arquivo**, `foco/AppSec.apkg`, com **38 decks** e **190 cards**. Cada deck corresponde a um Notebook de `gemini-notebook.md`, na numeração exata, distribuído em 5 fases.

## Arquivo único

| Fase | Decks |
|------|-------|
| Fase 0 — Fundamentos | 6 |
| Fase 1 — Vulnerabilidades | 12 |
| Fase 2 — Validação ofensiva leve | 6 |
| Fase 3 — Ferramentas | 8 |
| Fase 4 — Processo | 6 |
| **Total** | **38** |

No Anki, os decks aparecem como `AppSec::01-Web Application Security Fundamentals` até `AppSec::38-Application Incident Response and Developer Enablement`.

## Como usar

Estude o Notebook `NN` e revise o deck `AppSec::NN-...` no mesmo dia. O pareamento completo está em `MAPEAMENTO.md`, na raiz.

## Tipo de nota

Todos os 190 cards usam o tipo de nota **`AppSec`**, com os três campos:

- `Frente` — a pergunta;
- `Verso1` — **O QUE É**;
- `Verso2` — **EXEMPLO DE USO**.

O layout mantém a pergunta centralizada em negrito, o divisor horizontal, os rótulos laranjas e o modo noturno. Identificadores curtos e comandos de uma linha (`s3:GetObject`, `0.0.0.0/0`) ficam inline em `<code>`; trechos de várias linhas usam `<pre class="codeblock"><code>` com fundo próprio.

## Importar no Anki

**Arquivo → Importar…** e selecione `foco/AppSec.apkg`. Como é um arquivo único, não há duplicatas.

## Regenerar o pacote

A partir da raiz do repositório:

```text
python scripts/gerar_notebooks.py
```

O comando reconstrói `foco/AppSec.apkg` e `MAPEAMENTO.md` a partir de `gemini-notebook.md` e dos cards em `scripts/`.

## Material antigo de Cloud

Os pacotes de Cloud continuam arquivados em `cloud-eng/`, incluindo `cloud-eng/07-Notebooks-Cloud.apkg`. Eles não fazem parte do fluxo de estudo de AppSec e não precisam ser importados.
