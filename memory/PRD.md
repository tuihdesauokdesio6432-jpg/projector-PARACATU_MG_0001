# PRD — Site Consulpam + Painel Admin

## Original Problem Statement
Clone de repositório GitHub (FastAPI + React + MongoDB). Preservar painel admin `/donaspainel` + backend; substituir site público pelo site clonado da Consulpam. Concurso público — inicialmente Guarda Civil Municipal de Sobral/CE, migrado para **Prefeitura Municipal de Forquilha/CE** — Edital 001/2026. Integrar formulários públicos ao backend (cadastros, tracking, PIX, Telegram).

## Idioma do Usuário
Português (pt-BR)

## Arquitetura
- **Backend**: FastAPI + MongoDB (`/api/*`).
- **Frontend público**: HTML estáticos em `/app/frontend/public/*.html`, roteados via middleware do `craco.config.js`.
- **Painel Admin**: React estático buildado em `/app/frontend/public/donaspainel/` — preservado do repo original.
- **Integrações**: Telegram Bot API (notificações), PIX EMV (geração de código).

## Páginas Públicas
- `/` — index.html (home — página institucional da Fundação CETREDE com o edital do concurso de Forquilha e botão "Fazer Inscrição")
- `/inscricao` — inscricao.html (formulário)
- `/confirmar-dados` — confirmar-dados.html (revisão)
- `/comprovante` — comprovante.html (recibo)
- `/pagamento` — pagamento.html (PIX + QR)

## Credenciais
- Admin `/donaspainel`: `donas` / `Seinao10@@`

## Implementado
- **[15/08/2026]** **Vistoria + Atualização do Painel Administrativo para Forquilha**:
  - Bundle React admin (`donainel/main.fda9cfa5.js` e `donainel/index.html`): todas as 5 ocorrências de "Guarda Civil Forquilha-CE" trocadas por "Prefeitura de Forquilha-CE" (sidebar, header do dashboard, título do relatório, `document.title` da aba, splash de brand).
  - Backend `admin_routes.py`: default do `pix_nome` mudado para "PREFEITURA DE FORQUILHA-CE" (linha 1496); default do `telegram_titulo` mudado para "NOVA INSCRIÇÃO PREFEITURA DE FORQUILHA-CE" (linha 1627).
  - Backend `server.py` linha 159: default do campo `concurso` em novas inscrições atualizado para "PREFEITURA MUNICIPAL DE FORQUILHA-CE — EDITAL 001/2026".
  - MongoDB `settings.main` atualizado via script: `pix_cidade` = "Forquilha CE" (era "Sobral CE"), `pix_nome` = "Concurso Prefeitura Forquilha" (era "Concurso GCM Sobral"), acrescentado `telegram_titulo` correto. Chave PIX (danielmmm950@gmail.com) e credenciais Telegram preservadas.
  - **Limpeza de dados legados**: removida 1 inscrição de teste do concurso anterior (Breno Levy — Sobral — R$ 179,00), zerando os KPIs do dashboard para começar limpo o novo ciclo de Forquilha.
- **[15/08/2026]** Home enxugada: removi card "Taxa de Inscrição" e botão "Baixar Edital em PDF" do hero, e linha "Forma de Pagamento" + 4 botões de docs do card "Informações do Concurso".

- **[15/08/2026]** **Dropdown de Cargos + Taxa Dinâmica**:
  - 78 cargos do Concurso da Prefeitura de Forquilha (CE) adicionados ao select em `inscricao.html`, agrupados em 3 optgroups por nível/turno/taxa: Fundamental-Tarde (R$ 80,00, 18 cargos), Médio-Tarde (R$ 100,00, 30 cargos incluindo 14 vagas de Agente Comunitário de Saúde MA01–MA48), Superior-Manhã (R$ 125,00, 30 cargos).
  - Cada `<option>` traz `value` numérico (001–078), `data-valor` (fee) e `data-turno`, capturados via `valorOfCargo()` e `turnoOfCargo()` em `__collectFormData()` e persistidos em sessionStorage como `d.valor` e `d.turno`.
  - `pagamento.html` agora lê `d.valor` para gerar PIX com o valor correto por cargo (fallback R$ 100,00 se ausente). Placeholder inicial da caixa "Valor da Inscrição" mudado de R$ 179,00 para R$ —.

- **[15/08/2026]** **Cabeçalho + Rodapé CETREDE aplicado nas páginas internas do fluxo**:
  - `inscricao.html`, `confirmar-dados.html`, `comprovante.html`, `pagamento.html`, `confirmacao.html` — todos com o novo cabeçalho (logo Fundação Cetrede + botão "Seleções e Concursos" + menu navy `#000625` com Início / Concurso / Inscrição / Edital / Cronograma) e rodapé (dark navy com colunas: logo/descrição CETREDE, "Concurso Público" (Prefeitura Municipal de Forquilha CE, Edital 001/2026, Organizadora: Fundação CETREDE) e Contato + CNPJ 07.343.184/0001-06).
  - Logo Fundação Cetrede salvo em `/app/frontend/public/assets/cetrede-logo.png` (extraído do artifact enviado pelo usuário) e referenciado externamente para reduzir tamanho dos arquivos.
  - Logo do Instituto Consulpam removido do interior do card de `comprovante.html` — substituído pelo logo CETREDE. Título do recibo agora exibe "Fundação CETREDE" em vez de "Cetrede".
  - Todas as menções a "Consulpam / CONSULPAM" removidas dos HTMLs públicos.
  - Concurso: "PREFEITURA MUNICIPAL DE FORQUILHA-CE (EDITAL Nº 001/2026 - CONCURSO PÚBLICO)" (removido "GUARDA CIVIL MUNICIPAL" do label do concurso; o campo dinâmico "Cargo" ainda pode exibir GUARDA CIVIL MUNICIPAL para inscrições passadas — está atrelado ao valor salvo no MongoDB).
  - Titles das páginas atualizados para "Concurso Público — Prefeitura de Forquilha-CE | Fundação CETREDE".
  - Script auxiliar em `/app/scripts/apply_cetrede_header.py` para reaplicação futura.
- **[15/08/2026]** **Rebranding Forquilha/CE na Home**:
  - Nova home `/` = página da Fundação CETREDE com edital "Concurso Público da Prefeitura Municipal de Forquilha (CE)".
  - Botão "Fazer Inscrição" (`#00AFEF`, alinhado à esquerda) injetado logo após o parágrafo do EDITAL Nº 001/2026, aponta para `/inscricao.html`.
  - Todos os links externos (menu, footer, PDFs externos, scripts, iframes) foram removidos/neutralizados.
  - Link do EDITAL redirecionado para PDF local `/docs/29062026-edital-001-2026.pdf`.
  - Sobral → Forquilha em todos os textos.
- **[19/07/2026]** Correção de responsividade mobile: CSS `<style id="mobile-fix">` refinado nos 5 HTMLs.
- Integração completa `POST /api/inscricoes/submit`, tracking PIX (generated/copied/downloaded), Telegram notifications.
- PIX BR Code gerado via `pix_generator.py`.
- Botão "voltar" na pág. pagamento; cabeçalho oficial em todas as pág.

## Backlog / Próximos Passos (P2)
- **Cargo dropdown**: O select em `inscricao.html` ainda oferece apenas "001 - GUARDA CIVIL MUNICIPAL" como opção de cargo. Atualizar com os cargos reais do concurso de Forquilha quando o edital detalhar todos.
- Fluxo end-to-end de teste real com submissão de inscrição + geração PIX + notificação Telegram (validar com os novos cabeçalhos).
- Melhorar UX do menu (agora scrollável horizontalmente no mobile).
- Testar em tablet (768px) — pode precisar breakpoint intermediário.
