# PRD — Portal de Inscrições IBGP (Concurso Paracatu/MG)

## ⚠️ PROJETO ATUAL (atualizado 24/08/2026)
NÃO é mais o PSS SEED 2026 (PR). Agora é o **Concurso Público do Município de Paracatu/MG** (banca IBGP), com DOIS editais:
- **Edital nº 02/2026** — Concurso Público do Município de Paracatu/MG (68 cargos)
- **Edital nº 03/2026** — Guarda Civil Municipal de Paracatu/MG (cargo 301)

## Idioma do usuário: pt-BR (responder sempre em português)

## Arquitetura
- Frontend público: HTML/JS/CSS vanilla em `/app/frontend/public/*.html` (sem bundler)
- Admin: React em `/donaspainel`
- Backend: FastAPI (`server.py`, `admin_routes.py`), MongoDB
- Rotas API prefixo `/api`

## Páginas Públicas
- `index.html` — Home Paracatu/MG (layout IBGP). Título desceu (margin-top 40px), 2 cards CENTRALIZADOS lado a lado (Edital 02 e 03), sem título "OUTROS CERTAMES", sem links externos. Cards inteiros clicáveis → `edital-02.html` / `edital-03.html`. Ambos cards com mesma data (27/07/26–25/08/26, "1 dias"). Tracking `/api/track/access` + CSP `connect-src 'self'`.
- `edital-02.html` / `edital-03.html` — Páginas de detalhe do concurso. Card OUTROS removido, rodapé IBGP mantido. CARGO/EDITAL/RESULTADOS iniciam RECOLHIDOS (toggle JS próprio, sem Bootstrap JS). Botão "Realizar inscrição" (abaixo da Data da Prova) → `inscricao.html?edital=02` / `?edital=03`.
- Fluxo: `inscricao.html`, `confirmar-dados.html`, `pagamento.html`, `comprovante.html`, `confirmacao.html`

## Cabeçalho/Rodapé do fluxo (24/08/2026)
- Cabeçalho antigo NC/UFPR (gov.br + banner PSS SEED) REMOVIDO das 5 páginas.
- Novo cabeçalho IBGP (barra branca: logo IBGP CSS + CONCURSOS + "Área do Candidato" vermelho) + brasão Paracatu (`/assets/paracatu-brasao.png`) + "MUNICÍPIO DE PARACATU/MG".
- **2 variantes de subtítulo** conforme edital, com PERSISTÊNCIA via sessionStorage (`pss_edital`) a partir do param `?edital=02/03`.
- Rodapé único IBGP vermelho (IBGP CONCURSOS / contato@ibgp.org.br / Avenida do Contorno, 1480 - Floresta / Mapa Site: Certames) — bloco `#pss-footer-wrap`.

## Formulário inscricao.html — Seleção de Cargo (24/08/2026)
- Sistema antigo (NRE→Municípios→Prova→Função + 2ª inscrição) REMOVIDO.
- Agora só 2 selects: **Certame** (id=certame, name=certame) e **CARGO** (id=cargoSel, name=cargoSel).
- Cargos embutidos por edital (JSON no script). Certame pré-selecionado do sessionStorage/param.
- `__collectFormData`: concurso=texto do certame, certame=02/03, cargo=texto do cargo, funcao=cargo, valor=data-valor do cargo. nre/municipios/prova/2ª-inscrição zerados (compat).
- **VALOR (PENDENTE CONFIRMAÇÃO)**: regra provisória por prefixo do código do cargo — 1xx/2xx=R$70, 3xx/4xx=R$90, 5xx/6xx=R$110. Vai direto ao PIX. Aguardando tabela oficial do usuário.

## key DB schema
- `cadastros`, `inscricoes` {cpf,cargo,concurso,valor,pix_status,status}, `settings`, `events`, `accesses`

## Credenciais admin
- Login: `donas` / Senha: `Seinao10@@` (painel `/donaspainel`)

## Pendências / Backlog
- CONFIRMAR regra de preço por cargo (P0 — afeta pagamento PIX)
- Textos internos do formulário ainda citam "NC/UFPR"/"PSS SEED" (ex.: "Aceita receber do NC/UFPR..."), fora do escopo de cabeçalho/rodapé — rebranding do conteúdo interno pendente.
- Backend pode precisar mapear certame→edital/valores server-side (validação de preço).

## Deploy
- Usuário faz deploy em VPS separada via "Save to Github" → outro agente faz git pull.
