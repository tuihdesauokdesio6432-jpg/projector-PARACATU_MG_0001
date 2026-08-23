#!/usr/bin/env python3
"""
Replace the Instituto Consulpam header (#topo) and footer (#rodape) blocks with
a Fundação CETREDE-branded header + footer across all internal HTML pages of the
public site. Also updates textual references to "Consulpam" / old contest info.
"""
from bs4 import BeautifulSoup
from pathlib import Path

PUB = Path('/app/frontend/public')
FILES = [
    'inscricao.html',
    'confirmar-dados.html',
    'comprovante.html',
    'pagamento.html',
]

# --- New CETREDE header (self-contained; matches home page palette) ---
CETREDE_HEADER = """
<div id="cetrede-header" style="background:#ffffff;padding:0;border-bottom:3px solid #00AFEF;font-family:'Trebuchet MS',Arial,Helvetica,sans-serif;">
  <div style="max-width:1200px;margin:0 auto;padding:18px 20px;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;">
    <a href="/" style="display:inline-flex;align-items:center;text-decoration:none;">
      <img src="/assets/cetrede-logo.png" alt="Fundação Cetrede" style="height:56px;width:auto;display:block;">
    </a>
    <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
      <a href="/" style="display:inline-block;background:#00AFEF;color:#fff;text-decoration:none;font-weight:700;font-size:13px;letter-spacing:.5px;text-transform:uppercase;padding:12px 22px;border-radius:6px;">Seleções e Concursos</a>
    </div>
  </div>
  <nav style="background:#000625;">
    <ul style="max-width:1200px;margin:0 auto;padding:12px 20px;list-style:none;display:flex;gap:22px;flex-wrap:wrap;">
      <li style="float:none;"><a href="/" style="color:#fff;text-decoration:none;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.4px;padding:6px 0;">Início</a></li>
      <li style="float:none;"><a href="/" style="color:#fff;text-decoration:none;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.4px;padding:6px 0;">Concurso</a></li>
      <li style="float:none;"><a href="/inscricao.html" style="color:#fff;text-decoration:none;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.4px;padding:6px 0;">Inscrição</a></li>
      <li style="float:none;"><a href="/docs/29062026-edital-001-2026.pdf" style="color:#fff;text-decoration:none;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.4px;padding:6px 0;">Edital</a></li>
      <li style="float:none;"><a href="/docs/29062026-cronograma-atividades.pdf" style="color:#fff;text-decoration:none;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.4px;padding:6px 0;">Cronograma</a></li>
    </ul>
  </nav>
</div>
"""

# --- New CETREDE footer ---
CETREDE_FOOTER = """
<div id="cetrede-footer" style="background:#000625;color:#e6f4ff;padding:34px 20px 24px;margin-top:40px;font-family:'Trebuchet MS',Arial,Helvetica,sans-serif;">
  <div style="max-width:1200px;margin:0 auto;display:flex;gap:40px;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;">
    <div style="flex:1 1 260px;min-width:220px;">
      <img src="/assets/cetrede-logo.png" alt="Fundação Cetrede" style="height:60px;width:auto;display:block;background:#fff;padding:8px 12px;border-radius:6px;">
      <p style="margin:14px 0 0;font-size:13px;line-height:1.6;color:#c9d6f5;">Fundação de Apoio à Cultura, à Pesquisa e ao Desenvolvimento Institucional Científico e Tecnológico.</p>
    </div>
    <div style="flex:1 1 260px;min-width:220px;">
      <h3 style="color:#fff;font-size:15px;margin:0 0 12px;text-transform:uppercase;letter-spacing:.5px;">Concurso Público</h3>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#c9d6f5;">Prefeitura Municipal de Forquilha (CE)</p>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#c9d6f5;">Edital Nº 001/2026 — 25 de Junho de 2026</p>
      <p style="margin:0;font-size:13px;line-height:1.6;color:#c9d6f5;">Organizadora: Fundação CETREDE</p>
    </div>
    <div style="flex:1 1 260px;min-width:220px;">
      <h3 style="color:#fff;font-size:15px;margin:0 0 12px;text-transform:uppercase;letter-spacing:.5px;">Contato</h3>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#c9d6f5;">Av. da Universidade, 2932 — Benfica</p>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#c9d6f5;">Fortaleza — CE</p>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#c9d6f5;">CNPJ: 07.343.184/0001-06</p>
      <p style="margin:0;font-size:13px;line-height:1.6;color:#c9d6f5;">Atendimento: seg. a sex., 8h às 17h</p>
    </div>
  </div>
  <div style="max-width:1200px;margin:22px auto 0;padding-top:16px;border-top:1px solid rgba(255,255,255,.12);font-size:12px;color:#8fa8d6;text-align:center;">
    © 2026 Fundação CETREDE — Todos os direitos reservados.
  </div>
</div>
"""


def replace_block(soup, block_id, replacement_html):
    tag = soup.find(id=block_id)
    if not tag:
        return False
    new = BeautifulSoup(replacement_html, 'html.parser')
    tag.replace_with(new)
    return True


def process(file_path: Path):
    html = file_path.read_text(encoding='utf-8')

    # Textual updates (broad find/replace before DOM parse)
    replacements = [
        ('Consulpam - Consultoria Público - Privada', 'Fundação CETREDE'),
        ('CONSULPAM', 'CETREDE'),
        ('Consulpam', 'Cetrede'),
        ('consulpam', 'cetrede'),
        ('Instituto Cetrede', 'Fundação CETREDE'),
        ('Instituto CETREDE', 'Fundação CETREDE'),
        # Legacy contest wording sanity
        ('GUARDA CIVIL MUNICIPAL - PREFEITURA MUNICIPAL DE FORQUILHA-CE',
         'PREFEITURA MUNICIPAL DE FORQUILHA-CE'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    soup = BeautifulSoup(html, 'lxml')

    hdr_ok = replace_block(soup, 'topo', CETREDE_HEADER)
    ftr_ok = replace_block(soup, 'rodape', CETREDE_FOOTER)

    # Also update <title>
    if soup.title:
        soup.title.string = 'Concurso Público — Prefeitura de Forquilha-CE | Fundação CETREDE'

    file_path.write_text(str(soup), encoding='utf-8')
    print(f'{file_path.name}: header={hdr_ok} footer={ftr_ok}')


if __name__ == '__main__':
    for name in FILES:
        process(PUB / name)
    print('Done.')
