# Reorganização e revisão do deck Cloud Engineer.
#
# ETAPAS define a ordem pedagógica. Cada número é o deck original do pacote
# 07-Cloud-Engineer.apkg (01-86). A ordem dentro da etapa é a ordem de estudo.
#
# ADICOES acrescenta cartões pontuais para lacunas identificadas na auditoria.
# OVERRIDES_CERT corrige cartões que vêm dos arquivos de certificação originais.

ETAPAS = [
    ("01-Fundamentos de Infraestrutura", [
        1, 2, 3, 4, 5,
        7, 8, 9, 10, 11, 12, 13, 14, 15,
        6,
        16, 17, 18, 19, 20, 21, 22, 23,
        79,
    ]),
    ("02-Fundamentos AWS", [
        24, 25, 26, 27, 28, 29, 30, 31,
    ]),
    ("03-Serviços AWS", [
        32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 77,
    ]),
    ("04-Infraestrutura como Código", [
        46, 47, 48, 49, 50, 51, 82,
    ]),
    ("05-Containers e Orquestração", [
        52, 53, 54, 55, 56, 57, 81,
    ]),
    ("06-CI-CD e Segurança de Desenvolvimento", [
        58, 59, 83, 85,
    ]),
    ("07-Operações e Observabilidade", [
        60, 61, 62, 84, 63, 64, 72, 73,
    ]),
    ("08-Arquitetura e Produção", [
        65, 66, 74, 75, 67, 76, 68, 69, 80,
    ]),
    ("09-Consolidação", [
        78, 70,
    ]),
    ("10-Apêndice Multicloud", [
        71, 86,
    ]),
]

# Cartões novos, sempre anexados ao fim do deck para preservar os GUIDs
# existentes e permitir que uma reimportação atualize os cartões já estudados.
# Os decks 15, 16, 17, 20 e 27 recebem os novos cartões diretamente nos módulos
# cards_fase0.py e cards_fase1.py; aqui ficam apenas os decks carregados de
# arquivos .apkg antigos ou de cards_vagas.py.
ADICOES = {
    75: [
        ("O que é AWS KMS?",
         "Serviço gerenciado de chaves usado para criptografia em repouso e envelope encryption; integra com S3, EBS, RDS e Secrets Manager, com políticas de chave, auditoria e rotação.",
         "Chave KMS por ambiente; o S3 usa SSE-KMS e a aplicação descriptografa via role, sem acesso à chave mestra."),
        ("O que é AWS Config?",
         "Registra configurações e mudanças de recursos e avalia regras de conformidade, como bucket público ou Security Group aberto. Não bloqueia a ação por si só; alerta e pode disparar remediação automática.",
         "Regra do Config detecta bucket público e aciona uma automação do Systems Manager para corrigir."),
        ("O que é AWS WAF?",
         "Firewall de camada 7 que inspeciona HTTP/HTTPS. Uma Web ACL combina AWS Managed Rules (SQLi, XSS, bots), regras customizadas e rate-based rules por IP; ela só atua quando associada a um ALB, CloudFront ou API Gateway.",
         "Web ACL associada a uma distribuição CloudFront, com AWS Managed Rules e rate-based rule de 2.000 requisições por 5 minutos por IP."),
    ],
    77: [
        ("O que é o AWS Systems Manager?",
         "Conjunto de ferramentas de operação: Session Manager, Run Command, Patch Manager, Parameter Store e Inventory. O SSM Agent precisa estar instalado e rodando na instância, com conectividade de saída para os endpoints do serviço; o acesso é controlado por IAM e registrado no CloudTrail.",
         "Instância privada com SSM Agent e VPC Endpoint para SSM; acesso via Session Manager sem bastion e patches aplicados pelo Patch Manager."),
        ("O que é o AWS Secrets Manager?",
         "Armazena e rotaciona segredos como senhas, tokens e chaves de API, com acesso por IAM, auditoria no CloudTrail e rotação nativa para RDS, Redshift e DocumentDB.",
         "Senha do RDS rotacionada automaticamente a cada 30 dias e lida pela aplicação via SDK."),
    ],
    79: [
        ("Nginx com TLS e virtual hosts",
         "Cada virtual host é um bloco server com server_name; para HTTPS, ouça na 443, informe ssl_certificate e ssl_certificate_key e redirecione a porta 80 para 443. Valide com nginx -t antes do reload.",
         "server { listen 443 ssl; server_name app.exemplo.com; ssl_certificate /etc/letsencrypt/live/app/fullchain.pem; ssl_certificate_key /etc/letsencrypt/live/app/privkey.pem; location / { proxy_pass http://127.0.0.1:8080; } }"),
    ],
    81: [
        ("Amazon EKS",
         "Kubernetes gerenciado na AWS: o control plane (API server, etcd e scheduler) é operado pela AWS e não fica visível para o usuário; o data plane são os nodes EC2 ou Fargate onde os pods rodam; add-ons como CoreDNS, VPC CNI e metrics server são componentes que você gerencia e atualiza.",
         "Cluster EKS com node group gerenciado, VPC CNI e CoreDNS como add-ons, e IRSA (IAM Roles for Service Accounts) para conceder permissões AWS aos pods."),
    ],
}

# Chave: (nome antigo do deck no pacote de certificação, frente do cartão).
OVERRIDES_CERT = {
    ("Cloud Engineer::SAA-C03::Resiliente",
     "RDS Multi-AZ vs Read Replica — diferença principal?"): (
        "RDS Multi-AZ vs Read Replica — diferença principal?",
        "Multi-AZ DB instance: standby síncrono, sem leitura e com failover automático. Multi-AZ DB cluster: três instâncias em três AZs, duas legíveis e failover mais rápido. Read Replica: réplica assíncrona para escala de leitura, sem failover automático.",
        "Use Multi-AZ DB cluster quando precisa de HA e leitura; read replica para relatórios e cargas analíticas."),
    ("Cloud Engineer::CLF-C02::Servicos", "Instance Store"): (
        "Instance Store",
        "Armazenamento em bloco efêmero local, perdido quando a instância é parada, hibernada ou terminada; um reboot não apaga. Indicado para cache e dados temporários.",
        "Usar Instance Store para cache e arquivos temporários, nunca para dados persistentes."),
    ("Cloud Engineer::CLF-C02::Seguranca", "AWS WAF (Web Application Firewall)"): (
        "AWS WAF — regras e associação",
        "Filtra HTTP/HTTPS com uma Web ACL que combina AWS Managed Rules, regras customizadas e rate-based rules por IP. A ACL só protege depois de associada a um ALB, CloudFront ou API Gateway.",
        "Proteger uma distribuição CloudFront com AWS Managed Rules contra SQLi e uma rate-based rule de 2.000 requisições por 5 minutos por IP."),
    ("Cloud Engineer::CLF-C02::Servicos", "Amazon EKS"): (
        "O que o CLF-C02 espera saber sobre EKS?",
        "EKS é o Kubernetes gerenciado da AWS: o control plane é operado pela AWS e o data plane são os nodes EC2 ou Fargate. Para o CLF-C02, basta reconhecer o serviço e essa divisão de responsabilidades.",
        "Uma empresa leva manifestos Kubernetes existentes para o EKS sem operar o API server ou o etcd."),
    ("Cloud Engineer::CLF-C02::Servicos", "AWS Systems Manager"): (
        "AWS Systems Manager — visão para o CLF-C02",
        "Ferramenta de operação em escala: Session Manager substitui o SSH, Run Command executa comandos remotos e Patch Manager aplica patches. O SSM Agent precisa estar ativo na instância e o acesso é controlado por IAM.",
        "Acessar uma EC2 pelo Session Manager sem abrir a porta 22 e sem bastion."),
    ("Cloud Engineer::SAA-C03::Seguro", "Amazon Macie"): (
        "Macie em uma arquitetura SAA-C03",
        "Em um cenário de exame, use Macie para descobrir e classificar dados sensíveis em S3 e acionar remediação; ele é complementar a S3 Block Public Access, KMS e Inspector.",
        "Bucket corporativo com CPFs: Macie classifica os objetos e dispara uma lambda de remediação."),
    ("Cloud Engineer::SAA-C03::Seguro", "Amazon Cognito"): (
        "Cognito na arquitetura: user pool x identity pool",
        "User pool cuida de cadastro e login de usuários; identity pool troca identidades autenticadas ou anônimas por credenciais AWS temporárias via role — sem chaves permanentes na aplicação.",
        "App web autentica no Cognito e usa o identity pool para assumir uma role com acesso limitado a um bucket S3."),
}

# Ordem dos decks de certificação e IDs internos preservados do pacote original.
# (nome antigo, certificação, sufixo novo, deck_id)
CERT_DECKS = [
    ("Cloud Engineer::CLF-C02::Conceitos", "CLF-C02", "01-Conceitos", 2200000001),
    ("Cloud Engineer::CLF-C02::Seguranca", "CLF-C02", "02-Segurança", 2200000003),
    ("Cloud Engineer::CLF-C02::Servicos", "CLF-C02", "03-Serviços", 2200000004),
    ("Cloud Engineer::CLF-C02::Custos", "CLF-C02", "04-Custos", 2200000002),
    ("Cloud Engineer::SAA-C03::Seguro", "SAA-C03", "01-Seguro", 2200000008),
    ("Cloud Engineer::SAA-C03::Resiliente", "SAA-C03", "02-Resiliente", 2200000007),
    ("Cloud Engineer::SAA-C03::Performance", "SAA-C03", "03-Performance", 2200000006),
    ("Cloud Engineer::SAA-C03::Custo", "SAA-C03", "04-Custo", 2200000005),
]


def validar_ordem():
    vistos = [numero for _, numeros in ETAPAS for numero in numeros]
    if sorted(vistos) != list(range(1, 87)):
        faltando = sorted(set(range(1, 87)) - set(vistos))
        repetidos = sorted({n for n in vistos if vistos.count(n) > 1})
        raise SystemExit(
            "Ordem das etapas inválida. Faltando: %s; repetidos: %s"
            % (faltando, repetidos)
        )
