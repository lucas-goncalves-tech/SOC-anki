# Conjunto focado de decks — Cloud Engineer

`foco/` contém **quatro arquivos independentes**:

- `07-Cloud-Engineer-Final.apkg` — 94 decks folha e 700 cards: 688 originais + 12 lacunas pontuais, com correções adicionais e sem frentes duplicadas. É o deck principal.
- As versões original (`07-Cloud-Engineer.apkg`, 688 cards) e revisada (`07-Cloud-Engineer-Revisado.apkg`, 700 cards) foram movidas para `.archive/` e não devem ser importadas.
- `08-Soft-Skills.apkg` — 4 decks e 49 cards de soft skills aplicáveis (LinkedIn e marca pessoal, comunicação e relacionamento, comportamento e desenvolvimento, entrevista e carreira). É um pacote separado: não altera nem duplica o arquivo principal.
- `09-Prompt-Engineering.apkg` — 4 decks e 94 cards de prompt engineering (fundamentos, técnicas de prompting, estrutura e controle da resposta, aplicação prática). Também é separado.

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

## Onde ficaram os arquivos antigos

Os seis decks originais de `foco/` foram movidos para `cloud-eng/` com prefixo `foco-`, preservando conteúdo e tipo de nota:

- `cloud-eng/foco-01-CLF-C02.apkg`
- `cloud-eng/foco-02-SAA-C03.apkg`
- `cloud-eng/foco-03-Redes.apkg`
- `cloud-eng/foco-04-Entrevistas.apkg`
- `cloud-eng/foco-05-Cloud-Neutro.apkg`
- `cloud-eng/foco-06-Lacunas.apkg`

Eles não precisam ser importados: seu conteúdo está no `07-Cloud-Engineer-Revisado.apkg` (os cards redundantes ficaram só nessas cópias de arquivo).

## Soft skills (arquivo separado)

`08-Soft-Skills.apkg` usa o **mesmo tipo de nota** (`Cloud Engineer`, campos
`Frente`, `Verso1`, `Verso2`), mas o deck é independente — não fica debaixo de
`Cloud Engineer`:

| Deck | Cards | Conteúdo |
|------|-------|----------|
| `Soft Skills::LinkedIn e Marca Pessoal` | 15 | resumo, busca de vagas, indicação, postar, perfil, palavras-chave, planilha de candidaturas, laços da rede |
| `Soft Skills::Comunicação e Relacionamento` | 12 | daily, update de incidente, feedback, pedir ajuda, postmortem, risco, escuta ativa, CNV, assertividade |
| `Soft Skills::Comportamento e Desenvolvimento` | 12 | erro em produção, impostor, pedir feedback, aplicar teoria, prazo, ADR, Pareto, foco, perfis, pontos fortes |
| `Soft Skills::Entrevista e Carreira` | 10 | "conte sobre você", STAR, falha, pergunta técnica, preparação, follow-up |

O deck é **independente**: não é filho de `Cloud Engineer`. As chaves internas
dos quatro decks são 91–94 (IDs `2300000091`–`2300000094`).

Critério dos cards: **ação prática**, não estatística de pesquisa. Cada frente é
um tema curto; `Verso1` dá a regra e `Verso2` dá uma frase ou exemplo pronto.

Para regenerar:

```text
cd scripts
python gerar_soft_skills.py
```

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

## Importar no Anki

**Arquivo → Importar…** e selecione `foco/07-Cloud-Engineer-Final.apkg`,
`foco/08-Soft-Skills.apkg` e/ou `foco/09-Prompt-Engineering.apkg`. São
independentes: importar um não afeta os outros.

Os GUIDs dos 688 cartões originais foram preservados. Ainda assim, como os decks
mudaram de nome e de hierarquia, o Anki pode manter os cartões nos decks antigos.
Para ver a nova ordem, faça backup, remova os decks antigos `Cloud Engineer` (ou
use um perfil limpo) e importe o arquivo final. Os arquivos em `.archive/` não
devem ser importados.

Para regenerar o pacote principal:

```text
cd scripts
python gerar_notebooks.py
```
