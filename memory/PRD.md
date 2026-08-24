# PRD — Portal PSS SEED 2026 (NC/UFPR) + Painel Admin

## Original Problem Statement
Clone de repositório GitHub (FastAPI + React + MongoDB). Reconfigurar portal de inscrição existente para o **Processo Seletivo Simplificado — PSS SEED 2026** (Secretaria de Estado da Educação do Paraná, banca NC/UFPR). Rebranding completo do fluxo público e painel admin, campos dinâmicos complexos (Núcleo Regional de Educação, Municípios, Provas, Funções), segunda inscrição opcional, preço dinâmico por nº de inscrições, layouts de impressão de comprovante, e nova home institucional.

## Idioma do Usuário
Português (pt-BR)

## Arquitetura
- **Backend**: FastAPI + MongoDB (`/api/*`) — `server.py`, `admin_routes.py`.
- **Frontend público**: HTML/JS/CSS estáticos em `/app/frontend/public/*.html` (sem bundler).
- **Painel Admin**: React (CRA) em `/donaspainel`. `/farpapainel` redireciona para `/`.
- **Integrações**: Telegram Bot API (notificações), PIX EMV (geração de código).

## ⚠️ MUDANÇA DE PROJETO (24/08/2026)
O projeto foi redirecionado: **NÃO é mais o PSS SEED 2026 (PR)**. Agora é o **Concurso Público do Município de Paracatu/MG - Edital nº 02/2026** (banca IBGP).
- Nova `index.html` (home): página do concurso Paracatu/MG, fornecida pelo usuário (layout IBGP). Todos os links externos removidos/neutralizados. Botão "Realizar inscrição" aponta para `inscricao.html` (fluxo de inscrição atual). Script de tracking `/api/track/access` e CSP `connect-src 'self'` mantidos.
- **PENDENTE**: rebranding das demais páginas do fluxo (`inscricao.html`, `confirmar-dados.html`, `pagamento.html`, `comprovante.html`, `confirmacao.html`) e do painel admin ainda mostram "PSS SEED 2026". Aguardando instrução do usuário.

## Páginas Públicas
- `/` — index.html (home concurso Paracatu/MG — layout IBGP, links externos removidos)
- `/inscricao` — inscricao.html (formulário dinâmico: NRE, Municípios, Prova, Função, 2ª inscrição opcional)
- `/confirmar-dados` — confirmar-dados.html
- `/pagamento` — pagamento.html (PIX + QR, print A4 single-page)
- `/comprovante` — comprovante.html
- `/confirmacao` — confirmacao.html

## Credenciais
- Admin `/donaspainel`: `donas` / `Seinao10@@`

## Preços
- 1 inscrição: R$ 68,00 | 2 inscrições: R$ 88,00

## Implementado
- **[24/08/2026]** **Modal de aviso na home**: injetado em `index.html` (logo NC/UFPR, "Aviso Importante", data de encerramento 24/08/2026 23h59, botão "OK, entendi"). Abre ao carregar; fecha por botão, clique fora ou ESC. Verificado por screenshot.
- Rebranding completo para PSS SEED 2026 / NC/UFPR (home, fluxo, painel admin, login bg).
- Campos dinâmicos: NRE (32 regiões), Municípios (até 2), Prova + Função (ÁREA BÁSICA / EDUCAÇÃO PROFISSIONAL), Cidade de Prova.
- Bloco "2ª Inscrição" opcional com campos duplicados independentes.
- Preço dinâmico (R$ 68 / R$ 88).
- Correção do botão "Inscrever" (validação com campos removidos) + avisos visuais de campos obrigatórios.
- Confirmação e comprovante refletem dados da 1ª e 2ª inscrição dinamicamente.
- Print A4 single-page em pagamento.html com cabeçalho/rodapé print-only.
- Título Telegram: "NOVA INSCRIÇÃO — PSS SEED 2026".
- 20 inscrições realistas seedadas com status de pagamento variados.

## Backlog / Próximos Passos
- Nenhuma tarefa pendente específica; aguardar próximas solicitações do usuário.

## Notas Técnicas
- Não editar o build React para páginas públicas; elas vivem em `/app/frontend/public/*.html`.
- Editar HTML público depende de Hot Reload / restart do frontend.
