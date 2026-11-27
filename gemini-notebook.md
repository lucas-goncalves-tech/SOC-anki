# Plano de estudos — SOC N1 e N2

Reorganizado em 26/11/2026 a partir de levantamento de vagas de SOC N1 e N2 (Brasil e remoto, 2024–2026), discussões em fóruns (r/cybersecurity, r/SecurityCareerAdvice, Hacker News) e fontes oficiais (MITRE ATT&CK v20, NIST SP 800-61r3, NIST CSF 2.0, CompTIA, Microsoft, SigmaHQ).

**Como usar:** a ordem dos notebooks é a ordem de estudo. Os notebooks 01–16 são a base do N1; 17–21 cobrem frameworks e detecção; 22–28 aprofundam o N2; 29–32 fecham com certificação, prática de laboratório e entrevista. O índice antigo, do pacote Cloud, ficou preservado em `.archive/gemini-notebook-cloud.md`.

### Notebook 01 — Networking Fundamentals for SOC
- **Objetivo:** Entender TCP/IP para interpretar qualquer alerta sem depender de decorar a ferramenta do momento.
- **Estrutura do Conteúdo:**
  1. Modelo OSI e TCP/IP, encapsulamento e endereços MAC e IP.
  2. TCP versus UDP, handshake, flags SYN, ACK, FIN e RST, e portas críticas (22, 53, 80, 443, 88, 389, 445, 3389).
  3. CIDR, subnetting, default gateway, NAT e VLAN no contexto de investigação.
  4. DNS, HTTP, TLS, LDAP e Kerberos como protocolos observáveis em log.
  5. Leitura de pcap no Wireshark: conversas, fluxos e anomalias.
  6. O que firewall, proxy, WAF e IDS/IPS registram.

### Notebook 02 — DNS, HTTP and TLS for Analysts
- **Objetivo:** Reconhecer padrões maliciosos em consultas DNS e requisições web.
- **Estrutura do Conteúdo:**
  1. Registros A, AAAA, CNAME, MX, NS e TXT com SPF, DKIM e DMARC.
  2. DGA, fast flux, TTL muito baixo e tunelamento DNS.
  3. Métodos e códigos de status HTTP no access.log; User-Agent e Referer como pista.
  4. TLS handshake, emissor e validade do certificado; certificado autoassinado como indicador.
  5. Consulta de reputação de domínio e URL em VirusTotal e urlscan.

### Notebook 03 — Linux Essentials for SOC
- **Objetivo:** Investigar hosts Linux com comandos nativos e conhecer a telemetria disponível.
- **Estrutura do Conteúdo:**
  1. Shell, navegação, permissões, usuários, sudo e UID/GID.
  2. Processos, threads, ps, top, árvore de processos e sinais.
  3. `/var/log/auth.log`, `/var/log/secure`, journalctl e dmesg.
  4. cron, systemd e persistência em Linux.
  5. auditd, integridade de arquivos e shell history.
  6. Comandos de rede: ss, netstat, curl e tcpdump.

### Notebook 04 — Windows Essentials for SOC
- **Objetivo:** Entender a estrutura do Windows e do Active Directory para saber onde a evidência aparece.
- **Estrutura do Conteúdo:**
  1. Usuários, grupos, UAC, privilégios e Registry.
  2. Árvore de processos: smss, csrss, wininit, services, lsass e svchost.
  3. Serviços, tarefas agendadas, pasta Startup e chaves Run/RunOnce.
  4. PowerShell, ExecutionPolicy e logging de script block.
  5. Noções de AD: domínio, DC, grupos, políticas e Kerberos.

### Notebook 05 — Windows Event IDs and Sysmon
- **Objetivo:** Ler os eventos que sustentam a triagem e a investigação de endpoint Windows.
- **Estrutura do Conteúdo:**
  1. Segurança: 4624 e 4625, Logon Types 2, 3 e 10, substatus 0xC0000064 versus 0xC000006A.
  2. 4688 e 4689 com linha de comando; 4648, 4672, 4698, 4720, 4732, 7045 e 1102.
  3. Kerberos no DC: 4768, 4769 e 4776.
  4. PowerShell 4104 e Task Scheduler 106, 200 e 201.
  5. Sysmon IDs 1, 3, 7, 8, 10, 11, 13 e 22.
  6. Correlação temporal entre logon, criação de processo e conexão de rede.

### Notebook 06 — Logs, Timestamps and Normalization
- **Objetivo:** Tornar logs de fontes diferentes comparáveis e confiáveis na linha do tempo.
- **Estrutura do Conteúdo:**
  1. Fontes: endpoint, rede, identidade, aplicação e cloud.
  2. Syslog, CEF e JSON; facility e severidade.
  3. Normalização de campos com ECS e ASIM para consultas e regras reutilizáveis.
  4. NTP, UTC e alinhamento de timestamps entre hosts.
  5. Retenção, envio centralizado e evento 1102 como tentativa de apagar rastros.

### Notebook 07 — SOC Fundamentals and Analyst Tiers
- **Objetivo:** Entender a missão do SOC e onde o N1 termina e o N2 começa.
- **Estrutura do Conteúdo:**
  1. SOC versus NOC versus CSIRT e o fluxo monitorar, triar, escalar e documentar.
  2. N1, N2 e N3: responsabilidades, on-call e critérios de escalonamento.
  3. Evento, alerta, incidente e caso; severidade versus prioridade.
  4. Tríade CIA aplicada à triagem.
  5. Turnos 12x36, SLA, KPIs e passagem de turno.

### Notebook 08 — Threat Landscape and Terminology
- **Objetivo:** Dominar o vocabulário que aparece em alertas, tickets e entrevistas.
- **Estrutura do Conteúdo:**
  1. Vulnerabilidade, ameaça, risco, exploit, CVE e CVSS.
  2. Malware, ransomware, phishing, BEC e engenharia social.
  3. IOC, IoA e TTP; Pyramid of Pain aplicada ao vocabulário.
  4. Controles preventivo, detetivo e corretivo; Zero Trust e MFA.
  5. Boletins de segurança e contexto de risco por ativo.

### Notebook 09 — Alert Triage and Prioritization
- **Objetivo:** Decidir com evidência o que é ruído, o que é falso positivo e o que merece escalonamento.
- **Estrutura do Conteúdo:**
  1. Ler o alerta e a regra que disparou antes de abrir o host.
  2. Cinco perguntas: o que disparou, qual ativo e usuário, é normal ali, há eventos correlatos, qual o impacto.
  3. Enriquecimento: inventário, dono do ativo, histórico do usuário e reputação de IP, domínio e hash.
  4. Classificação em TP, FP, benigno e inconclusivo; na dúvida, escalar.
  5. Priorização por impacto: ativo crítico, credencial privilegiada e múltiplos hosts.
  6. Registro no ticket com fato separado de hipótese.

### Notebook 10 — SIEM Navigation and Search
- **Objetivo:** Consultar, filtrar e correlacionar eventos no SIEM com método.
- **Estrutura do Conteúdo:**
  1. Estrutura de busca em SPL e KQL: filtros, campos extraídos, eval, stats e timechart.
  2. Agregações, lookups e joins entre fontes.
  3. Dashboards, buscas salvas e alertas.
  4. Regras de correlação: janela de tempo, threshold e agrupamento por usuário ou host.
  5. Ferramentas do mercado: Splunk, Microsoft Sentinel, QRadar, Elastic e Wazuh.
  6. Prática com BOTSv3 e Splunk Free usando telemetria real.

### Notebook 11 — Threat Intelligence and Enrichment
- **Objetivo:** Transformar indicadores em contexto para a decisão de triagem.
- **Estrutura do Conteúdo:**
  1. IOC versus relatório de CTI: feeds, boletins e inteligência interna.
  2. Enriquecimento de IP, domínio, URL e hash em VirusTotal, AbuseIPDB e urlscan.
  3. MISP, OpenCTI e STIX/TAXII no nível do analista.
  4. Pyramid of Pain: por que TTP vale mais que um hash.
  5. Registro da fonte e da data da inteligência usada no ticket.

### Notebook 12 — Phishing and Email Analysis
- **Objetivo:** Investigar um e-mail suspeito do cabeçalho ao impacto no endpoint.
- **Estrutura do Conteúdo:**
  1. Cabeçalho: Received, From, Return-Path, SPF, DKIM e DMARC.
  2. URLs e anexos: urlscan, sandbox e hash, sem abrir no host de trabalho.
  3. BEC e spoofing de executivo versus campanha em massa.
  4. Busca do mesmo remetente e URL na organização inteira no SIEM.
  5. Verificação do clique no EDR e correlação com criação de processo.
  6. Bloqueio do domínio, remoção dos e-mails e comunicação ao usuário.

### Notebook 13 — Endpoint Triage with EDR
- **Objetivo:** Usar telemetria de endpoint para validar e conter um alerta.
- **Estrutura do Conteúdo:**
  1. Process tree, linha de comando, usuário e caminho do executável.
  2. Isolamento do host: quando isolar e quando apenas monitorar.
  3. Live response, varredura remota e coleta de artefatos.
  4. LoLBins, powershell.exe -enc e pais inesperados como winword.exe.
  5. Políticas de exclusão e impacto no tuning de detecções.
  6. EDR no mercado: Defender for Endpoint, CrowdStrike Falcon e SentinelOne.

### Notebook 14 — Network Traffic Analysis
- **Objetivo:** Reconstruir a comunicação suspeita a partir de fluxos e capturas.
- **Estrutura do Conteúdo:**
  1. Wireshark: follow streams, filtros de display e leitura de flags.
  2. Beaconing DNS e HTTP, jitter e periodicidade.
  3. Suricata e Zeek: alertas e registros de conexão em conn.log, dns.log e http.log.
  4. Proxy, firewall e WAF como fontes complementares.
  5. Exfiltração e tunelamento: sinais em volume, porta e payload.

### Notebook 15 — Incident Response Lifecycle
- **Objetivo:** Seguir um ciclo de resposta consistente do primeiro alerta ao postmortem.
- **Estrutura do Conteúdo:**
  1. NIST SP 800-61r3: Detect, Respond, Recover e Improvement.
  2. Preparação: playbooks, papéis, contatos e acessos.
  3. Contenção curta e longa, erradicação e recuperação.
  4. Cadeia de custódia, evidência em UTC e preservação de logs.
  5. Comunicação com usuários, gestão e áreas afetadas.
  6. Lições aprendidas e atualização dos playbooks.

### Notebook 16 — SOC Operations and Reporting
- **Objetivo:** Encerrar o turno com caso documentado e passagem limpa para o próximo analista.
- **Estrutura do Conteúdo:**
  1. Abertura da fila, checklist de fontes e casos sem dono.
  2. Escrita de caso: fato, hipótese, evidência, ação e próximo passo.
  3. Handoff entre turnos e confirmação de leitura.
  4. Jira, ServiceNow e Zendesk: prioridade, estado e SLA.
  5. MTTD, MTTR e volume de alertas como métricas da fila.
  6. Inglês técnico para leitura de documentação e método STAR para entrevista.

### Notebook 17 — MITRE ATT&CK in Practice
- **Objetivo:** Usar ATT&CK como linguagem comum para descrever, mapear e cobrir comportamentos.
- **Estrutura do Conteúdo:**
  1. Táticas, técnicas e sub-técnicas; v20 com Stealth TA0005 e Defense Impairment TA0112.
  2. Mapeamento de alertas e casos com IDs Txxxx.
  3. Navigator para visualizar cobertura e encontrar gaps de telemetria.
  4. Relação com a Kill Chain: técnicas não são lineares.
  5. Planejamento de purple team a partir das lacunas.

### Notebook 18 — Frameworks Compared
- **Objetivo:** Escolher o modelo certo para explicar o ataque e priorizar a defesa.
- **Estrutura do Conteúdo:**
  1. Cyber Kill Chain: sete fases, contra-medidas por fase e a limitação linear.
  2. Diamond Model: Adversary, Infrastructure, Capability, Victim e activity threads.
  3. Pyramid of Pain: hash, IP, domínio, artefato, ferramenta e TTP.
  4. NIST CSF 2.0: GV, ID, PR, DE, RS e RC, com foco em DE e RS para o SOC.
  5. Quando usar cada modelo num relatório ou postmortem.

### Notebook 19 — Detection Engineering with Sigma
- **Objetivo:** Escrever e manter regras de detecção que sobrevivam ao contato com a fila real.
- **Estrutura do Conteúdo:**
  1. Estrutura Sigma YAML: logsource, detection, condition e level.
  2. Conversão para SPL, KQL e XML com pySigma.
  3. Mapeamento ATT&CK e tags na regra.
  4. Tuning de falsos positivos com exceções documentadas.
  5. Versionamento, revisão por pares e testes com dados sintéticos.
  6. Regras gerenciadas do fornecedor versus regras próprias.

### Notebook 20 — Detection Validation and Purple Team
- **Objetivo:** Provar que a detecção dispara e medir o que ficou sem cobertura.
- **Estrutura do Conteúdo:**
  1. Atomic Red Team e Caldera para simular técnicas.
  2. BOTSv3 e datasets públicos para validar consultas sem gerar incidente.
  3. Testes controlados em laboratório com hosts isolados.
  4. Medição de cobertura por tática e lacunas de log.
  5. Documentação do resultado, ajuste da regra e repetição do teste.

### Notebook 21 — Vulnerabilities and Exposure
- **Objetivo:** Entender a relação entre vulnerabilidade, ativo e risco na rotina do SOC.
- **Estrutura do Conteúdo:**
  1. CVE, CVSS e priorização por explorabilidade e exposição.
  2. Scanning e inventário: o que o SOC consome do time de vulnerability management.
  3. Explorações comuns em SMB, RDP e aplicações web expostas.
  4. Correlação entre alerta e ativo vulnerável durante o enriquecimento.
  5. Escalonamento para o time de patches com evidência.

### Notebook 22 — Windows Persistence and Privilege
- **Objetivo:** Encontrar mecanismos de persistência e elevação usados depois do acesso inicial.
- **Estrutura do Conteúdo:**
  1. Run e RunOnce, Startup, serviços com 7045 e tarefas com 4698.
  2. WMI event subscriptions e DLL hijack ou sideload.
  3. Autoruns e Sysinternals para inventariar pontos de inicialização.
  4. Evento 4672, privilégios especiais e UAC bypass.
  5. Fileless e uso de LoLBins.
  6. Remoção da persistência e verificação de que não voltou.

### Notebook 23 — Identity Attacks and Active Directory
- **Objetivo:** Investigar ataques a identidade e diretório, a principal via de movimento lateral.
- **Estrutura do Conteúdo:**
  1. Kerberos: AS-REQ, AS-REP, TGS e eventos 4768, 4769 e 4776.
  2. Kerberoasting, pass-the-hash e pass-the-ticket.
  3. Golden Ticket com hash krbtgt e rotação dupla; Silver Ticket com hash de serviço.
  4. DCSync e replicação indevida de diretório.
  5. PAM, JIT, LAPS e Conditional Access como controles.
  6. Correlação entre logon atípico e mudança de privilégio.

### Notebook 24 — Lateral Movement
- **Objetivo:** Reconhecer a movimentação entre hosts antes da contenção.
- **Estrutura do Conteúdo:**
  1. PsExec e SMB, WinRM nas portas 5985 e 5986, RDP e WMI.
  2. Eventos 4624 tipo 3, 4648, 7045 e conexões nas portas 445 e 5985.
  3. Administração legítima versus padrão anômalo por host e horário.
  4. Sysmon 1, 3 e 10 na reconstrução da cadeia.
  5. Regras Sigma e consultas SPL e KQL para detectar o padrão.
  6. Escalonamento e contenção do host de origem.

### Notebook 25 — Memory and Host Forensics
- **Objetivo:** Recuperar evidência que não existe mais em log quando o atacante agiu no host.
- **Estrutura do Conteúdo:**
  1. Volatility 3: processos ocultos, árvore, código injetado e sockets.
  2. KAPE e Velociraptor para coleta rápida e remota.
  3. MFT, USN Journal, Prefetch, ShimCache, Amcache e SRUM.
  4. Registry hives e artefatos de navegador.
  5. Cadeia de custódia e hash da imagem antes da análise.
  6. Limite entre N2 e N3: quando pedir forense profunda.

### Notebook 26 — Threat Hunting Methodology
- **Objetivo:** Procurar atividade que não gerou alerta, a principal diferença prática do N2.
- **Estrutura do Conteúdo:**
  1. Hipótese a partir de CTI, ATT&CK e anomalias do ambiente.
  2. Baseline do que é normal para aquele host e usuário.
  3. Busca em SIEM e EDR por comportamento, não apenas por IOC.
  4. Iteração: ampliar, refutar ou confirmar a hipótese com evidência.
  5. Resultado documentado: achado, regra nova ou gap de telemetria.

### Notebook 27 — Cloud SOC (M365 and AWS)
- **Objetivo:** Investigar identidade e cargas em nuvem com os logs que o analista realmente tem.
- **Estrutura do Conteúdo:**
  1. Entra ID sign-in logs, risco de usuário e Conditional Access.
  2. Unified Audit Log e logs de Exchange e SharePoint no M365.
  3. CloudTrail, GuardDuty, VPC Flow Logs e AWS Config.
  4. Correlação entre identidade e atividade de cloud.
  5. Casos típicos: token roubado, access key exposta e privilege escalation.
  6. Quando escalar para o time de cloud security engineering.

### Notebook 28 — Automation for Analysts
- **Objetivo:** Reduzir trabalho repetitivo de triagem com scripts e playbooks simples.
- **Estrutura do Conteúdo:**
  1. Python para parsear logs, normalizar campos e enriquecer IOCs.
  2. PowerShell para consultar eventos e inventariar hosts.
  3. Bash para tratar arquivos e texto em hosts Linux.
  4. Integração com APIs de threat intel e de ticketing.
  5. SOAR e playbooks: o que automatizar e o que exige julgamento humano.
  6. Cuidado com segredos, logs da automação e auditabilidade.

### Notebook 29 — Certification Strategy
- **Objetivo:** Escolher certificação sem confundir filtro de RH com competência prática.
- **Estrutura do Conteúdo:**
  1. Network+ e Security+ SY0-701 como base, com foco em Security Operations.
  2. CySA+ CS0-004: SecOps, vulnerability management, IR e reporting.
  3. SC-200 para ambientes Microsoft; BTL1, SAL1 e SAL2 como prova prática.
  4. Mudanças em 2026: AZ-500 e MS-102 aposentados e transição de versões da CompTIA.
  5. CEH e PNPT: o que entregam e por que não substituem prática de SOC.
  6. Regra prática: a certificação abre a entrevista; log e relatório decidem.

### Notebook 30 — Home Lab and Practice
- **Objetivo:** Montar um ambiente de treino barato para praticar toda semana.
- **Estrutura do Conteúdo:**
  1. Wazuh e OpenSearch como SIEM open-source leve.
  2. Splunk Free e BOTSv3 para SPL com dados reais.
  3. Elastic Security para KQL e detecções; Security Onion para Zeek, Suricata e pcap.
  4. TryHackMe SOC L1 e L2, e CyberDefenders para investigações guiadas.
  5. Cadência: um caso por semana com write-up em português.
  6. Limitações do laboratório: o que só aparece em produção.

### Notebook 31 — Interview Practice N1
- **Objetivo:** Responder perguntas técnicas de triagem com método e evidência.
- **Estrutura do Conteúdo:**
  1. Como triar um alerta: cinco passos e critérios de escalonamento.
  2. 4624, 4625 e 4688, Logon Types e substatus em cenários de brute force.
  3. Phishing: cabeçalho, SPF, DKIM, DMARC e busca na organização inteira.
  4. Leitura de linha de log: o que você vê e o que faz em seguida.
  5. Impossible travel e login de país incomum.
  6. Método STAR para situações de erro, conflito e pressão de SLA.

### Notebook 32 — Interview Practice N2 and Capstone
- **Objetivo:** Demonstrar profundidade N2 com correlação, decisão e comunicação.
- **Estrutura do Conteúdo:**
  1. Correlação de endpoint, rede, identidade e cloud num único caso.
  2. Quando isolar o host e quando apenas monitorar: tradeoffs.
  3. Tuning de detecção com evidência de falso positivo.
  4. Explicar Golden Ticket, DCSync e persistência em linguagem simples.
  5. Mentoria do N1 e escrita de relatório para executivo.
  6. Capstone: investigar um caso fim a fim e entregar timeline, IOC, ATT&CK e ações.
