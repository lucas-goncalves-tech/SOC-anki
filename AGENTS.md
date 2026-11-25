# AGENTS.md — cloud-engineer-anki

Três pacotes Anki independentes na raiz: `07-Cloud-Engineer-Final.apkg` (trilha AWS/Cloud), `08-Soft-Skills.apkg` e `09-Prompt-Engineering.apkg`. Cada `.apkg` é **derivado**: o conteúdo vivo está em `scripts/`. Editar o binário é trabalho perdido na próxima geração.

## Ponteiros

| Material | Abrir quando |
|---|---|
| `README.md` | visão geral, contagens, importação no Anki, decisões de migração |
| `MAPEAMENTO.md` | ordem das etapas, origem de cada deck (`nb`/`extra`/`vaga`), contagens |
| `gemini-notebook.md` | título e tópicos-base de um notebook do pacote 07 |
| `scripts/revisao.py` | mudar `ETAPAS`, acrescentar cards (`ADICOES`), corrigir certificações (`OVERRIDES_CERT`) |
| `.archive/` | comparar versões antigas ou recuperar o modelo de nota; fora isso, ignorar |
| `.agents/skills/` | criar ou editar cards no Anki com as skills `anki` e `anki-card-generator` |

## Padrão do card

- Uma nota, um card. Modelo `Cloud Engineer` (ID `1830472615`), campos `Frente`, `Verso1` = **O QUE É**, `Verso2` = **EXEMPLO DE USO**. O CSS laranja e o modo noturno vêm do arquivo-base em `.archive/cloud-eng/foco-01-CLF-C02.apkg`; reaproveite o modelo, criar outro quebra a compatibilidade.
- Tupla canônica: `(Frente, "O QUE É", "EXEMPLO DE USO")` — três strings não vazias, sem `\x1f`. `Verso2` é afirmação ou exemplo pronto, nunca pergunta.
- Estilo: português, termos técnicos em inglês, aspas retas, ação prática no lugar de estatística.
- **GUID é identidade:** `md5(f"{nome_do_deck}-{indice:02d}")[:12]`. No pacote 07 o gerador usa `nome_antigo` de propósito, para renomear decks sem quebrar a reimportação. Nos pacotes 08 e 09 o GUID vem do nome atual: mudou o nome, mudou o GUID → exija import limpo no Anki e registre o procedimento no README.
- Ordem de estudo: prefixo numérico no nome do deck (`01-…`) mais `due` sequencial. Sem prefixo, a árvore ordena alfabeticamente.
- Faixas reservadas: notas `1700000000000` (07), `1750000000000` (08), `1760000000000` (09), passo 10. Decks: `2100000000+num` (07), `2300000091–94` (08), `2300000095–98` (09).

## Scripts por responsabilidade

- **Geradores:** `gerar_notebooks.py` (pacote 07 e a parte do 07 no `MAPEAMENTO.md`; preserva as seções 08 e 09 do arquivo), `gerar_soft_skills.py` (08), `gerar_prompt_engineering.py` (09). Os dois últimos importam `ler_modelo()` e `slug()` do primeiro. Todos limpam `notes`, `cards`, `revlog` e `graves` antes de gravar.
- **Conteúdo:** `cards_fase0.py` (notebooks 01–23), `cards_fase1.py`, `cards_fase2.py`, `cards_vagas.py` (81–86), `cards_cert.py` (certificações), `cards_soft_skills.py` (08), `cards_prompt_engineering.py` (09).
- **Verificação do 07:** `verificar_revisao.py` e `verificar_final.py` são portas históricas contra `.archive/`; rode-as depois de qualquer mudança no pacote 07.
- **Texto:** `humanizar_apkgs.py` aplica substituições exatas aos três apkgs, preservando GUIDs e IDs.

## Alterar cards

**Pacote 07**

1. Localize o dono do card: `cards_fase0/1/2.py` (01–70), `cards_vagas.py` (81–86), `cards_cert.py` com `revisao.py: OVERRIDES_CERT` (certificações) ou `revisao.py: ADICOES` (lacunas). Critério: o número do notebook existe em `revisao.py: ETAPAS` e o título casa com `gemini-notebook.md`.
2. Edite a tupla no módulo de origem. Cartões novos entram ao fim do deck, porque a posição participa do GUID. Critério: `validar()` passa e a frente nova não repete outra frente do pacote.
3. Rode `python gerar_notebooks.py` e `python verificar_final.py`. Critério: os dois scripts terminam sem erro, as seções 08 e 09 do `MAPEAMENTO.md` seguem intactas e as contagens casam com o `README.md`.

**Pacotes 08 e 09**

1. Edite `DECKS` em `cards_soft_skills.py` ou `cards_prompt_engineering.py`. Critério: a tupla editada está no módulo e o número do deck permanece na faixa reservada.
2. Rode o gerador correspondente. Critério: `validar()` passa e a contagem impressa casa com o `README.md`.
3. Se o nome do deck mudou, os GUIDs mudaram: documente a importação limpa no README. Critério: nenhuma frente duplicada, nenhum campo vazio e a nota de migração no README orienta remover o deck antigo antes de importar.
