# Plano de Estudos — AppSec Engineer

# Fase 0 — Fundamentos

### Notebook 01 — Web Application Security Fundamentals
- **Objetivo:** Compreender o que é segurança de aplicações e por que ela depende de pessoas, processo e tecnologia.
- **Estrutura do Conteúdo:**
  1. O que é Application Security e o papel do AppSec Engineer.
  2. Threat actors, motivações e modelos de ameaça mais comuns contra aplicações web.
  3. Confidentiality, Integrity e Availability (CIA) aplicados a software.
  4. Diferença entre vulnerabilidade, ameaça, risco e exposição.
  5. Defesa em profundidade e o princípio de least privilege no ciclo de desenvolvimento.

### Notebook 02 — HTTP for AppSec
- **Objetivo:** Ler e interpretar tráfego HTTP para identificar onde controles de segurança são aplicados ou ignorados.
- **Estrutura do Conteúdo:**
  1. Estrutura de uma mensagem HTTP: request line, headers e body.
  2. Métodos HTTP e implicações de segurança de GET, POST, PUT, PATCH e DELETE.
  3. Status codes relevantes para segurança e o que eles revelam.
  4. Cookies, Set-Cookie e atributos Secure, HttpOnly e SameSite.
  5. HTTP/1.1, HTTP/2 e HTTP/3: diferenças que afetam testes e defesas.

### Notebook 03 — Authentication, Sessions and Authorization
- **Objetivo:** Distinguir autenticação de autorização e entender como sessões e tokens mantêm a identidade do usuário.
- **Estrutura do Conteúdo:**
  1. Authentication factors: something you know, have e are.
  2. Password storage, hashing e políticas de credencial.
  3. Session management, session fixation e session hijacking.
  4. Authorization models: RBAC, ABAC e ReBAC.
  5. Tokens, JWT e OAuth 2.0/OpenID Connect em alto nível.

### Notebook 04 — Applied Cryptography for Applications
- **Objetivo:** Aplicar criptografia de forma correta no armazenamento e no transporte de dados da aplicação.
- **Estrutura do Conteúdo:**
  1. Symmetric versus asymmetric encryption e quando usar cada uma.
  2. Hashing, salted hashing e password hashing algorithms (bcrypt, Argon2).
  3. TLS, certificados e o handshake em alto nível.
  4. Key management, rotação de chaves e secrets.
  5. Erros comuns: ECB mode, IV reutilizado e criptografia caseira.

### Notebook 05 — OWASP Top 10 2025 Overview
- **Objetivo:** Conhecer a taxonomia OWASP Top 10 2025 e usá-la como vocabulário comum de risco.
- **Estrutura do Conteúdo:**
  1. O que é o OWASP Top 10 e como ele é construído.
  2. As dez categorias de 2025 e o que mudou em relação a 2021.
  3. A01 Broken Access Control, incluindo SSRF, e A02 Security Misconfiguration.
  4. A03 Software Supply Chain Failures e A10 Mishandling of Exceptional Conditions.
  5. Como mapear um achado real para uma categoria do Top 10.

### Notebook 06 — OWASP ASVS 5.0 and Security Requirements
- **Objetivo:** Traduzir requisitos de segurança em critérios verificáveis usando o OWASP ASVS 5.0.
- **Estrutura do Conteúdo:**
  1. O que é o ASVS e para que servem os níveis de verificação.
  2. Estrutura do ASVS 5.0: capítulos, requisitos e níveis.
  3. Como derivar security requirements de um requisito de negócio.
  4. Uso do ASVS em revisão de arquitetura e em testes.
  5. Limites do ASVS e relação com o Top 10 e o API Top 10.

# Fase 1 — Vulnerabilidades

### Notebook 07 — Broken Access Control (A01, inclui SSRF)
- **Objetivo:** Reconhecer falhas de controle de acesso, incluindo SSRF, e entender como preveni-las.
- **Estrutura do Conteúdo:**
  1. Access control horizontal, vertical e context-dependent.
  2. IDOR e manipulação de identificadores em APIs.
  3. Missing function-level access control e bypass de autorização.
  4. SSRF: server-side request forgery e acesso a metadata de cloud.
  5. Prevenção: deny by default, checagem server-side e allowlists de destino.

### Notebook 08 — Security Misconfiguration (A02)
- **Objetivo:** Identificar configurações inseguras em aplicações, servidores e serviços gerenciados.
- **Estrutura do Conteúdo:**
  1. Default credentials, contas de exemplo e recursos desnecessários.
  2. Mensagens de erro verbosas e exposição de stack traces.
  3. Security headers e configuração de CORS.
  4. Configuração insegura em cloud storage e serviços gerenciados.
  5. Hardening, baseline de configuração e Infrastructure as Code.

### Notebook 09 — Software Supply Chain Failures (A03)
- **Objetivo:** Entender como dependências e artefatos comprometidos introduzem risco na aplicação.
- **Estrutura do Conteúdo:**
  1. O que é software supply chain e por que ela falha.
  2. Dependências diretas e transitivas, versões e lockfiles.
  3. Typosquatting, dependency confusion e pacotes maliciosos.
  4. Componentes desatualizados e vulnerabilidades conhecidas (CVEs).
  5. Controles: inventário de dependências, verificação de integridade e atualização contínua.

### Notebook 10 — Cryptographic Failures (A04)
- **Objetivo:** Detectar dados sensíveis expostos por criptografia ausente, fraca ou mal aplicada.
- **Estrutura do Conteúdo:**
  1. Dados sensíveis em repouso e em trânsito.
  2. Algoritmos obsoletos e modos de operação inseguros.
  3. Erros de geração e gestão de chaves e IVs.
  4. Hashing inadequado de senhas e dados derivados.
  5. Verificação: TLS, armazenamento de segredos e classificação de dados.

### Notebook 11 — Injection (A05)
- **Objetivo:** Compreender injeção como falha de separação entre dados e comandos.
- **Estrutura do Conteúdo:**
  1. SQL injection e prepared statements.
  2. Command injection e execução de processos pelo servidor.
  3. LDAP, NoSQL e template injection.
  4. Cross-site scripting como forma de injeção no navegador.
  5. Prevenção: parameterização, validação e encoding contextual.

### Notebook 12 — Insecure Design (A06)
- **Objetivo:** Reconhecer riscos que nascem de decisões de design, não de erros de implementação.
- **Estrutura do Conteúdo:**
  1. Diferença entre insecure design e implementation flaw.
  2. Ausência de limites de negócio: fluxos de recuperação de senha e checkout.
  3. Abuse cases e modelagem de ameaças no design.
  4. Segregação de responsabilidades e trust boundaries.
  5. Padrões de design seguro e revisão de arquitetura.

### Notebook 13 — Authentication Failures (A07)
- **Objetivo:** Identificar fragilidades em autenticação e gestão de sessão.
- **Estrutura do Conteúdo:**
  1. Credential stuffing, brute force e password spraying.
  2. Políticas fracas de senha e ausência de rate limiting.
  3. MFA, recuperação de conta e fluxos de reset.
  4. Session fixation, expiração e revogação de sessão.
  5. Prevenção: MFA, proteção contra automação e monitoramento de falhas.

### Notebook 14 — Software or Data Integrity Failures (A08)
- **Objetivo:** Entender riscos de integridade em código, pipelines e dados serializados.
- **Estrutura do Conteúdo:**
  1. Integridade de artefatos e atualizações não assinadas.
  2. CI/CD como vetor de ataque e permissões de pipeline.
  3. Insecure deserialization e objetos não confiáveis.
  4. Assinatura de artefatos e verificação de origem.
  5. Prevenção: checksums, assinatura e revisão de dependências.

### Notebook 15 — Security Logging and Alerting Failures (A09)
- **Objetivo:** Garantir que eventos de segurança sejam registrados, protegidos e monitorados.
- **Estrutura do Conteúdo:**
  1. Eventos que precisam ser logados: autenticação, autorização e mudanças críticas.
  2. Log injection e proteção dos próprios logs.
  3. Retenção, integridade e acesso aos logs.
  4. Alertas eficazes versus ruído operacional.
  5. Detecção de ataques e resposta a incidentes baseada em logs.

### Notebook 16 — Mishandling of Exceptional Conditions (A10)
- **Objetivo:** Tratar erros e condições excepcionais sem expor dados nem permitir estados inseguros.
- **Estrutura do Conteúdo:**
  1. Fail open versus fail closed.
  2. Tratamento de exceções e mensagens de erro seguras.
  3. Estados inconsistentes após falhas parciais.
  4. Timeouts, retries e limites de recursos.
  5. Prevenção: tratamento centralizado de erros e testes de condições anormais.

### Notebook 17 — API Security (OWASP API Top 10)
- **Objetivo:** Aplicar o OWASP API Security Top 10 a APIs REST e GraphQL.
- **Estrutura do Conteúdo:**
  1. Especificidades de segurança em APIs e exposição de objetos.
  2. Broken object level authorization (BOLA) e broken function level authorization.
  3. Excessive data exposure e mass assignment.
  4. Rate limiting, resource consumption e falta de inventário de APIs.
  5. Autenticação de APIs, tokens e boas práticas de gateway.

### Notebook 18 — Client-Side Security (XSS, CSRF, CORS, clickjacking)
- **Objetivo:** Compreender ataques e defesas que ocorrem no navegador do usuário.
- **Estrutura do Conteúdo:**
  1. XSS: stored, reflected e DOM-based.
  2. Content Security Policy e Trusted Types.
  3. CSRF e tokens anti-CSRF, SameSite cookies.
  4. CORS: origens permitidas e erros comuns de configuração.
  5. Clickjacking, frame-ancestors e headers de proteção.

# Fase 2 — Validação ofensiva leve

### Notebook 19 — Burp Suite and Interception Proxies
- **Objetivo:** Operar um interception proxy para observar e alterar tráfego de aplicações próprias ou autorizadas.
- **Estrutura do Conteúdo:**
  1. Como funciona um interception proxy e o papel do CA de teste.
  2. Configuração de escopo, proxy e certificados no Burp Suite.
  3. Repeater, Intruder e Comparer no fluxo de análise.
  4. Captura de tráfego HTTPS e tráfego de APIs.
  5. Limites éticos e legais: escopo autorizado e registro de evidências.

### Notebook 20 — Request Manipulation and Parameter Testing
- **Objetivo:** Testar entradas e parâmetros de forma sistemática sem recorrer a automação cega.
- **Estrutura do Conteúdo:**
  1. Enumeração de parâmetros de query, body, headers e cookies.
  2. Valores limítrofes, tipos inesperados e campos ocultos.
  3. Bypass de validação client-side e de controles de UI.
  4. HTTP parameter pollution e mass assignment.
  5. Registro de hipóteses, testes e resultados por requisição.

### Notebook 21 — Testing Authentication and Authorization
- **Objetivo:** Verificar se autenticação e autorização resistem a manipulação de identidade e privilégio.
- **Estrutura do Conteúdo:**
  1. Testes de força bruta controlada e política de senhas.
  2. Testes de fluxo de login, MFA e recuperação de conta.
  3. Verificação de IDOR e escalonamento horizontal de privilégios.
  4. Testes de função administrativa e escalonamento vertical.
  5. Testes de expiração, revogação e reutilização de sessão.

### Notebook 22 — Testing Injection and SSRF
- **Objetivo:** Validar injeção e SSRF em ambiente de laboratório com métodos reproduzíveis.
- **Estrutura do Conteúdo:**
  1. Testes de SQL injection com payloads mínimos e observação de respostas.
  2. Testes de command injection e template injection.
  3. Testes de XSS refletido e armazenado.
  4. Testes de SSRF contra destinos internos e metadata endpoints.
  5. Confirmação de impacto, falso positivo e evidência mínima.

### Notebook 23 — Testing Client-Side and APIs
- **Objetivo:** Testar aplicações SPA e APIs além da interface visível.
- **Estrutura do Conteúdo:**
  1. Análise de JavaScript, endpoints e segredos expostos no cliente.
  2. Testes de CORS, CSP e postMessage.
  3. Enumeração de endpoints e métodos de API.
  4. Testes de BOLA e mass assignment em APIs.
  5. Ferramentas de apoio: DevTools, proxies e clientes HTTP.

### Notebook 24 — Evidence, Lab Practice and Reporting
- **Objetivo:** Documentar achados de forma reproduzível, com impacto e recomendação claros.
- **Estrutura do Conteúdo:**
  1. Estrutura de um relatório: resumo, escopo, método e achados.
  2. Escrita de passos de reprodução e evidências.
  3. Classificação de severidade e uso de CVSS.
  4. Recomendações acionáveis para o time de desenvolvimento.
  5. Prática em laboratórios: OWASP Juice Shop, DVWA e WebGoat.

# Fase 3 — Ferramentas

### Notebook 25 — SAST
- **Objetivo:** Entender como análise estática encontra problemas no código-fonte e como interpretar seus resultados.
- **Estrutura do Conteúdo:**
  1. Como funciona SAST: parsing, data flow e taint analysis.
  2. Cobertura, linguagens suportadas e limites da análise.
  3. Integração do SAST no repositório e no pull request.
  4. Triagem de achados e priorização por exploração real.
  5. Métricas de adoção e qualidade dos achados.

### Notebook 26 — DAST
- **Objetivo:** Usar análise dinâmica para testar aplicações em execução.
- **Estrutura do Conteúdo:**
  1. Como funciona DAST e o que ele consegue observar.
  2. Requisitos de ambiente: aplicação acessível, autenticação e dados de teste.
  3. Escopo, crawling e autenticação em scanners DAST.
  4. Limites: cegueira de lógica de negócio e dependência de superfície.
  5. Integração em staging e leitura dos resultados.

### Notebook 27 — SCA and Dependency Scanning
- **Objetivo:** Identificar dependências vulneráveis e gerenciar risco de terceiros.
- **Estrutura do Conteúdo:**
  1. Software Composition Analysis e inventário de dependências.
  2. Fontes de vulnerabilidade: CVE, NVD, GHSA e advisories.
  3. Reachability e priorização de dependências realmente usadas.
  4. Atualização, pinning e política de dependências.
  5. Automação de SCA no pipeline e tratamento de ruído.

### Notebook 28 — Secrets Detection and Management
- **Objetivo:** Evitar que credenciais vazem no código e garantir gestão segura de segredos.
- **Estrutura do Conteúdo:**
  1. Como segredos vazam: commits, logs, imagens e variáveis.
  2. Detecção em repositório, histórico e pipeline.
  3. Rotação e revogação de credenciais expostas.
  4. Secret managers e injeção de segredos em runtime.
  5. Prevenção: pre-commit hooks, scanning contínuo e educação do time.

### Notebook 29 — Container and IaC Scanning
- **Objetivo:** Detectar configurações e componentes inseguros em containers e infraestrutura como código.
- **Estrutura do Conteúdo:**
  1. Camadas de imagem, Dockerfile e boas práticas de build.
  2. Scanning de imagens e vulnerabilidades de pacotes do sistema.
  3. IaC scanning para Terraform e Kubernetes.
  4. Misconfigurations comuns: privilégios, rede e storage público.
  5. Integração no build e políticas de bloqueio.

### Notebook 30 — Scanner Tuning and False Positive Reduction
- **Objetivo:** Calibrar ferramentas para que os achados sejam confiáveis e acionáveis.
- **Estrutura do Conteúdo:**
  1. Falso positivo, falso negativo e custo de cada erro.
  2. Regras, severidade e supressões justificadas.
  3. Baseline, tuning por aplicação e revisão periódica.
  4. Comunicação de resultados ao time de desenvolvimento.
  5. Métricas de precisão e confiança nas ferramentas.

### Notebook 31 — Security Gates in CI/CD
- **Objetivo:** Inserir controles de segurança no pipeline sem travar a entrega.
- **Estrutura do Conteúdo:**
  1. Shift-left e o papel dos gates de segurança.
  2. Gates bloqueantes versus informativos e critérios de falha.
  3. Integração de SAST, SCA, secrets e IaC scanning no pipeline.
  4. Permissões de CI/CD, OIDC e proteção de credenciais.
  5. Exceções, aprovação de risco e evolução dos gates.

### Notebook 32 — AppSec Metrics and Reporting
- **Objetivo:** Medir o programa de AppSec com métricas que orientem decisões.
- **Estrutura do Conteúdo:**
  1. Métricas de processo: cobertura de scanning e adoção de gates.
  2. Métricas de resultado: MTTR, densidade de vulnerabilidades e reincidência.
  3. SLA de correção por severidade.
  4. Dashboards e comunicação para liderança técnica.
  5. Cuidados com métricas que incentivam comportamento errado.

# Fase 4 — Processo

### Notebook 33 — Threat Modeling with STRIDE
- **Objetivo:** Identificar ameaças antes da implementação usando um método estruturado.
- **Estrutura do Conteúdo:**
  1. O que é threat modeling e quando fazer.
  2. Decomposição do sistema: fluxos, ativos e trust boundaries.
  3. STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service e elevation of privilege.
  4. Priorização de ameaças e definição de mitigações.
  5. Documentação e revisão do modelo ao longo do ciclo.

### Notebook 34 — Secure Code Review
- **Objetivo:** Revisar código com foco em segurança de forma eficiente e colaborativa.
- **Estrutura do Conteúdo:**
  1. O que procurar em uma revisão de segurança.
  2. Pontos críticos: entrada, autenticação, autorização, criptografia e logs.
  3. Uso de checklists e padrões seguros por linguagem.
  4. Comunicação de achados em pull requests.
  5. Limites da revisão manual e complemento com ferramentas.

### Notebook 35 — Secure SDLC and NIST SSDF
- **Objetivo:** Integrar segurança em todas as etapas do ciclo de desenvolvimento.
- **Estrutura do Conteúdo:**
  1. Secure SDLC e DevSecOps: princípios e diferenças.
  2. NIST SP 800-218 (SSDF): práticas e grupos de práticas.
  3. Requisitos, design, implementação, verificação e resposta.
  4. Papéis e responsabilidades entre AppSec e desenvolvimento.
  5. Adoção gradual e medição de maturidade.

### Notebook 36 — Vulnerability Management and Remediation SLAs
- **Objetivo:** Gerir vulnerabilidades do achado à correção com prioridade baseada em risco.
- **Estrutura do Conteúdo:**
  1. Ciclo de vida de uma vulnerabilidade: descoberta, triagem, correção e verificação.
  2. Priorização por exploração, exposição e impacto no negócio.
  3. SLAs por severidade e exceções formais.
  4. Comunicação com owners e acompanhamento de prazos.
  5. Métricas de remediação e redução de risco acumulado.

### Notebook 37 — Software Supply Chain Controls (SBOM, SLSA, signing)
- **Objetivo:** Aplicar controles de integridade e rastreabilidade na cadeia de suprimentos de software.
- **Estrutura do Conteúdo:**
  1. SBOM: CycloneDX, SPDX e uso na resposta a incidentes.
  2. Assinatura de artefatos e imagens de container.
  3. SLSA: níveis de garantia e proveniência de build.
  4. Verificação de origem e políticas de admissão.
  5. Rastreabilidade de dependências e resposta a comprometimentos.

### Notebook 38 — Application Incident Response and Developer Enablement
- **Objetivo:** Apoiar a resposta a incidentes de aplicação e capacitar desenvolvedores em segurança.
- **Estrutura do Conteúdo:**
  1. Incident response aplicado a vulnerabilidades exploradas.
  2. Triagem, contenção, erradicação e recuperação.
  3. Coordenação com times de produto, infraestrutura e jurídico.
  4. Post-mortem, causa raiz e ações preventivas.
  5. Developer enablement: treinamento, champions e documentação segura.

---

# Orientações gerais para utilização dos notebooks

**Padrão de produção dos materiais:**

1. Utilizar a documentação oficial da OWASP (Top 10 2025, ASVS 5.0, API Top 10 e cheat sheets) como fonte principal.
2. Manter cada material restrito ao assunto do notebook.
3. Explicar os fundamentos antes dos conceitos avançados.
4. Apresentar exemplos práticos de código, requisições HTTP e configuração.
5. Incluir cenários reais de vulnerabilidade e de revisão de código quando pertinentes.
6. Utilizar terminologia técnica em inglês, explicando em português.
7. Não introduzir assuntos de fases futuras sem necessidade para compreender o assunto atual.

**Público-alvo:** estudante em preparação para uma vaga de AppSec Engineer, com foco em fundamentos de segurança de aplicações, vulnerabilidades web/API, ferramentas de análise e processo de desenvolvimento seguro.

**Critério de qualidade:** cada notebook deve permitir que o estudante compreenda o assunto central e saiba reconhecê-lo em código, requisições ou configurações reais, sem precisar de um material que tente ensinar várias disciplinas ao mesmo tempo.
