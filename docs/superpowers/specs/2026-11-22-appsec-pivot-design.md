# Pivot para AppSec — design

Data: 2026-11-22

## Intenção e por quê

O repo hoje é um curso de Cloud Engineer expresso em dois artefatos: um
`gemini-notebook.md` com temas bem picotados (Fases → Issues → 70 Notebooks) e
um pacote Anki único (`foco/07-Notebooks.apkg`) com um deck por tema. O
usuário quer mudar o **foco** do repo para AppSec, mantendo exatamente esse
princípio: notebook com temas atômicos de um lado, deck main com os assuntos
do outro.

O objetivo concreto é preparar para uma **vaga de Application Security
Engineer**, não para uma prova. A preocupação levantada na conversa foi que
AppSec tem um lado pentest e que muitos temas poderiam virar um material
"absurdamente desnecessário" — incluindo a dúvida sobre se seria possível
validar a memorização de tanta coisa. A resposta desenhada aqui é manter o
mecanismo de memorização que já existe (um tema → um deck → ~5 cards
atônicos, estudo pareado com revisão) e controlar o volume com um filtro
rígido de temas, em vez de controlar pela quantidade de cards.

## Metas

1. Substituir o plano de Cloud por um plano de estudos de AppSec com cerca de
   38 temas atônicos em 5 fases, ancorado em três fontes: OWASP Top 10 2025,
   OWASP ASVS 5.0.0 e competências recorrentes em vagas de AppSec Engineer.
2. Manter um único `.apkg` com um sub-deck por tema, agora com prefixo
   `AppSec::` e tipo de nota chamado `AppSec`.
3. Gerar cerca de 190 cards no mesmo padrão atual: pergunta central, divisor,
   rótulos `O QUE É` e `EXEMPLO DE USO`, termos técnicos em inglês explicados
   em português.
4. Incluir um braço de **validação ofensiva leve** — o suficiente para
   reproduzir achados e julgar exploitabilidade, sem metodologia de red team.
5. Reescrever `MAPEAMENTO.md` e a documentação, e deixar o gerador mais
   simples e reproduzível (`python scripts/gerar_notebooks.py`).
6. Preservar o material de Cloud no histórico do git e em arquivos separados,
   sem mantê-lo como trilha ativa do repo.

## Não metas

- Preparar para certificações. Não haverá decks equivalentes a CLF-C02 ou
  SAA-C03.
- Formar pentester / red team. Não haverá metodologia completa de pentest,
  cadeias de exploração avançadas ou preparação para OSCP.
- Cobrir engenharia de cloud em profundidade. Conhecimento de cloud entra só
  quando a vaga de AppSec pede (ex.: container/IaC scanning, pipelines).
- Criar um tipo de nota novo do zero. O tipo existente é adaptado.

## Anti-metas

O que tornaria isso um fracasso mesmo funcionando tecnicamente:

- Um deck inchado com temas que não aparecem na vaga — exatamente o
  "absurdamente desnecessário" que o usuário quis evitar.
- Cards que ensinam vários conceitos de uma vez ou que só fazem sentido com
  um vídeo externo. O padrão atual de atomicidade deve ser mantido.
- Perder a capacidade de regenerar o `.apkg` a partir das fontes em Markdown
  e Python.
- Quebrar o pareamento tema ↔ deck, que é o que torna a memorização
  verificável na prática.

## Restrições

- O gerador atual é Python puro (`sqlite3`, `zipfile`, `hashlib`, `json`),
  sem dependências externas. Continua assim.
- O tipo de nota é copiado de `cloud-eng/foco-01-CLF-C02.apkg`: campos
  `Frente`, `Verso1`, `Verso2`, CSS com modo noturno e blocos de código
  renderizados como `<pre class="codeblock"><code>`. Isso deve ser preservado.
- O notebook atual usa terminologia técnica em inglês com explicação em
  português e define que cada material deve ser restrito ao seu tema.
- A OWASP Top 10 vigente é a de 2025 (não a de 2021): SSRF está dentro de
  A01 Broken Access Control, Software Supply Chain Failures é A03, e A10 é
  Mishandling of Exceptional Conditions. O ASVS vigente é 5.0.0 (mai/2025),
  com tradução em português.
- Ambiente Windows; os caminhos no gerador são resolvidos a partir de
  `Path(__file__).resolve().parents[1]`.

## Abordagens consideradas

| Abordagem | O que faz | Trade-off |
|-----------|----------|-----------|
| **A. Pivotar o conteúdo, manter o pipeline** (escolhida) | Troca notebooks, cards, nomes e docs; reaproveita gerador, tipo de nota e CSS | Limpo e de baixo risco; o preço é perder a regeneração dos decks de Cloud pelos scripts (os `.apkg` antigos e o git permanecem) |
| B. Trilha paralela | Mantém Cloud e adiciona AppSec ao lado | Nada se perde, mas o repo deixa de ter foco único e a manutenção dobra |
| C. Repo do zero | Novo gerador, novo tipo de nota, nova estrutura | Conceitualmente mais limpo, mas descarta o que já funciona e aumenta risco sem ganho em memorização |

A escolha foi A porque preserva exatamente a mecânica que já foi validada no
repo (um tema → um deck → cards atônicos, com mapeamento ligando estudo e
revisão) e remove somente o que estava amarrado a Cloud e a provas.

## Decisões tomadas

### Filtro de temas

Só entra tema que satisfaz pelo menos um critério:

1. Aparece na OWASP Top 10 2025 ou no ASVS 5.0.0;
2. Aparece recorrentemente em vagas de AppSec Engineer;
3. É necessário para validar ou explicar um tema dos critérios anteriores.

Qualquer tema que não caiba nesses três fica de fora. É esse filtro — e não
um teto artificial de cards — que controla o volume.

### Competências observadas em vagas (referência do critério 2)

A pesquisa que ancorou o critério 2 encontrou, de forma recorrente em vagas
de AppSec Engineer:

- threat modeling e revisão de design/código;
- classes de vulnerabilidade web/API — controle de acesso, SSRF, injeção,
  autenticação e autorização;
- operação e calibração de SAST, DAST, IAST, SCA, secrets scanning e
  container/IaC scanning;
- triagem de achados, redução de falsos positivos, gestão de vulnerabilidades
  com SLA e métricas (MTTR, densidade, cobertura);
- Secure SDLC/DevSecOps, gates de CI/CD, shift-left e NIST SSDF (SP 800-218);
- supply chain — SBOM, assinatura de imagens, SLSA, CycloneDX/SPDX;
- cloud e pipelines (AWS aparece com frequência);
- parceria com engenheiros, revisão de PRs e comunicação de risco para
  liderança;
- apoio a incidentes de aplicação e coordenação de pentests de terceiros.

Não há corpus de vagas no repo e não será criado. A lista de 38 temas abaixo
é a saída autoritativa do critério 2; as competências acima são a
justificativa registrada, não uma lista adicional de temas.

### Estrutura do plano (38 temas propostos)

```text
Fase 0 — Fundamentos (6)
  01 Web Application Security Fundamentals
  02 HTTP for AppSec
  03 Authentication, Sessions and Authorization
  04 Applied Cryptography for Applications
  05 OWASP Top 10 2025 Overview
  06 OWASP ASVS 5.0 and Security Requirements

Fase 1 — Vulnerabilidades (12)
  07 Broken Access Control (A01, inclui SSRF)
  08 Security Misconfiguration (A02)
  09 Software Supply Chain Failures (A03)
  10 Cryptographic Failures (A04)
  11 Injection (A05)
  12 Insecure Design (A06)
  13 Authentication Failures (A07)
  14 Software or Data Integrity Failures (A08)
  15 Security Logging and Alerting Failures (A09)
  16 Mishandling of Exceptional Conditions (A10)
  17 API Security (OWASP API Top 10)
  18 Client-Side Security (XSS, CSRF, CORS, clickjacking)

Fase 2 — Validação ofensiva leve (6)
  19 Burp Suite and Interception Proxies
  20 Request Manipulation and Parameter Testing
  21 Testing Authentication and Authorization
  22 Testing Injection and SSRF
  23 Testing Client-Side and APIs
  24 Evidence, Lab Practice and Reporting

Fase 3 — Ferramentas (8)
  25 SAST
  26 DAST
  27 SCA and Dependency Scanning
  28 Secrets Detection and Management
  29 Container and IaC Scanning
  30 Scanner Tuning and False Positive Reduction
  31 Security Gates in CI/CD
  32 AppSec Metrics and Reporting

Fase 4 — Processo (6)
  33 Threat Modeling with STRIDE
  34 Secure Code Review
  35 Secure SDLC and NIST SSDF
  36 Vulnerability Management and Remediation SLAs
  37 Software Supply Chain Controls (SBOM, SLSA, signing)
  38 Application Incident Response and Developer Enablement
```

Não haverá capstone nem decks extras: os 38 temas já esgotam o filtro acima.
O builder pode ajustar títulos e a distribuição exata dos cards, desde que o
filtro e a divisão em 5 fases sejam respeitados.

### Cards

- 4 a 6 cards por tema, meta de ~190 no total.
- Formato inalterado: `Frente` com a pergunta, `Verso1` = O QUE É,
  `Verso2` = EXEMPLO DE USO.
- Fontes prioritárias para o conteúdo: documentação oficial da OWASP (Top 10 2025,
  ASVS 5.0.0, API Top 10, cheat sheets) e as competências observadas nas
  vagas. Termos técnicos ficam em inglês, com explicação em português.

### Arquivos e nomenclatura

- `gemini-notebook.md` é substituído pelo plano AppSec (mantém o nome do
  arquivo para preservar o contrato com o gerador, mas muda todo o conteúdo).
- `scripts/cards_fase0.py` ... `cards_fase4.py`: um arquivo de cards por fase.
- `scripts/cards_cert.py` e `scripts/cards_vagas.py` saem da árvore.
- `scripts/gerar_notebooks.py`: permanecem a leitura do Markdown, a validação
  tema ↔ cards, a cópia do modelo de nota e a geração de `.apkg`. Saem
  `FONTES_EXTRA`, `carregar_extras()`, `carregar_certificacao()`,
  `EXTRAS_TITULOS`, `FORA_DA_PROVA`, `OVERRIDES_EXTRA`, `CARD_DUPLICADO` e as
  regras de certificação.
- Tipo de nota: nome muda de `Cloud Engineer` para `AppSec`. Mantêm-se campos,
  CSS e templates. O ID do modelo deve ser trocado na geração para não
  colidir com o tipo `Cloud Engineer` já existente na coleção do Anki.
- Decks: `AppSec::NN-Tema`, com IDs sequenciais a partir de `2300000000`.
  A faixa `2100000000` pertence aos decks de Cloud; reaproveitá-la faria o
  Anki fundir ou renomear os decks antigos na importação, o que anularia a
  meta de preservar o material de Cloud.
- Tags: `appsec nnNN_slug`, sem a tag `fora-da-prova` (não há provas).
- Saída: `foco/AppSec.apkg`. O pacote antigo
  `foco/07-Notebooks.apkg` é movido para `cloud-eng/07-Notebooks-Cloud.apkg`
  para não deixar dois pacotes concorrentes em `foco/`.
- `MAPEAMENTO.md` e `foco/README.md` são reescritos com as 5 fases, os 38
  decks e o total de cards. O README explica o pareamento estudo ↔ revisão.

## O que fica para o builder

- Redigir os ~190 cards a partir das fontes oficiais, respeitando o formato
  e a atomicidade.
- Ajustar a função `validar()` e `escrever_mapa()` para as 5 fases e os 38
  temas.
- Definir os IDs numéricos do modelo e a forma exata de renomeá-lo no JSON
  copiado do arquivo-base.
- Ajustar títulos de temas desde que o filtro e as contagens por fase sejam
  mantidos.
