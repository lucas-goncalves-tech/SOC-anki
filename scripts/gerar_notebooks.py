"""Gera foco/07-Cloud-Engineer-Final.apkg e MAPEAMENTO.md.

O tipo de nota é copiado de cloud-eng/foco-01-CLF-C02.apkg: mesmo ID
(1830472615), mesmos campos (Frente, Verso1, Verso2), mesmo CSS e mesmos
templates. O arquivo revisado contém:

- 84 decks da trilha principal, agrupados nas etapas 01-09
- 2 decks no apêndice multicloud (Azure e GCP)
- 8 decks de certificação, separados em 11-Certificações
- 700 cards: 688 originais + 12 lacunas pontuais

A ordem dos decks segue a auditoria pedagógica: fundamentos de infraestrutura,
Linux, Git, redes, fundamentos AWS, serviços AWS, IaC, containers, CI/CD,
operações, arquitetura e consolidação.
"""

import hashlib
import json
import os
import re
import sqlite3
import tempfile
import time
import zipfile
from pathlib import Path

from cards_fase0 import CARDS as FASE0
from cards_fase1 import CARDS as FASE1
from cards_fase2 import CARDS as FASE2
from cards_cert import ADICOES as ADICOES_CERT
from cards_vagas import DECKS as DECKS_VAGAS
from revisao import ADICOES, CERT_DECKS, ETAPAS, OVERRIDES_CERT, validar_ordem

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "gemini-notebook.md"
TEMPLATE = ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg"
CERT_SOURCES = (
    ROOT / "cloud-eng" / "foco-01-CLF-C02.apkg",
    ROOT / "cloud-eng" / "foco-02-SAA-C03.apkg",
)
OUTPUT = ROOT / "foco" / "07-Cloud-Engineer-Final.apkg"
MAPA = ROOT / "MAPEAMENTO.md"

CARDS = {**FASE0, **FASE1, **FASE2}

EXTRAS_TITULOS = {
    71: "Azure",
    72: "Padrões de Resiliência",
    73: "SLO, SLI e Error Budget",
    74: "Consistência e Dados",
    75: "Segurança Avançada",
    76: "FinOps",
    77: "Serviços AWS Complementares",
    78: "Cenários de Entrevista",
    79: "Redes Complementar",
    80: "Fundamentos Complementares",
}

FONTES_EXTRA = (
    "cloud-eng/foco-03-Redes.apkg",
    "cloud-eng/foco-04-Entrevistas.apkg",
    "cloud-eng/foco-05-Cloud-Neutro.apkg",
    "cloud-eng/foco-06-Lacunas.apkg",
)

# Correção encontrada na auditoria: o deck antigo dizia "6 Rs".
OVERRIDES_EXTRA = {
    "AZ-900 cobre o quê?": (
        "AZ-900 cobre o quê?",
        "Fundamentos de cloud no Azure: conceitos de nuvem, serviços principais, segurança, governança, custo e preço.",
        "É a certificação de entrada da Microsoft, equivalente ao Cloud Practitioner da AWS. É o primeiro passo para quem quer trabalhar com Azure.<br>EN: Microsoft Azure Fundamentals"),
    "O que é degradação graciosa?": (
        "O que é degradação graciosa?",
        "Manter a <b>funcionalidade crítica</b> disponível quando uma dependência falha, em vez de derrubar tudo.",
        "E-commerce sem recomendação ainda finaliza a compra; o cache serve conteúdo enquanto o banco recupera."),
    "Quais são os 6 Rs de migração para cloud?": (
        "Quais são os 7 Rs de migração para cloud?",
        "As sete estratégias são Rehost, Replatform, Repurchase, Refactor, Retire, Retain e Relocate.",
        "Relocate é mover para outra região ou infraestrutura sem mudar a aplicação, por exemplo sa-east-1 para us-east-1."),
}

# Card duplicado entre CLF-C02::Servicos e o notebook 31.
CARD_DUPLICADO = "AWS Site-to-Site VPN"

GRUPOS_ESPECIAIS = {
    71: "apendice-multicloud",
    72: "complementar",
    73: "complementar",
    74: "complementar",
    75: "complementar",
    76: "complementar",
    78: "complementar",
    80: "complementar",
    86: "apendice-multicloud",
}


def titulos_notebooks():
    texto = NOTEBOOK.read_text(encoding="utf-8")
    itens = re.findall(r"^### Notebook (\d+) — (.+)$", texto, re.M)
    return {int(numero): titulo.strip() for numero, titulo in itens}


def slug(titulo):
    return re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")


def grupo_extra(frente):
    f = frente.lower()
    if any(k in f for k in (
        "azure", "az-900", "entra id", "app service", "aks", "bicep",
        "virtual machine scale sets", "cosmos db", "key vault",
    )):
        return 71
    if any(k in f for k in ("circuit breaker", "backoff", "idempotent", "timeout", "bulkhead", "degradação graciosa")):
        return 72
    if any(k in f for k in ("sli", "slo", "error budget")):
        return 73
    if any(k in f for k in ("teorema cap", "consistência", "sql e nosql", "leader/follower")):
        return 74
    if any(k in f for k in ("zero trust", "stride", "envelope encryption")):
        return 75
    if any(k in f for k in ("unit economics", "showback", "chargeback", "anomalia de custo")):
        return 76
    if f.startswith("cenário:"):
        return 78
    if any(k in f for k in ("nginx", "dnsmasq")):
        return 79
    if any(k in f for k in ("sla", "vendor lock-in")):
        return 80
    if any(k in f for k in (
        "6 rs", "landing zone", "crr", "x-ray", "boto3", "step functions",
        "session manager", "parameter store", "elastic beanstalk", "cdk",
        "cognito", "elastic ip", "api gateway", "elasticache",
        "transit gateway", "site-to-site", "ebs, efs", "aurora",
    )):
        return 77
    return None


def carregar_extras():
    extras = {numero: [] for numero in EXTRAS_TITULOS}
    for nome in FONTES_EXTRA:
        with zipfile.ZipFile(ROOT / nome) as arquivo:
            dados = arquivo.read("collection.anki2")
        fd, tmp = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        with open(tmp, "wb") as arquivo:
            arquivo.write(dados)
        con = sqlite3.connect(tmp)
        for (flds,) in con.execute("select flds from notes order by id"):
            campos = tuple(flds.split("\x1f"))
            if len(campos) != 3:
                raise SystemExit("Card com campos inesperados em %s" % nome)
            grupo = grupo_extra(campos[0])
            if grupo is not None:
                extras[grupo].append(OVERRIDES_EXTRA.get(campos[0], campos))
        con.close()
        os.remove(tmp)
    vazios = [numero for numero, cartoes in extras.items() if not cartoes]
    if vazios:
        raise SystemExit("Grupos de extras vazios: %s" % vazios)
    return extras


def carregar_certificacao():
    decks = {}
    for caminho in CERT_SOURCES:
        with zipfile.ZipFile(caminho) as arquivo:
            dados = arquivo.read("collection.anki2")
        fd, tmp = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        with open(tmp, "wb") as arquivo:
            arquivo.write(dados)
        con = sqlite3.connect(tmp)
        nomes = json.loads(con.execute("select decks from col").fetchone()[0])
        for did, flds in con.execute(
            "select c.did, n.flds from cards c join notes n on c.nid=n.id"
        ):
            nome = nomes[str(did)]["name"]
            campos = tuple(flds.split("\x1f"))
            if len(campos) != 3:
                raise SystemExit("Card com campos inesperados em %s" % caminho)
            if campos[0] == CARD_DUPLICADO:
                continue
            decks.setdefault(nome, []).append(campos)
        con.close()
        os.remove(tmp)

    for nome, cartoes in ADICOES_CERT.items():
        decks.setdefault(nome, []).extend(cartoes)

    for (nome, frente), novo in OVERRIDES_CERT.items():
        cartoes = decks.get(nome)
        if cartoes is None:
            raise SystemExit("Deck de certificação ausente: %s" % nome)
        for indice, cartao in enumerate(cartoes):
            if cartao[0] == frente:
                cartoes[indice] = novo
                break
        else:
            raise SystemExit("Cartão não encontrado em %s: %s" % (nome, frente))

    faltando = [antigo for antigo, *_ in CERT_DECKS if antigo not in decks]
    if faltando:
        raise SystemExit("Decks de certificação sem conteúdo: %s" % faltando)
    return decks


def validar(titulos):
    if set(titulos) != set(CARDS):
        raise SystemExit(
            "Notebooks sem cards ou cards sem notebook: %s / %s"
            % (sorted(set(titulos) - set(CARDS)), sorted(set(CARDS) - set(titulos)))
        )
    total = 0
    for numero, cartoes in sorted(CARDS.items()):
        if not cartoes:
            raise SystemExit("Notebook %02d sem cards" % numero)
        for cartao in cartoes:
            if len(cartao) != 3 or not all(isinstance(c, str) and c.strip() for c in cartao):
                raise SystemExit("Card inválido no notebook %02d: %r" % (numero, cartao))
            if "\x1f" in "".join(cartao):
                raise SystemExit("Card com separador de campo no notebook %02d" % numero)
        total += len(cartoes)
    return total


def ler_modelo():
    with zipfile.ZipFile(TEMPLATE) as arquivo:
        colecao = arquivo.read("collection.anki2")
        outros = {
            nome: arquivo.read(nome)
            for nome in arquivo.namelist()
            if nome != "collection.anki2"
        }
    fd, caminho = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    with open(caminho, "wb") as arquivo:
        arquivo.write(colecao)
    return caminho, outros


def gerar(decks):
    caminho, outros = ler_modelo()
    con = sqlite3.connect(caminho)
    conf, models, decks_json, dconf, tags = con.execute(
        "select conf, models, decks, dconf, tags from col"
    ).fetchone()

    modelo = next(iter(json.loads(models).values()))
    if modelo["name"] != "Cloud Engineer" or [f["name"] for f in modelo["flds"]] != [
        "Frente", "Verso1", "Verso2"
    ]:
        raise SystemExit("O modelo do arquivo-base não é o esperado")

    deck_base = next(v for k, v in json.loads(decks_json).items() if k != "1")
    now = int(time.time())
    novos_decks = {"1": json.loads(decks_json)["1"]}

    con.execute("delete from notes")
    con.execute("delete from cards")
    con.execute("delete from revlog")
    con.execute("delete from graves")

    base_id = 1700000000000
    posicao = 0
    for deck in decks:
        meta = dict(deck_base)
        meta.update({"id": deck["id"], "name": deck["nome"], "usn": -1, "mod": now})
        novos_decks[str(deck["id"])] = meta
        tag = deck["tag"]
        for indice, (frente, verso1, verso2) in enumerate(deck["cartoes"], start=1):
            nota_id = base_id + posicao * 10
            # GUID calculado com o nome antigo e o índice original: uma
            # reimportação atualiza os cartões existentes em vez de duplicá-los.
            guid = hashlib.md5(("%s-%02d" % (deck["nome_antigo"], indice)).encode()).hexdigest()[:12]
            con.execute(
                "insert into notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) "
                "values (?,?,?,?,?,?,?,?,?,?,?)",
                (nota_id, guid, modelo["id"], now, -1, " %s " % tag,
                 "\x1f".join((frente, verso1, verso2)), frente, 0, 0, ""),
            )
            con.execute(
                "insert into cards (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, "
                "reps, lapses, left, odue, odid, flags, data) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (nota_id + 1, nota_id, deck["id"], 0, now, -1, 0, 0, posicao,
                 0, 0, 0, 0, 0, 0, 0, 0, ""),
            )
            posicao += 1

    con.execute(
        "update col set mod=?, scm=?, ls=?, conf=?, models=?, decks=?, dconf=?, tags=?",
        (now, now, now, conf, json.dumps({str(modelo["id"]): modelo}, ensure_ascii=False),
         json.dumps(novos_decks, ensure_ascii=False), dconf, tags),
    )
    con.commit()
    con.close()

    with open(caminho, "rb") as arquivo:
        colecao_nova = arquivo.read()
    os.remove(caminho)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as arquivo:
        arquivo.writestr("collection.anki2", colecao_nova)
        for nome, dados in outros.items():
            arquivo.writestr(nome, dados)
    return posicao


SECAO_SOFT_SKILLS = """## Pacote 08 — soft skills

Arquivo separado: `foco/08-Soft-Skills.apkg`. Usa o mesmo tipo de nota, mas o deck é
independente (não fica debaixo de `Cloud Engineer`).

| Deck | Cards |
|------|-------|
| `Soft Skills::LinkedIn e Marca Pessoal` | 15 |
| `Soft Skills::Comunicação e Relacionamento` | 12 |
| `Soft Skills::Comportamento e Desenvolvimento` | 12 |
| `Soft Skills::Entrevista e Carreira` | 10 |

**Total: 4 decks, 49 cards.**"""

SECAO_PROMPT = """## Pacote 09 - prompt engineering

Arquivo separado: `foco/09-Prompt-Engineering.apkg`. Usa o mesmo tipo de nota, mas o deck é
independente (não fica debaixo de `Cloud Engineer`).

| Deck | Cards | Conteúdo |
|------|-------|----------|
| `Prompt Engineering::01-Fundamentos` | 19 | definição, estrutura, FECTAP como checklist, tokens, janela de contexto, custo e conversa por assunto |
| `Prompt Engineering::02-Técnicas de Prompting` | 26 | zero/one/few-shot, CoT e modelos de raciocínio, direto x guiado, roles, chaining, tool calling, iteração, casos de escolha |
| `Prompt Engineering::03-Estrutura e Controle da Resposta` | 28 | formato, JSON x Structured Outputs, validação, variáveis, tom, persona, alucinação, RAG, grounding, injection |
| `Prompt Engineering::04-Aplicação Prática` | 21 | debug, revisão de código, produtividade, decisão, criatividade, biblioteca, evals e CI |

**Total: 4 decks, 94 cards.**"""


def escrever_mapa(titulos, decks):
    principais = [d for d in decks if d["numero"] is not None and d["numero"] not in (71, 86)]
    apendice = [d for d in decks if d["numero"] in (71, 86)]
    certificacoes = [d for d in decks if d["numero"] is None]
    total = sum(len(d["cartoes"]) for d in decks)

    linhas = [
        "# MAPEAMENTO — trilha revisada",
        "",
        "Arquivo final: `foco/07-Cloud-Engineer-Final.apkg`.",
        "Modelo `Cloud Engineer` (campos `Frente`, `Verso1` = O QUE É e `Verso2` = EXEMPLO DE USO).",
        "",
        "As versões original (688 cards) e revisada (700 cards) foram arquivadas em `.archive/`.",
        "",
        "**Como usar:** siga as etapas de 01 a 09 na ordem. As certificações ficam por último",
        "e não fazem parte da trilha principal. O apêndice multicloud (Azure e GCP) é opcional.",
        "",
        "| Grupo | Decks | Cards |",
        "|-------|-------|-------|",
        "| Etapas 01–09 | %d | %d |" % (
            len(principais), sum(len(d["cartoes"]) for d in principais)),
        "| Apêndice multicloud | %d | %d |" % (
            len(apendice), sum(len(d["cartoes"]) for d in apendice)),
        "| Certificações | %d | %d |" % (
            len(certificacoes), sum(len(d["cartoes"]) for d in certificacoes)),
        "| **Total** | **%d** | **%d** |" % (len(decks), total),
        "",
        "## Etapas da trilha principal",
        "",
    ]

    for etapa, numeros in ETAPAS:
        etapa_decks = [d for d in decks if d["etapa"] == etapa]
        linhas += [
            "### %s" % etapa,
            "",
            "| Ordem | Deck | Origem | Cards |",
            "|-------|------|--------|-------|",
        ]
        for deck in etapa_decks:
            linhas.append("| %02d | `%s` | %s | %d |" % (
                deck["posicao"], deck["nome"], deck["origem"], len(deck["cartoes"])))
        linhas += [
            "",
            "**Total da etapa: %d decks, %d cards.**" % (
                len(etapa_decks), sum(len(d["cartoes"]) for d in etapa_decks)),
            "",
        ]

    linhas += [
        "## Certificações",
        "",
        "Separadas da trilha principal. Estude depois de consolidar AWS, Linux, redes e IaC;",
        "use os decks para revisar e identificar lacunas, não como primeiro contato com o assunto.",
        "",
        "### CLF-C02 — ordem recomendada",
        "",
        "Conceitos → Segurança → Serviços → Custos.",
        "",
        "### SAA-C03 — ordem recomendada",
        "",
        "Seguro → Resiliente → Performance → Custo (30%, 26%, 24% e 20% do exame).",
        "",
        "| Certificação | Ordem | Deck | Cards |",
        "|--------------|-------|------|-------|",
    ]
    for deck in certificacoes:
        linhas.append("| %s | %02d | `%s` | %d |" % (
            deck["cert"], deck["ordem_cert"], deck["nome"], len(deck["cartoes"])))

    linhas += [
        "",
        "## Correções desta revisão",
        "",
        "- Cloud Computing: virtualização tratada como um habilitador, não como origem única.",
        "- Private Cloud: separação entre propriedade, hospedagem e controle operacional.",
        "- Multicloud: redução de lock-in como possibilidade, não como garantia.",
        "- CIDR: fórmula 2^h - 2 com exceções /31 e /32.",
        "- DNS: resolução recursiva x iterativa, caches por TTL e cache negativo.",
        "- Docker Networking: DNS por nome apenas em bridge definida pelo usuário.",
        "- Terraform State: valores sensíveis, backend protegido, locking, versionamento e recuperação.",
        "- NAT Gateway: separado de VPC Endpoints para acesso a serviços AWS.",
        "- ACM: certificados para CloudFront obrigatoriamente em us-east-1.",
        "- Lambda: timeout, memória, concorrência e modelo efêmero.",
        "- RDS Multi-AZ: distinção entre Multi-AZ DB instance e Multi-AZ DB cluster.",
        "- EC2 Instance Store: perda em stop, hibernate e terminate; reboot não apaga.",
        "- Kubernetes Secrets: base64 não é criptografia; RBAC por recurso e encryption at rest protegem camadas distintas.",
        "- IAM OIDC: trust policy valida aud e sub, não apenas a origem do token.",
        "- AWS WAF: AWS Managed Rules, rate-based rules e associação obrigatória ao recurso.",
        "- EKS: control plane gerenciado, data plane e add-ons separados.",
        "- AWS Systems Manager: SSM Agent, conectividade e IAM como requisitos operacionais.",
        "- GitHub Actions: deploy por OIDC no lugar de access key estática.",
        "- Frentes repetidas (EKS, Macie e Cognito) reescritas com ângulos distintos.",
        "",
        "## Lacunas acrescentadas",
        "",
        "- Troubleshooting avançado de Linux (15).",
        "- DHCP e ARP (16).",
        "- IPv6 operacional (17).",
        "- DNS na prática: diagnóstico e propagação (20).",
        "- IAM OIDC para pipelines (27).",
        "- AWS KMS, AWS Config e AWS WAF (75).",
        "- AWS Systems Manager e AWS Secrets Manager (77).",
        "- Nginx com TLS e virtual hosts (79).",
        "- Amazon EKS (81).",
        "",
        SECAO_SOFT_SKILLS,
        "",
        SECAO_PROMPT,
        "",
        "## Afinidade entre assuntos",
        "",
        "Git (06) com CI/CD (58–59); Dockerfile (53) com Compose (56); redes (16–23) com VPC (28–31);",
        "DNS (20) com Route 53 (40); IAM (26–27) com CloudTrail (62); Terraform (46–51) com Git (06);",
        "CloudWatch (60–61) com troubleshooting (63–64); Kubernetes (81) com Docker (52–57).",
        "",
    ]
    MAPA.write_text("\n".join(linhas), encoding="utf-8")


def montar_deck(numero, etapa, posicao, titulo, cartoes, origem):
    nome_antigo = "Cloud Engineer::%02d-%s" % (numero, titulo)
    grupo = GRUPOS_ESPECIAIS.get(numero, "trilha-principal")
    tag = "cloud-engineer %s etapa%02d ordem%02d nb%02d_%s" % (
        grupo, int(etapa[:2]), posicao, numero, slug(titulo))
    return {
        "id": 2100000000 + numero,
        "nome": "Cloud Engineer::%s::%02d-%s" % (etapa, posicao, titulo),
        "nome_antigo": nome_antigo,
        "tag": tag,
        "cartoes": cartoes,
        "numero": numero,
        "etapa": etapa,
        "posicao": posicao,
        "origem": origem,
        "cert": None,
    }


def main():
    titulos = titulos_notebooks()
    validar(titulos)
    validar_ordem()

    extras = carregar_extras()
    certificacao = carregar_certificacao()

    titulos_extras = dict(EXTRAS_TITULOS)
    titulos_vagas = {numero: titulo for numero, (titulo, _) in DECKS_VAGAS.items()}
    todos = {**titulos, **titulos_extras, **titulos_vagas}
    if set(todos) != set(range(1, 87)):
        raise SystemExit("Títulos ausentes ou sobrando: %s" % (
            sorted(set(range(1, 87)) ^ set(todos)),))

    decks = []
    for etapa_idx, (etapa, numeros) in enumerate(ETAPAS, start=1):
        for posicao, numero in enumerate(numeros, start=1):
            if numero in CARDS:
                cartoes = list(CARDS[numero])
                origem = "nb %02d" % numero
            elif numero in extras:
                cartoes = list(extras[numero])
                origem = "extra %02d" % numero
            else:
                cartoes = list(DECKS_VAGAS[numero][1])
                origem = "vaga %02d" % numero
            cartoes += list(ADICOES.get(numero, []))
            decks.append(montar_deck(
                numero, etapa, posicao, todos[numero], cartoes, origem))

    for posicao, (antigo, cert, sufixo, deck_id) in enumerate(CERT_DECKS, start=1):
        cartoes = list(certificacao[antigo])
        decks.append({
            "id": deck_id,
            "nome": "Cloud Engineer::11-Certificações::%s::%s" % (cert, sufixo),
            "nome_antigo": antigo,
            "tag": "cloud-engineer certificacao cert_%s_%s" % (
                cert.lower().replace("-", "_"), slug(sufixo)),
            "cartoes": cartoes,
            "numero": None,
            "etapa": "11-Certificações",
            "posicao": posicao,
            "ordem_cert": int(sufixo[:2]),
            "origem": "certificação",
            "cert": cert,
        })

    total = sum(len(deck["cartoes"]) for deck in decks)
    gerados = gerar(decks)
    if gerados != total:
        raise SystemExit("Contagem divergente: %d != %d" % (gerados, total))
    escrever_mapa(titulos, decks)

    profissionais = [d for d in decks if d["numero"] is not None]
    certs = [d for d in decks if d["numero"] is None]
    print("OK: %d decks, %d cards" % (len(decks), total))
    print("Trilha profissional: %d decks, %d cards" % (
        len(profissionais), sum(len(d["cartoes"]) for d in profissionais)))
    print("Certificações: %d decks, %d cards" % (
        len(certs), sum(len(d["cartoes"]) for d in certs)))
    print("Apkg:", OUTPUT)
    print("Mapa:", MAPA)


if __name__ == "__main__":
    main()
