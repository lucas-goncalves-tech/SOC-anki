# Conjunto focado de decks — Cloud Engineer

Conjunto enxuto para revisão: **289 cards em 5 decks**, todos filhos do único deck pai `Cloud Engineer`. O que é fácil de praticar (Linux, Git, Bash, Docker, Terraform, K8s, observabilidade, segurança) ficou de fora; a profundidade dos cards foi mantida, o que mudou foi o escopo.

## Arquivos

| Arquivo | Cards | Conteúdo |
|---------|-------|----------|
| `01-CLF-C02.apkg` | 105 | AWS Cloud Practitioner (4 subdecks) |
| `02-SAA-C03.apkg` | 50 | AWS Solutions Architect – Associate (4 subdecks) |
| `03-Redes.apkg` | 28 | Redes |
| `04-Entrevistas.apkg` | 96 | Entrevistas |
| `05-Cloud-Neutro.apkg` | 20 | Fundamentos de cloud vendor-neutral |

Hierarquia no Anki:

```
Cloud Engineer
├── CLF-C02
│   ├── Conceitos
│   ├── Seguranca
│   ├── Servicos
│   └── Custos
├── SAA-C03
│   ├── Seguro
│   ├── Resiliente
│   ├── Performance
│   └── Custo
├── Redes
├── Entrevistas
└── Cloud Neutro
```

## Padronização

Todos os 289 cards usam o **mesmo tipo de nota** (`Cloud Engineer`, ID `1830472615`) e o mesmo visual: pergunta centralizada em negrito, divisor horizontal, rótulos laranjas `O QUE É` e `EXEMPLO DE USO`, com modo noturno. Não há mais decks com modelos diferentes.

Nomes curtos: `PAI::CERTIFICADO::DOMÍNIO` (ex.: `Cloud Engineer::SAA-C03::Seguro`).

## Comandos

Identificadores curtos (ARNs, `s3:GetObject`, `0.0.0.0/0`) ficam inline. Quando o card **exige um comando**, ele aparece em um bloco cercado com fundo próprio — equivalente visual ao `` ``` `` do Markdown (os campos do Anki são HTML, então o bloco é renderizado como `<pre class="codeblock"><code>`):

```text
docker ps -a
docker logs --tail 100
docker inspect
```

Cards de diagnóstico e entrevista (processos, portas, disco, systemd, SSH, Docker, Terraform, AWS CLI) foram reescritos com esse padrão.

## Próximo nível da certificação AWS

Após o Cloud Practitioner (CLF-C02), o próximo passo para cloud engineer é **AWS Certified Solutions Architect – Associate (SAA-C03)** — o Associate mais reconhecido, com prova de 65 questões/130 min, US$ 150 e validade de 3 anos. Seus domínios (30% seguro, 26% resiliente, 24% performance, 20% custo) definem os quatro subdecks do arquivo 02.

Fontes: [AWS – Solutions Architect Associate](https://aws.amazon.com/certification/certified-solutions-architect-associate/) e [guias de prova](https://docs.aws.amazon.com/aws-certification/latest/examguides/aws-certification-exam-guides.html).

O deck `05-Cloud-Neutro` cobre os mesmos fundamentos do Practitioner de forma independente de vendor (IaaS/PaaS/SaaS, responsabilidade compartilhada, AZ/Região, escala, SLA, RTO/RPO, CDN, CapEx/OpEx, lock-in, IaC), para não depender só da AWS.

## Importar no Anki

**Arquivo → Importar…** e selecione os `.apkg`. Como você apagou o deck antigo para começar do zero, importe os cinco sem receio de duplicatas.

> Os arquivos originais continuam intactos em `AWS/` e `cloud-eng/`; o que está em `foco/` são versões regeradas e padronizadas.
