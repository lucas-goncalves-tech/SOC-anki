# Conjunto focado de decks — Cloud Engineer

A raiz contém **quatro arquivos independentes**:

- `07-Cloud-Engineer-Final.apkg` — 94 decks folha e 700 cards: 688 originais + 12 lacunas pontuais, com correções adicionais e sem frentes duplicadas. É o deck principal.
- `08-Soft-Skills.apkg` — 4 decks e 59 cards de soft skills aplicáveis (comunicação, comportamento, entrevistas e LinkedIn), com cartões de situações técnicas. É um pacote separado: não altera nem duplica o arquivo principal.
- `09-Prompt-Engineering.apkg` — 4 decks e 94 cards de prompt engineering (fundamentos, técnicas de prompting, estrutura e controle da resposta, aplicação prática). Também é separado.
- `SOC-N1-N2.apkg` — 10 decks e 236 cards de SOC nas profundidades N1 e N2 (208 + 28). É separado e não duplica o arquivo principal.

Tem umas coisas antigas em `.archive/`. Pode ignorar.

## Trilha revisada

| Grupo | Decks | Cards |
|-------|-------|-------|
| Etapas 01–09 | 84 | 448 |
| Apêndice multicloud | 2 | 24 |
| Certificações | 8 | 228 |
| **Total** | **94** | **700** |

No Anki, a árvore fica assim:

```text
Cloud Engineer
  01-Fundamentos de Infraestrutura
  02-Fundamentos AWS
  03-Serviços AWS
  04-Infraestrutura como Código
  05-Containers e Orquestração
  06-CI-CD e Segurança de Desenvolvimento
  07-Operações e Observabilidade
  08-Arquitetura e Produção
  09-Consolidação
  10-Apêndice Multicloud
  11-Certificações
    CLF-C02
      01-Conceitos
      02-Segurança
      03-Serviços
      04-Custos
    SAA-C03
      01-Seguro
      02-Resiliente
      03-Performance
      04-Custo
```

- **Etapas 01–09** — a ordem de estudo. Primeiro infraestrutura, Linux, Git e redes; depois fundamentos AWS, serviços, IaC, containers, CI/CD, operações, arquitetura e consolidação. Git aparece depois de Linux; Kubernetes aparece depois de Docker e ECS; Nginx e redes complementares entram junto de redes.
- **10-Apêndice Multicloud** — Azure e GCP. São opcionais e não são pré-requisitos para dominar AWS.
- **11-Certificações** — CLF-C02 e SAA-C03 separados da trilha profissional. Estude depois de consolidar o conteúdo; use os decks para revisar e identificar lacunas.
- **Origem dos decks** — o mapa completo, com o número original de cada notebook/extra/vaga, está em `MAPEAMENTO.md`.

## Correções e lacunas da versão final

A revisão preserva os 688 cartões originais e acrescenta 12 cartões pontuais. As principais correções:

- Cloud Computing: virtualização como um habilitador, não como origem única.
- Private Cloud: propriedade, hospedagem e controle operacional são coisas distintas.
- Multicloud: reduzir lock-in é possível, mas não automático.
- CIDR: fórmula `2^h - 2` com exceções `/31` e `/32`.
- DNS: resolução recursiva x iterativa e diagnóstico de propagação.
- Docker Networking: DNS por nome apenas em bridge definida pelo usuário.
- Terraform State: pode conter valores sensíveis e precisa de backend protegido.
- NAT Gateway x VPC Endpoints.
- ACM: certificados para CloudFront precisam estar em `us-east-1`.
- Lambda: timeout, memória, concorrência e modelo efêmero.
- RDS Multi-AZ DB instance x Multi-AZ DB cluster.
- EC2 Instance Store: perda em stop, hibernate e terminate; reboot não apaga.
- Kubernetes Secrets: base64 não é criptografia; RBAC controla o recurso e encryption at rest protege o etcd.
- IAM OIDC: trust policy valida `aud` e `sub`.
- AWS WAF: regras gerenciadas, rate-based rules e associação ao ALB/CloudFront/API Gateway.
- EKS: control plane, data plane e add-ons distinguidos.
- Systems Manager: SSM Agent, conectividade e IAM como requisitos.
- Terraform State: locking, versionamento e recuperação de versões anteriores.
- GitHub Actions: OIDC no lugar de access key estática no deploy.

Lacunas acrescentadas: troubleshooting avançado de Linux, DHCP/ARP, IPv6 operacional, DNS na prática, IAM OIDC, AWS KMS, AWS Config, AWS WAF, AWS Systems Manager, AWS Secrets Manager, Nginx com TLS e Amazon EKS.

Frentes que estavam duplicadas foram reescritas com ângulos distintos: `Amazon EKS` (trilha × CLF-C02), `Amazon Macie` e `Amazon Cognito` (CLF-C02 × SAA-C03). Nenhum cartão foi removido.

## Padronização

Todos os 700 cards usam o **mesmo tipo de nota** (`Cloud Engineer`, ID `1830472615`): pergunta centralizada em negrito, divisor horizontal, rótulos laranjas `O QUE É` e `EXEMPLO DE USO`, com modo noturno. O modelo foi copiado do deck original de Cloud Practitioner — não foi criado tipo novo.

Identificadores curtos (ARNs, `s3:GetObject`, `0.0.0.0/0`) ficam inline. Comandos aparecem em bloco com fundo próprio, renderizado como `<pre class="codeblock"><code>`:

```text
docker ps -a
docker logs --tail 100
docker inspect
```

## Arquivos antigos

O que sobrou das versões anteriores está em `.archive/`. Não é preciso importar nada daí.

## Soft skills (arquivo separado)

`08-Soft-Skills.apkg` usa o **mesmo tipo de nota** (`Cloud Engineer`, campos
`Frente`, `Verso1`, `Verso2`), mas o deck é independente — não fica debaixo de
`Cloud Engineer`:

| Deck | Cards | Conteúdo |
|------|-------|----------|
| `Soft Skills::01-Comunicação` | 20 | daily, incidente, feedback, CNV, assertividade, dizer não, code review, comunicação de incidente técnico |
| `Soft Skills::02-Comportamento` | 7 | erro em produção, impostor, priorização, atenção, pontos fracos, diário das emoções |
| `Soft Skills::03-Entrevistas` | 17 | apresentação, STAR, falha, conflito, ponto fraco, perguntas técnicas, projeto e decisão técnica, negociação |
| `Soft Skills::04-LinkedIn e Marca Pessoal` | 15 | resumo, evidências, networking, indicação, follow-up, portfólio, resultados técnicos |

**Total: 4 decks, 59 cards.** O prefixo numérico nos nomes dos decks impõe a
ordem de estudo no Anki: comunicação → comportamento → entrevistas → LinkedIn.
Sem ele, a árvore ordenaria alfabeticamente (Comportamento, Comunicação,
Entrevista, LinkedIn). Dentro de cada deck, o campo `due` segue a ordem da lista.

O deck é **independente**: não é filho de `Cloud Engineer`. As chaves internas
dos quatro decks são 91–94 (IDs `2300000091`–`2300000094`).

Critério dos cards: **ação prática**, não estatística de pesquisa. Cada frente é
um tema curto; `Verso1` dá a regra e `Verso2` dá uma frase ou exemplo pronto.

**Migração:** os GUIDs são derivados do nome do deck + índice. Como os nomes
mudaram, os GUIDs também mudaram — antes de importar, remova o deck antigo
`08 - Soft Skills (revisado)` do Anki (faça backup do perfil antes, se houver
revisões nele). Com os nomes agora fixos, regenerações futuras sobrescrevem os
cards em vez de duplicá-los.

Para regenerar (o gerador já grava o texto final, sem necessidade de rodar a
humanização depois):

```text
cd scripts
python gerar_soft_skills.py
```

### Prática oral (fora do Anki)

O deck fixa estruturas e frases, mas não desenvolve comunicação oral, controle
emocional ou segurança em entrevista. Depois de estudar o bloco de entrevistas,
responda em voz alta a perguntas como "conte uma situação em que você cometeu um
erro técnico e assumiu a responsabilidade" e cheque a resposta com cinco pontos:

1. O contexto ficou claro?
2. Você explicou sua responsabilidade?
3. Descreveu suas ações?
4. Apresentou um resultado verdadeiro?
5. Demonstrou aprendizado?

Faça isso em ciclos curtos e periódicos; o Anki é a referência, a simulação é o
treino.

## Prompt engineering (arquivo separado)

`09-Prompt-Engineering.apkg` usa o **mesmo tipo de nota** (`Cloud Engineer`,
campos `Frente`, `Verso1`, `Verso2`) e também é independente de `Cloud Engineer`.
As chaves internas dos quatro decks são 95–98 (IDs `2300000095`–`2300000098`).

| Deck | Cards | Conteúdo |
|------|-------|----------|
| `Prompt Engineering::01-Fundamentos` | 19 | definição, prompt básico x avançado, estrutura, FECTAP como checklist, tokens, janela de contexto, custo |
| `Prompt Engineering::02-Técnicas de Prompting` | 26 | zero/one/few-shot, CoT e modelos de raciocínio, direto x guiado, roles, chaining, tool calling, iteração, casos de escolha |
| `Prompt Engineering::03-Estrutura e Controle da Resposta` | 28 | formato, JSON x Structured Outputs, validação, variáveis, tom, persona, alucinação, RAG, grounding, prompt injection |
| `Prompt Engineering::04-Aplicação Prática` | 21 | debug, revisão de código, produtividade, decisão, criatividade, biblioteca de prompts, evals e CI |

O critério dos cards é o mesmo do pacote 08: `Verso1` dá a regra e `Verso2` dá um
exemplo pronto, nunca uma pergunta.

Para regenerar:

```text
cd scripts
python gerar_prompt_engineering.py
```

## SOC N1/N2 (arquivo separado)

`SOC-N1-N2.apkg` usa o **mesmo tipo de nota** (`Cloud Engineer`, campos
`Frente`, `Verso1` = O QUE É e `Verso2` = EXEMPLO DE USO), com o CSS laranja e o
modo noturno do arquivo-base. A árvore começa em `SOC`, fora de `Cloud Engineer`,
e segue o mesmo padrão de prefixo numérico do pacote 07.

| Deck | Cards | Conteúdo |
|------|-------|----------|
| `SOC::00-Rotina e Triagem N1` | 12 | turno real: abertura da fila, priorização, triagem em cinco passos, enriquecimento, escalonamento, documentação e handoff |
| `SOC::01-Fundamentos SOC` | 21 | SOC, redes, DNS/HTTP/TLS e noções de Windows/Linux |
| `SOC::02-Logs e SIEM` | 27 | fontes e formatos de log, eventos Windows, Sysmon, EDR, PowerShell/ExecutionPolicy, iptables/pfSense, Wazuh e consultas |
| `SOC::03-Frameworks e Detecção` | 22 | MITRE ATT&CK (inclui a mudança da v18), Kill Chain, Diamond Model, STRIDE/DREAD, Pyramid of Pain, Sigma/YARA/Suricata e tuning |
| `SOC::04-Triagem e Investigação (N1)` | 59 | fluxo de triagem, phishing, malware, credenciais, rede/web, OWASP Web Top 10:2025, OWASP API Security Top 10:2023, threat intel e documentação |
| `SOC::05-Resposta a Incidentes` | 15 | ciclos NIST/SANS, contenção, erradicação, recuperação, evidências e playbooks |
| `SOC::06-N2 Investigação Aprofundada` | 28 | artefatos Windows, memória/rede, movimentação lateral, WinRM, PAM/SSH, integridade de arquivos, AD/GPO e engenharia de detecção |
| `SOC::07-Cloud para SOC` | 5 | CloudTrail, eventos AWS, GuardDuty e Entra ID no nível básico |
| `SOC::08-Automação e Consolidação` | 13 | shell/PowerShell/Python para logs e IOCs, mais cenários de entrevista N1 e N2 |
| `SOC::09-Cenários Investigativos` | 34 | triagem de autenticação e endpoint, correlação/detecção/exfiltração, cloud, N2, escalonamento e cenários web/API |

**Total: 10 decks, 236 cards** (208 de N1 e 28 de N2). Dentro de cada deck o
campo `due` segue a ordem da lista; decks com prefixo numérico garantem a ordem
de estudo na árvore.

As notas começam em `1770000000000` (passo 10) e os decks usam IDs
`2400000000`–`2400000009`, faixas separadas de 07, 08 e 09. O GUID é derivado
de `nome_antigo` + índice no deck, como no pacote 07. O gerador grava o nome
visível em `nome_antigo`, então mudar o nome do deck ou a ordem dos cards muda
os GUIDs; nesses casos, a importação deve ser limpa.

**Migração para 236 cards:** o deck `09-Cenários Investigativos` entra no fim da
árvore e não desloca os cards das etapas 00–08. Nesta versão, os dois cards
duplicados sobre condução de hunt foram unificados em um só no deck 06: os 3
cards seguintes (`baseline`, `ciclo de vida da regra` e `purple team`) mudaram de
GUID. O card sobre ATT&CK v18, a seção de OWASP API Security, a seção
investigativa de OWASP Web 2025 e os 4 cenários web/API entraram sempre no fim
do respectivo deck; nenhuma dessas inclusões desloca cards anteriores. Se você
importou a versão de 179 cards, remova o deck `SOC::06-N2 Investigação
Aprofundada` antes de reimportar para não duplicar esses 3 cards. Uma versão
intermediária do deck 09 foi gravada direto no `.apkg` sem os campos de
agendamento do deck (`lrnToday`, `newToday`, `revToday`, `timeToday`) e o Anki
recusava a importação com `JsonError`; agora o deck é gerado por `cards_soc.py`
como os demais.

**Migração para 179 cards:** os 8 cards novos entraram no meio dos decks
`02-Logs e SIEM`, `03-Frameworks e Detecção`, `04-Triagem e Investigação (N1)` e
`06-N2 Investigação Aprofundada`. Como o GUID usa o índice dentro do deck, 45
cards seguintes às inserções mudaram de GUID. Se você já importou a versão de
171 cards, remova o deck `SOC` antes de importar esta versão; senão o Anki trata
os cards deslocados como novos.

Para regenerar:

```text
cd scripts
python gerar_soc.py
```

## Importar no Anki

**Arquivo → Importar…** e selecione `07-Cloud-Engineer-Final.apkg`,
`08-Soft-Skills.apkg`, `09-Prompt-Engineering.apkg` e/ou `SOC-N1-N2.apkg`, todos
na raiz. São independentes: importar um não afeta os outros.

Os GUIDs dos 688 cartões originais foram preservados. Ainda assim, como os decks
mudaram de nome e de hierarquia, o Anki pode manter os cartões nos decks antigos.
Para ver a nova ordem, faça backup, remova os decks antigos `Cloud Engineer` (ou
use um perfil limpo) e importe o arquivo final. O que ficou em `.archive/` pode ser ignorado.

Para regenerar o pacote principal:

```text
cd scripts
python gerar_notebooks.py
```
