# Conjunto focado de decks — Cloud Engineer

`foco/` contém **um único arquivo**, `07-Notebooks.apkg`, com 94 decks e 688 cards. Ele reúne o plano de estudos, os extras que o plano não cobria, as habilidades pedidas em vagas e os dois decks de certificação.

## Arquivo único

| Grupo | Decks | Cards |
|-------|-------|-------|
| Notebooks 01–70 | 70 | 349 |
| Extras 71–80 | 10 | 71 |
| Vagas 81–86 | 6 | 40 |
| CLF-C02 + SAA-C03 | 8 | 228 |
| **Total** | **94** | **688** |

No Anki, a ordem dos decks é: `01-...` até `86-...`, depois `CLF-C02::{Conceitos, Custos, Seguranca, Servicos}` e `SAA-C03::{Custo, Performance, Resiliente, Seguro}`.

- **01–70** — um deck por notebook de `gemini-notebook.md`, na numeração exata. Estude o Notebook `XX` e revise o deck `Cloud Engineer::XX-...` no mesmo dia.
- **71–80** — extras dos decks antigos: Azure, resiliência, SLO, consistência de dados, segurança avançada, FinOps, serviços AWS, cenários de entrevista, redes e fundamentos. Os decks 71 e 77–80 levam a tag `fora-da-prova` (são para entrevista/multicloud, não para prova).
- **81–86** — Kubernetes operacional, Python/Bash, CI/CD com Jenkins/GitLab/GitOps, stack de observabilidade, segurança shift-left e GCP básico.
- **CLF-C02 e SAA-C03** — decks de prova com os cards originais mais acréscimos de alto impacto apontados pela auditoria (Security Hub, Firewall Manager, SCT, D3.8 do CLF, ingestão e custo de rede no SAA, DR nomeado etc.).

O mapa completo está em `MAPEAMENTO.md`, na raiz.

## Padronização

Todos os 688 cards usam o **mesmo tipo de nota** (`Cloud Engineer`, ID `1830472615`): pergunta centralizada em negrito, divisor horizontal, rótulos laranjas `O QUE É` e `EXEMPLO DE USO`, com modo noturno. O modelo foi copiado do deck original de Cloud Practitioner — não foi criado tipo novo.

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

Eles não precisam ser importados: seu conteúdo está no `07-Notebooks.apkg` (os cards redundantes ficaram só nessas cópias de arquivo).

## Importar no Anki

**Arquivo → Importar…** e selecione `foco/07-Notebooks.apkg`. Como os decks antigos não são importados, não há duplicatas.

Para regenerar o pacote a partir das fontes:

```text
cd scripts
python gerar_notebooks.py
```
