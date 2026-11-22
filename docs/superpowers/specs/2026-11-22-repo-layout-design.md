# Reorganização da árvore do repo — design curto

Data: 2026-11-22

## Intenção

Depois do pivot para AppSec, a raiz ainda mistura dois assuntos: os diretórios
`cloud-eng/` (23 `.apkg` de Cloud) e `AWS/` (CLF-C02) convivem com os arquivos
AppSec, e o pacote e o README da AppSec ficam escondidos em `foco/`. O usuário
quer homogeneizar: o que não é AppSec vai para `.archive/`, o que é AppSec vai
para a raiz junto com o README.

## Abordagem escolhida

Mover os arquivos com `git mv` e ajustar os poucos caminhos que o gerador e os
testes ainda esperam. O histórico do git preserva o conteúdo; nada é apagado.
As alternativas descartadas foram arquivar por exclusão (contraria o pedido de
manter os arquivos em `.archive/`) e reconstruir a árvore do zero (sem ganho).

## Layout-alvo

```text
.gitignore, LICENSE, skills-lock.json
README.md               ← foco/README.md
AppSec.apkg             ← foco/AppSec.apkg
gemini-notebook.md, MAPEAMENTO.md
assets/note-type.apkg   ← cópia de cloud-eng/foco-01-CLF-C02.apkg
scripts/, tests/, docs/, .agents/
.archive/
  ├── cloud/            ← cloud-eng/ inteiro
  └── aws/              ← AWS/ inteiro
```

`gemini-notebook.md` mantém o nome: ele é o plano de estudos no formato que o
usuário chamou de "Gemini notebook" e é lido pelo gerador.

## Decisão registrada

O molde do tipo de nota (`cloud-eng/foco-01-CLF-C02.apkg`) fica **fora** do
`.archive/`, em `assets/note-type.apkg`. Ele é uma dependência de build — o
gerador copia dele campos `Frente`/`Verso1`/`Verso2`, CSS com modo noturno e
`pre.codeblock` — e não é conteúdo Cloud. O `.archive/` fica apenas com
material inerte.

## Ajustes obrigatórios

- `scripts/gerar_notebooks.py`: `TEMPLATE` aponta para `assets/note-type.apkg`;
  `OUTPUT` aponta para `AppSec.apkg` na raiz; docstring e texto do
  `MAPEAMENTO.md` gerado atualizados para o caminho novo.
- `MAPEAMENTO.md`: regeneration sem alterar contagens (38 decks, 190 cards).
- `tests/test_repo.py`: verificações que citam `foco/README.md` e
  `cloud-eng/07-Notebooks-Cloud.apkg` passam a usar `README.md` e
  `.archive/cloud/07-Notebooks-Cloud.apkg`.
- `README.md`: caminhos de importação e regeneração atualizados, com uma linha
  explicando `.archive/` e `assets/note-type.apkg`.
- `foco/`: diretório vazio removido.

## Não metas / anti-metas

- Não alterar conteúdo: nenhum card, tema, deck, ID ou tag muda.
- Não renomear o repositório nem o plano de estudos.
- Não apagar material de Cloud — ele deve continuar acessível em `.archive/`.
- Falha se, ao final, algum teste quebrar ou o `.apkg` regenerado deixar de
  ter 38 decks e 190 cards.
