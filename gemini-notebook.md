# Plano de estudos — SOC N1 e N2

Reorganizado em 26/11/2026 a partir de levantamento de vagas de SOC N1 e N2 (Brasil e remoto, 2024–2026), discussões em fóruns (r/cybersecurity, r/SecurityCareerAdvice, Hacker News) e fontes oficiais (MITRE ATT&CK v20, NIST SP 800-61r3, NIST CSF 2.0, CompTIA, Microsoft, SigmaHQ).

**Como usar:** a ordem dos notebooks é a ordem de estudo. Cada notebook tem de 3 a 4 tópicos, para que o aprofundamento não seja sacrificado pela quantidade de assuntos. Os notebooks 01–12 são a base; 13–26 cobrem a operação do N1; 27–32 tratam de frameworks e detecção; 33–45 aprofundam o N2; 46–53 fecham com certificação, laboratório e entrevista. O índice antigo, do pacote Cloud, ficou preservado em `.archive/gemini-notebook-cloud.md`.

### Notebook 01 — TCP/IP and OSI Model
- **Objetivo:** Entender o modelo de comunicação e o handshake TCP antes de olhar qualquer alerta.
- **Estrutura do Conteúdo:**
  1. Modelo OSI e modelo TCP/IP, camadas e encapsulamento.
  2. Endereços MAC e IP, ARP e resolução local.
  3. TCP versus UDP, handshake de três vias e flags SYN, ACK, FIN e RST.

### Notebook 02 — Network Addressing and Inspection
- **Objetivo:** Reconhecer endereçamento, portas e pontos de observação da rede.
- **Estrutura do Conteúdo:**
  1. Portas críticas: 22, 53, 80, 443, 88, 389, 445 e 3389.
  2. CIDR, subnetting, default gateway, NAT e VLAN na investigação.
  3. Leitura de pcap no Wireshark: conversas, fluxos e anomalias.
  4. O que firewall, proxy, WAF e IDS/IPS registram.

### Notebook 03 — DNS Records and Abuse
- **Objetivo:** Ler registros DNS e identificar padrões de abuso em consultas.
- **Estrutura do Conteúdo:**
  1. Registros A, AAAA, CNAME, MX, NS e TXT com SPF, DKIM e DMARC.
  2. DGA, fast flux e TTL muito baixo.
  3. Tunelamento DNS e consultas anômalas em volume e frequência.

### Notebook 04 — Web and TLS Signals
- **Objetivo:** Extrair sinais de requisições web e conexões TLS em logs.
- **Estrutura do Conteúdo:**
  1. Métodos e códigos de status HTTP no access.log.
  2. User-Agent e Referer como pista, com a ressalva de que podem ser forjados.
  3. TLS handshake, emissor e validade do certificado; certificado autoassinado como indicador.
  4. Consulta de reputação de domínio e URL em VirusTotal e urlscan.

### Notebook 05 — Linux CLI and Processes
- **Objetivo:** Navegar no Linux e entender o modelo de processos de um host.
- **Estrutura do Conteúdo:**
  1. Shell, navegação, permissões, usuários, sudo e UID/GID.
  2. Processos, threads, ps, top e árvore de processos.
  3. Sinais, prioridade e identificação de processo problemático.

### Notebook 06 — Linux Logs and Network Triage
- **Objetivo:** Encontrar evidência em logs Linux e coletar dados de rede no host.
- **Estrutura do Conteúdo:**
  1. `/var/log/auth.log`, `/var/log/secure`, journalctl e dmesg.
  2. cron, systemd, auditd, integridade de arquivos e shell history.
  3. ss e netstat para conexões e portas em escuta.
  4. curl e tcpdump na triagem de um host Linux.

### Notebook 07 — Windows Essentials for SOC
- **Objetivo:** Entender a estrutura do Windows para saber onde a evidência aparece.
- **Estrutura do Conteúdo:**
  1. Usuários, grupos, UAC, privilégios e Registry.
  2. Árvore de processos: smss, csrss, wininit, services, lsass e svchost.
  3. Serviços, tarefas agendadas, pasta Startup e chaves Run/RunOnce.
  4. PowerShell, ExecutionPolicy e logging de script block.

### Notebook 08 — Windows Event IDs and Logon Types
- **Objetivo:** Interpretar eventos de autenticação e criação de conta no Windows.
- **Estrutura do Conteúdo:**
  1. Eventos 4624 e 4625: sucesso e falha de logon.
  2. Logon Types 2, 3 e 10; substatus 0xC0000064 versus 0xC000006A.
  3. Eventos 4648, 4672, 4720 e 4732.
  4. Kerberos no Domain Controller: 4768, 4769 e 4776.

### Notebook 09 — Windows Process and Sysmon Events
- **Objetivo:** Correlacionar criação de processo, serviços e eventos do Sysmon.
- **Estrutura do Conteúdo:**
  1. Eventos 4688 e 4689 com linha de comando.
  2. PowerShell 4104 e Task Scheduler 106, 200 e 201.
  3. Serviço 7045 e limpeza de log com 1102.
  4. Sysmon IDs 1, 3, 7, 8, 10, 11, 13 e 22.

### Notebook 10 — Logs, Timestamps and Normalization
- **Objetivo:** Tornar logs de fontes diferentes comparáveis e confiáveis na linha do tempo.
- **Estrutura do Conteúdo:**
  1. Fontes: endpoint, rede, identidade, aplicação e cloud.
  2. Syslog, CEF e JSON; facility e severidade.
  3. Normalização de campos com ECS e ASIM.
  4. NTP, UTC, retenção e envio centralizado de logs.

### Notebook 11 — SOC Fundamentals and Analyst Tiers
- **Objetivo:** Entender a missão do SOC e onde o N1 termina e o N2 começa.
- **Estrutura do Conteúdo:**
  1. SOC versus NOC versus CSIRT.
  2. Fluxo monitorar, triar, escalar e documentar.
  3. N1, N2 e N3: responsabilidades, on-call e critérios de escalonamento.
  4. Evento, alerta, incidente e caso; severidade versus prioridade.

### Notebook 12 — Threat Landscape Terminology
- **Objetivo:** Dominar o vocabulário que aparece em alertas, tickets e entrevistas.
- **Estrutura do Conteúdo:**
  1. Vulnerabilidade, ameaça, risco, exploit, CVE e CVSS.
  2. Malware, ransomware, phishing, BEC e engenharia social.
  3. IOC, IoA e TTP; Pyramid of Pain aplicada ao vocabulário.
  4. Controles preventivo, detetivo e corretivo; Zero Trust e MFA.

### Notebook 13 — Alert Triage Fundamentals
- **Objetivo:** Abrir um alerta com método e decidir a classificação inicial.
- **Estrutura do Conteúdo:**
  1. Ler o alerta e a regra que disparou antes de abrir o host.
  2. Cinco perguntas: o que disparou, qual ativo e usuário, é normal ali, há eventos correlatos, qual o impacto.
  3. Classificação em TP, FP, benigno e inconclusivo.
  4. Regra prática: na dúvida, escalar.

### Notebook 14 — Alert Enrichment and Escalation
- **Objetivo:** Enriquecer o alerta e repassá-lo com contexto suficiente para o N2.
- **Estrutura do Conteúdo:**
  1. Inventário, dono do ativo, histórico do usuário e reputação de IP, domínio e hash.
  2. Priorização por impacto: ativo crítico, credencial privilegiada e múltiplos hosts.
  3. Critérios de escalonamento: ameaça confirmada, ativo crítico ou indício de movimentação lateral.
  4. Registro no ticket com fato separado de hipótese.

### Notebook 15 — SIEM Search Fundamentals
- **Objetivo:** Buscar e agregar eventos no SIEM com consultas reutilizáveis.
- **Estrutura do Conteúdo:**
  1. Estrutura de busca em SPL e KQL: filtros, campos extraídos e eval.
  2. Agregações com stats e timechart.
  3. Lookups e joins entre fontes.
  4. Dashboards, buscas salvas e alertas.

### Notebook 16 — Correlation Rules and SIEM Tools
- **Objetivo:** Entender como a regra se torna alerta e quais SIEMs aparecem no mercado.
- **Estrutura do Conteúdo:**
  1. Regras de correlação: janela de tempo, threshold e agrupamento por usuário ou host.
  2. Splunk, Microsoft Sentinel, QRadar, Elastic e Wazuh.
  3. Prática com BOTSv3 e Splunk Free usando telemetria real.
  4. Ajuste de regra a partir do retorno do analista.

### Notebook 17 — Threat Intelligence for Analysts
- **Objetivo:** Transformar indicadores em contexto para a decisão de triagem.
- **Estrutura do Conteúdo:**
  1. IOC versus relatório de CTI: feeds, boletins e inteligência interna.
  2. Enriquecimento de IP, domínio, URL e hash em VirusTotal, AbuseIPDB e urlscan.
  3. MISP, OpenCTI e STIX/TAXII no nível do analista.
  4. Pyramid of Pain e registro da fonte e da data no ticket.

### Notebook 18 — Phishing Analysis: Email Artifacts
- **Objetivo:** Analisar o e-mail suspeito pelo cabeçalho e pelo conteúdo.
- **Estrutura do Conteúdo:**
  1. Cabeçalho: Received, From, Return-Path, SPF, DKIM e DMARC.
  2. URLs e anexos: urlscan, sandbox e hash, sem abrir no host de trabalho.
  3. BEC e spoofing de executivo versus campanha em massa.

### Notebook 19 — Phishing Response and Hunting
- **Objetivo:** Medir o alcance da campanha e remover o impacto na organização.
- **Estrutura do Conteúdo:**
  1. Busca do mesmo remetente e URL na organização inteira no SIEM.
  2. Verificação do clique no EDR e correlação com criação de processo.
  3. Bloqueio do domínio e remoção dos e-mails.
  4. Comunicação ao usuário e registro do caso.

### Notebook 20 — EDR Triage Fundamentals
- **Objetivo:** Validar um alerta de endpoint pela árvore de processos.
- **Estrutura do Conteúdo:**
  1. Process tree, linha de comando, usuário e caminho do executável.
  2. LoLBins, powershell.exe -enc e pais inesperados como winword.exe.
  3. Isolamento do host: quando isolar e quando apenas monitorar.

### Notebook 21 — EDR Response and Tuning
- **Objetivo:** Coletar evidência no endpoint e ajustar a detecção.
- **Estrutura do Conteúdo:**
  1. Live response e varredura remota.
  2. Coleta de artefatos do endpoint.
  3. Políticas de exclusão e impacto no tuning de detecções.
  4. Defender for Endpoint, CrowdStrike Falcon e SentinelOne.

### Notebook 22 — Network Traffic Analysis
- **Objetivo:** Reconstruir a comunicação suspeita a partir de capturas e logs de rede.
- **Estrutura do Conteúdo:**
  1. Wireshark: follow streams, filtros de display e leitura de flags.
  2. Beaconing DNS e HTTP, jitter e anomalias de periodicidade.
  3. Suricata e Zeek: alertas, conn.log, dns.log e http.log.
  4. Exfiltração e tunelamento em proxy, firewall e WAF.

### Notebook 23 — Incident Response Phases
- **Objetivo:** Seguir o ciclo NIST sem pular a preservação de evidência.
- **Estrutura do Conteúdo:**
  1. NIST SP 800-61r3: Detect, Respond, Recover e Improvement.
  2. Preparação: playbooks, papéis, contatos e acessos.
  3. Contenção curta e longa, erradicação e recuperação.
  4. Cadeia de custódia, evidência em UTC e preservação de logs.

### Notebook 24 — Incident Communication and Improvement
- **Objetivo:** Fechar o incidente com comunicação correta e aprendizado registrado.
- **Estrutura do Conteúdo:**
  1. Comunicação com usuários, gestão e áreas afetadas.
  2. Linha do tempo do caso e decisões registradas.
  3. Postmortem e lições aprendidas.
  4. Atualização dos playbooks e das regras de detecção.

### Notebook 25 — SOC Shift Operations
- **Objetivo:** Abrir e encerrar o turno sem deixar alerta sem dono.
- **Estrutura do Conteúdo:**
  1. Abertura da fila e checklist das fontes de log.
  2. Casos sem dono e priorização no início do turno.
  3. Handoff entre turnos e confirmação de leitura.
  4. Jira, ServiceNow e Zendesk: prioridade, estado e SLA.

### Notebook 26 — Case Writing and Metrics
- **Objetivo:** Escrever casos que qualquer analista consiga continuar.
- **Estrutura do Conteúdo:**
  1. Escrita de caso: fato, hipótese, evidência e próximo passo.
  2. MTTD, MTTR e volume de alertas como métricas da fila.
  3. Relatório de turno para gestão.
  4. Inglês técnico para leitura de documentação.

### Notebook 27 — MITRE ATT&CK Fundamentals
- **Objetivo:** Usar ATT&CK como linguagem comum para descrever comportamentos.
- **Estrutura do Conteúdo:**
  1. Táticas, técnicas e sub-técnicas.
  2. v20: Stealth TA0005 e Defense Impairment TA0112.
  3. Mapeamento de alertas e casos com IDs Txxxx.
  4. Navigator para cobertura, gaps de telemetria e planejamento de purple team.

### Notebook 28 — Frameworks Compared
- **Objetivo:** Escolher o modelo certo para explicar o ataque e priorizar a defesa.
- **Estrutura do Conteúdo:**
  1. Cyber Kill Chain: sete fases, contra-medidas e limitação linear.
  2. Diamond Model: Adversary, Infrastructure, Capability e Victim.
  3. Pyramid of Pain: hash, IP, domínio, artefato, ferramenta e TTP.
  4. NIST CSF 2.0: GV, ID, PR, DE, RS e RC, com foco em DE e RS no SOC.

### Notebook 29 — Writing Detection Rules
- **Objetivo:** Escrever uma regra de detecção com campos e mapeamento corretos.
- **Estrutura do Conteúdo:**
  1. Estrutura Sigma YAML: logsource, detection, condition e level.
  2. Conversão para SPL, KQL e XML com pySigma.
  3. Mapeamento ATT&CK e tags na regra.
  4. Regras gerenciadas do fornecedor versus regras próprias.

### Notebook 30 — Detection Tuning and Maintenance
- **Objetivo:** Manter a regra útil depois que ela encontra a fila real.
- **Estrutura do Conteúdo:**
  1. Tuning de falsos positivos com exceções documentadas.
  2. Versionamento e revisão por pares.
  3. Testes com dados sintéticos.
  4. Documentação da regra e impacto no volume de alertas.

### Notebook 31 — Detection Validation
- **Objetivo:** Provar que a detecção dispara e medir o que ficou sem cobertura.
- **Estrutura do Conteúdo:**
  1. Atomic Red Team e Caldera para simular técnicas.
  2. BOTSv3 e datasets públicos para validar consultas.
  3. Testes controlados em laboratório com hosts isolados.
  4. Medição de cobertura, documentação do resultado e repetição do teste.

### Notebook 32 — Vulnerabilities and Exposure
- **Objetivo:** Conectar alerta, ativo vulnerável e risco na rotina do SOC.
- **Estrutura do Conteúdo:**
  1. CVE, CVSS e priorização por explorabilidade e exposição.
  2. Scanning e inventário: o que o SOC consome do time de vulnerability management.
  3. Explorações comuns em SMB, RDP e aplicações web expostas.
  4. Correlação com ativo vulnerável e escalonamento para o time de patches.

### Notebook 33 — Windows Persistence Mechanisms
- **Objetivo:** Reconhecer os pontos de inicialização usados após o acesso inicial.
- **Estrutura do Conteúdo:**
  1. Run e RunOnce, Startup, serviços com 7045 e tarefas com 4698.
  2. WMI event subscriptions e DLL hijack ou sideload.
  3. Autoruns e Sysinternals para inventariar a inicialização.
  4. Fileless e uso de LoLBins na persistência.

### Notebook 34 — Privilege and Cleanup
- **Objetivo:** Entender a elevação de privilégio e confirmar que a persistência foi removida.
- **Estrutura do Conteúdo:**
  1. Evento 4672, privilégios especiais e UAC bypass.
  2. Verificação da conta e do token usados na ação.
  3. Remoção da persistência identificada.
  4. Confirmação de que não voltou após reboot.

### Notebook 35 — Kerberos and Ticket Attacks
- **Objetivo:** Investigar ataques a tickets de autenticação no Windows.
- **Estrutura do Conteúdo:**
  1. Kerberos: AS-REQ, AS-REP, TGS e eventos 4768, 4769 e 4776.
  2. Kerberoasting e pass-the-ticket.
  3. Golden Ticket com hash krbtgt e rotação dupla.
  4. Silver Ticket com hash de serviço.

### Notebook 36 — Active Directory Compromise
- **Objetivo:** Detectar o abuso de identidade e diretório no movimento lateral.
- **Estrutura do Conteúdo:**
  1. Pass-the-hash e uso de credenciais roubadas.
  2. DCSync e replicação indevida de diretório.
  3. Correlação entre logon atípico e mudança de privilégio.
  4. PAM, JIT, LAPS e Conditional Access como controles.

### Notebook 37 — Lateral Movement Techniques
- **Objetivo:** Conhecer os protocolos usados para saltar de um host para outro.
- **Estrutura do Conteúdo:**
  1. PsExec e SMB, WinRM nas portas 5985 e 5986.
  2. RDP e WMI como vetores de acesso remoto.
  3. Eventos 4624 tipo 3, 4648 e 7045.
  4. Conexões nas portas 445 e 5985 na reconstrução do caso.

### Notebook 38 — Detecting Lateral Movement
- **Objetivo:** Separar administração legítima de padrão anômalo e conter a origem.
- **Estrutura do Conteúdo:**
  1. Administração legítima versus padrão anômalo por host e horário.
  2. Sysmon 1, 3 e 10 na cadeia de execução.
  3. Regras Sigma e consultas SPL e KQL para o padrão.
  4. Escalonamento e contenção do host de origem.

### Notebook 39 — Memory Forensics Basics
- **Objetivo:** Recuperar evidência de memória quando o log já não basta.
- **Estrutura do Conteúdo:**
  1. Volatility 3: processos ocultos e árvore de processos.
  2. Código injetado e sockets suspeitos.
  3. KAPE e Velociraptor para coleta rápida e remota.
  4. Hash da imagem e cadeia de custódia antes da análise.

### Notebook 40 — Host Artifacts and Scope
- **Objetivo:** Usar artefatos de disco para montar a linha do tempo e definir o escopo.
- **Estrutura do Conteúdo:**
  1. MFT, USN Journal, Prefetch e ShimCache.
  2. Amcache e SRUM na linha do tempo.
  3. Registry hives e artefatos de navegador.
  4. Limite entre N2 e N3: quando pedir forense profunda.

### Notebook 41 — Threat Hunting Methodology
- **Objetivo:** Procurar atividade que não gerou alerta, a diferença prática do N2.
- **Estrutura do Conteúdo:**
  1. Hipótese a partir de CTI, ATT&CK e anomalias do ambiente.
  2. Baseline do que é normal para aquele host e usuário.
  3. Busca em SIEM e EDR por comportamento, não apenas por IOC.
  4. Iteração, documentação do achado e conversão em regra.

### Notebook 42 — Cloud Identity Telemetry (M365)
- **Objetivo:** Investigar identidade e acesso no Microsoft 365.
- **Estrutura do Conteúdo:**
  1. Entra ID sign-in logs e risco de usuário.
  2. Conditional Access e sinais de risco.
  3. Unified Audit Log e logs de Exchange e SharePoint.
  4. Casos típicos: token roubado e MFA fatigue.

### Notebook 43 — AWS Telemetry for SOC
- **Objetivo:** Investigar atividade em AWS com os logs que o analista tem acesso.
- **Estrutura do Conteúdo:**
  1. CloudTrail e eventos de API.
  2. GuardDuty e VPC Flow Logs.
  3. AWS Config e mudanças de configuração.
  4. Correlação entre identidade e atividade de cloud, e quando escalar ao time de cloud.

### Notebook 44 — Scripting for Analysts
- **Objetivo:** Automatizar parsing, normalização e enriquecimento no dia a dia.
- **Estrutura do Conteúdo:**
  1. Python para parsear logs e enriquecer IOCs.
  2. PowerShell para consultar eventos e inventariar hosts.
  3. Bash para tratar arquivos e texto em Linux.
  4. Normalização de campos com scripts próprios.

### Notebook 45 — Orchestration and Safety
- **Objetivo:** Integrar automação ao fluxo de casos sem criar novo risco.
- **Estrutura do Conteúdo:**
  1. Integração com APIs de threat intel e de ticketing.
  2. SOAR e playbooks: o que automatizar.
  3. O que exige julgamento humano.
  4. Segredos, logs da automação e auditabilidade.

### Notebook 46 — Core Certifications for SOC
- **Objetivo:** Escolher a base de certificação que realmente aparece em vagas.
- **Estrutura do Conteúdo:**
  1. Network+ e Security+ SY0-701 como base.
  2. Foco em Security Operations no SY0-701.
  3. CySA+ CS0-004: SecOps, vulnerability management e IR.
  4. SC-200 para ambientes Microsoft com Sentinel e Defender.

### Notebook 47 — Practical Certifications and 2026 Changes
- **Objetivo:** Diferenciar prova prática de filtro de RH e evitar certificações aposentadas.
- **Estrutura do Conteúdo:**
  1. BTL1, SAL1 e SAL2 como prova prática.
  2. AZ-500 e MS-102 aposentados em 2026.
  3. CEH e PNPT: o que entregam e o que não entregam para SOC.
  4. Regra prática: a certificação abre a entrevista; log e relatório decidem.

### Notebook 48 — Building the Home Lab
- **Objetivo:** Montar um laboratório barato para praticar consultas e detecções.
- **Estrutura do Conteúdo:**
  1. Wazuh e OpenSearch como SIEM open-source leve.
  2. Splunk Free e BOTSv3 para SPL com dados reais.
  3. Elastic Security para KQL e detecções.
  4. Security Onion para Zeek, Suricata e pcap.

### Notebook 49 — Practice Routine
- **Objetivo:** Transformar o laboratório em prática constante com registro de casos.
- **Estrutura do Conteúdo:**
  1. TryHackMe SOC L1 e L2 como trilha guiada.
  2. CyberDefenders para investigações baseadas em evidências.
  3. Cadência de um caso por semana com write-up em português.
  4. Limitações do laboratório e o que só aparece em produção.

### Notebook 50 — Interview Practice N1: Technical
- **Objetivo:** Responder perguntas técnicas de triagem com método e evidência.
- **Estrutura do Conteúdo:**
  1. Como triar um alerta em cinco passos e quando escalar.
  2. 4624, 4625, 4688 e Logon Types em cenário de brute force.
  3. Phishing: cabeçalho, SPF, DKIM, DMARC e busca na organização.
  4. Leitura de linha de log e impossibilidade de viagem (impossible travel).

### Notebook 51 — Interview Practice N1: Behavior
- **Objetivo:** Explicar decisões e situações de turno com clareza.
- **Estrutura do Conteúdo:**
  1. Como justificar o escalonamento de um alerta.
  2. Situação de erro técnico e assunção de responsabilidade.
  3. Conflito e pressão de SLA com o método STAR.
  4. Perguntas sobre turno, documentação e inglês técnico.

### Notebook 52 — Interview Practice N2
- **Objetivo:** Demonstrar profundidade N2 com correlação, decisão e comunicação.
- **Estrutura do Conteúdo:**
  1. Correlação de endpoint, rede, identidade e cloud num único caso.
  2. Quando isolar o host e quando apenas monitorar.
  3. Tuning de detecção com evidência de falso positivo.
  4. Explicar Golden Ticket, DCSync e persistência em linguagem simples.

### Notebook 53 — Capstone: End-to-End Investigation
- **Objetivo:** Conduzir um caso completo e entregar um relatório utilizável.
- **Estrutura do Conteúdo:**
  1. Seleção do caso e levantamento das fontes de evidência.
  2. Timeline, IOC e mapeamento ATT&CK.
  3. Decisões de contenção e escalonamento.
  4. Relatório final com ações e lições aprendidas.
