# Design — refazer `foco/08-Soft-Skills.apkg` com cards de soft skills e LinkedIn

Data: 2026-11-24 · Status: **aprovado**

## Intenção

O `foco/08-Soft-Skills.apkg` atual está tecnicamente saudável (4 decks, 26 notas, modelo
`Cloud Engineer`, sem duplicatas, sem colisão de IDs), mas cobre só *rotina de trabalho*
e *STAR*. Os assuntos que aparecem nos cursos assistidos — perfil/networking no LinkedIn,
comunicação (escuta ativa, CNV, assertividade), gestão de tempo e comportamento — não têm
card nenhum. O objetivo é **refazer o pacote** com uma árvore de decks nova, contendo o
que foi montado nesta sessão: os 26 cards existentes reorganizados + 23 novos = 49.

## Goals

- **Árvore nova**: só decks novos (IDs `2300000091–94`), 49 cards no total.
  Os decks `87–90` saem do arquivo.
- Todo card rastreável a um título de aula, slide ou material que já está na base de
  cursos assistida — nada de conteúdo externo.
- Regenerar `foco/08-Soft-Skills.apkg` pelo gerador já existente.
- Sincronizar `foco/README.md` e `MAPEAMENTO.md` com a árvore e as contagens novas.
- Importar os cards no Anki desktop via AnkiConnect **depois** da aprovação do conteúdo.

## Non-goals / anti-goals

- **Nenhuma menção a caminho, URL ou fonte fora do repositório** em nenhum arquivo
  (README, MAPEAMENTO, design, comentários de código). Os cards falam do assunto, não
  da origem.
- Nada de conteúdo só de pesquisa web: se não está nos material assistido, não vira card.
- Não mexer em `foco/07-Notebooks.apkg` nem nos decks 01–86.
- Não criar modelo de nota novo — reaproveitar `Cloud Engineer` (`Frente`, `Verso1`, `Verso2`).
- Não alterar o **texto** dos 26 cards atuais — só mudam de deck. Exceção: a
  correção pedida em 2026-11-24 removeu perguntas do `Verso2` (11 cards, 6 deles
  originais) — `Verso2` é sempre afirmação ou exemplo, nunca pergunta.

## Abordagens consideradas

| # | Abordagem | Resultado |
|---|-----------|-----------|
| A | Acrescentar os 23 cards nos decks 87–90 já existentes | Descartada: o pedido é refazer o pacote com decks novos |
| B | Um deck novo só, com tudo dentro | Descartada: mistura comunicação, LinkedIn e entrevista num único baralho |
| **C** | **Reescrever a árvore com 4 decks novos, reorganizando os 49 cards** | **Escolhida** |

## Decisões

- **Árvore nova, sem os decks 87–90.** Os 4 decks novos nascem com IDs
  `2300000091`, `2300000092`, `2300000093`, `2300000094` — fora da faixa dos decks
  antigos, então não colidem nem sobrescrevem os anteriores.
- **Os 26 cards atuais entram de novo**, reorganizados pelos temas dos decks novos.
- **Formato de card**: `Frente` = tema curto em uma linha · `Verso1` = a regra ·
  `Verso2` = exemplo pronto. Mesmo critério dos 26 atuais.
- **Atomicidade**: um conceito por card. Listas do tipo "7 passos do resumo" viram um
  card só quando a lista *é* o conceito memorizado; caso contrário, dividir.
- **Tags**: continuam `soft-skills` + `nbXX_slug_do_deck` (geradas pelo próprio gerador).
- **IDs de nota**: faixa `1750000000000+`, mantida pelo `gerar_soft_skills.py`.
- **`MAPEAMENTO.md`**: hoje só documenta o 07. Passa a documentar também o 08.

## Escopo dos decks

Árvore final do `foco/08-Soft-Skills.apkg` — 4 decks, 49 cards:

| # | Deck | Cards |
|---|------|-------|
| 91 | `Soft Skills::LinkedIn e Marca Pessoal` | 15 |
| 92 | `Soft Skills::Comunicação e Relacionamento` | 12 |
| 93 | `Soft Skills::Comportamento e Desenvolvimento` | 12 |
| 94 | `Soft Skills::Entrevista e Carreira` | 10 |

### 91 — LinkedIn e Marca Pessoal (15 = 5 existentes + 10 novos)

**Existentes:** Resumo do LinkedIn · Procurar vagas no LinkedIn · Pedir indicação ou
referência · Postar conteúdo técnico · O que evitar no perfil.

**Novos:**

1. Primeira impressão no perfil — fotografia, headline e resumo
2. Estrutura de um resumo profissional impactante
3. Palavras-chave no perfil: onde inserir e como usar
4. Realizações: quantifique em vez de adjetivar
5. Status das vagas em "Minhas vagas"
6. Planilha de acompanhamento de candidaturas
7. Avisar a rede sobre disponibilidade: aberto vs. privativo
8. Texto de apresentação para convite/abordagem
9. Laços fracos × laços fortes na rede de contatos
10. Pesquisar a empresa antes de se candidatar

### 92 — Comunicação e Relacionamento (12 = 7 existentes + 5 novos)

**Existentes:** Atualização diária · Atualização em incidente · Dar feedback difícil ·
Receber crítica · Pedir ajuda em incidente · Escrever postmortem · Comunicar risco de prazo.

**Novos:**

1. Escuta ativa
2. Comunicação não violenta: observação, sentimento, necessidade, pedido
3. Assertividade × passividade × agressividade
4. Comunicação não verbal em apresentação e vídeo
5. Armadilhas ao dar feedback

### 93 — Comportamento e Desenvolvimento (12 = 6 existentes + 6 novos)

**Existentes:** Erro em produção · Síndrome do impostor · Pedir feedback ao líder ·
Transformar teoria em competência · Lidar com prazo apertado · Documentar decisão técnica.

**Novos:**

1. Princípio de Pareto (80/20) na escolha das tarefas
2. Multitarefa: o custo da troca de contexto
3. Diário das emoções e gatilhos
4. Perfis comportamentais: adaptar o discurso
5. Pontos fortes × pontos fracos: como administrar os fracos
6. Missão pessoal como filtro de decisão

### 94 — Entrevista e Carreira (10 = 8 existentes + 2 novos)

**Existentes:** Responder "conte sobre você" · Estruturar resposta STAR · STAR sem
experiência profissional · Provar comunicação na entrevista · Falar de uma falha ·
Pergunta técnica que você não sabe · Preparar histórias para entrevista · Encerrar a
entrevista.

**Novos:**

1. STAR fora da entrevista (descrever conquistas em currículo e perfil)
2. Follow-up pós-candidatura

## Como é feito

1. Reescrever `scripts/cards_soft_skills.py` (dict `DECKS`, chaves **91–94**, 49 cards).
2. Ajustar `scripts/gerar_soft_skills.py` para a faixa de deck nova (`2300000091–94`) e
   o `validar()` que hoje exige `numero >= 87`.
3. `python scripts/gerar_soft_skills.py` → regrava `foco/08-Soft-Skills.apkg`.
4. Rodar a validação estrutural (GUIDs, campos, decks, faixa de IDs, deck vazio).
5. Atualizar `foco/README.md` e `MAPEAMENTO.md` com a árvore e as contagens novas.
6. **Aprovação dos 23 cards novos texto a texto pelo humano.**
7. Importar no Anki via AnkiConnect nos decks `Soft Skills::…` novos.

## Riscos

- **GUIDs são derivados do nome do deck + índice**, e os nomes de deck mudam por
  completo. Se o `08` atual já foi importado no Anki, os 26 cards antigos entram como
  **duplicados** (os decks `87–90` ficam órfãos com os reviews). Mitigação: antes de
  importar, checar se os decks `Soft Skills::…` antigos existem no Anki e combinar a
  limpeza deles.
- Cards de cursos sem transcrição dependem do título da aula; onde o título não bastar,
  o card fica de fora em vez de ganhar conteúdo inventado.
