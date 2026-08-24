"""Gera 30 inscrições aleatórias com dados realistas e executa o fluxo completo
de PIX (gerado -> copiado -> baixado) chamando os endpoints públicos reais."""
import json
import random
import secrets
import time
import requests

BASE = "https://pss-seed.preview.emergentagent.com"

CARGOS = {
    "02": ["101 - AUXILIAR DE SERVIÇOS DE EDUCAÇÃO", "102 - CANTINEIRO", "103 - PEDREIRO", "104 - VIGIA", "201 - AUXILIAR DE SERVIÇOS GERAIS", "202 - BOMBEIRO HIDRÁULICO", "203 - ELETRICISTA", "205 - MECÂNICO DE VEÍCULOS E MÁQUINAS PESADAS", "208 - MOTORISTA DE VEÍCULOS LEVES", "210 - OPERADOR DE MÁQUINAS LEVES", "213 - PINTOR", "214 - SOLDADOR", "301 - ALMOXARIFE", "302 - AUXILIAR ADMINISTRATIVO", "304 - AUXILIAR DE SECRETARIA", "305 - OFICIAL ADMINISTRATIVO", "401 - TÉCNICO EM ANÁLISES CLÍNICAS", "403 - TÉCNICO EM ENFERMAGEM", "404 - TÉCNICO EM RADIOLOGIA", "501 - ADMINISTRADOR", "502 - ADVOGADO", "503 - ARQUITETO", "505 - ASSISTENTE SOCIAL", "508 - ENFERMEIRO", "510 - ENGENHEIRO CIVIL", "512 - FARMACÊUTICO", "514 - FISIOTERAPEUTA", "516 - PROFESSOR DE ENSINO BÁSICO I PEB I", "519 - PSICÓLOGO", "521 - FONOAUDIÓLOGO", "603 - MÉDICO - CLÍNICA MÉDICA", "605 - MÉDICO - CARDIOLOGIA", "614 - MÉDICO - PEDIATRIA", "616 - MÉDICO - PSIQUIATRIA"],
    "03": ["301 - GUARDA CIVIL MUNICIPAL"],
}
CONCURSO_TXT = {
    "02": "CONCURSO PÚBLICO DO MUNICÍPIO DE PARACATU/MG - EDITAL Nº 02/2026",
    "03": "CONCURSO PÚBLICO DA GUARDA CIVIL MUNICIPAL DE PARACATU/MG - EDITAL Nº 03/2026",
}

def tier_valor(ed, codigo):
    d = int(codigo[0]) if codigo and codigo[0].isdigit() else 0
    if ed == "03":
        return 90
    if d <= 2:
        return 70
    if d <= 4:
        return 90
    return 110

# ---- geradores de dados reais ----
NOMES = ["ANA", "BRUNO", "CARLA", "DANIEL", "EDUARDA", "FELIPE", "GABRIELA", "HENRIQUE",
         "ISABELA", "JOÃO", "KARINA", "LUCAS", "MARIANA", "NATÁLIA", "OTÁVIO", "PAULA",
         "RAFAEL", "SABRINA", "THIAGO", "VANESSA", "WELLINGTON", "YASMIN", "CAMILA", "RENATO",
         "FERNANDA", "GUSTAVO", "LARISSA", "MARCELO", "PATRÍCIA", "RODRIGO"]
SOBRENOMES = ["SILVA", "SANTOS", "OLIVEIRA", "SOUZA", "PEREIRA", "COSTA", "RODRIGUES", "ALMEIDA",
              "NASCIMENTO", "LIMA", "ARAÚJO", "FERREIRA", "GOMES", "MARTINS", "ROCHA", "CARVALHO",
              "RIBEIRO", "ALVES", "MONTEIRO", "BARBOSA", "MENDES", "FREITAS", "CARDOSO", "TEIXEIRA"]
BAIRROS = ["CENTRO", "PARACATUZINHO", "AMOROSO COSTA", "BELA VISTA", "SANTA RITA",
           "ALTO DA COLINA", "NOSSA SENHORA DE FÁTIMA", "SANTO ANTÔNIO", "ESPLANADA", "JK"]
RUAS = ["RUA DIREITA", "AVENIDA OLEGÁRIO MACIEL", "RUA DA CONTAGEM", "RUA GERALDO PORFÍRIO",
        "AVENIDA BRASÍLIA", "RUA DOM SILVÉRIO", "RUA MESTRE ABEL", "AVENIDA JK",
        "RUA CORONEL JOSÉ MARIA", "RUA ALTINO GUIMARÃES"]
ESCOL = ["ENSINO FUNDAMENTAL", "ENSINO MÉDIO", "ENSINO TÉCNICO", "ENSINO SUPERIOR", "PÓS-GRADUAÇÃO"]
CIVIL = ["SOLTEIRO(A)", "CASADO(A)", "DIVORCIADO(A)", "VIÚVO(A)"]
SEXO = ["Masculino", "Feminino"]

def gen_cpf():
    n = [random.randint(0, 9) for _ in range(9)]
    s = sum((10 - i) * n[i] for i in range(9))
    d1 = (s * 10) % 11
    d1 = 0 if d1 == 10 else d1
    n.append(d1)
    s = sum((11 - i) * n[i] for i in range(10))
    d2 = (s * 10) % 11
    d2 = 0 if d2 == 10 else d2
    n.append(d2)
    return "".join(map(str, n))

def fmt_cpf(c):
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

def gen_phone():
    return f"(38) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

sess = requests.Session()
ok = 0
fail = 0
for i in range(30):
    ed = random.choices(["02", "03"], weights=[85, 15])[0]
    cargo = random.choice(CARGOS[ed])
    codigo = cargo.split(" - ")[0]
    valor = tier_valor(ed, codigo)
    nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"
    cpf = gen_cpf()
    first = nome.split()[0].lower()
    email = f"{first}.{random.choice(SOBRENOMES).lower()}{random.randint(1,999)}@gmail.com"
    protocolo = "".join(str(secrets.randbelow(10)) for _ in range(10))
    concurso = CONCURSO_TXT[ed]

    payload = {
        "concurso": concurso, "certame": ed, "cargo": cargo,
        "funcao": cargo, "valor": valor, "protocolo": protocolo,
        "cpf": fmt_cpf(cpf), "nome": nome, "email": email,
        "dataNascimento": f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{random.randint(1970,2004)}",
        "sexo": random.choice(SEXO), "nacionalidade": "BRASILEIRA",
        "tipoDocumento": "RG", "cep": f"38600-{random.randint(0,999):03d}",
        "endereco": random.choice(RUAS), "numero": str(random.randint(10, 2500)),
        "complemento": "", "bairro": random.choice(BAIRROS),
        "estado": "MINAS GERAIS", "cidade": "PARACATU",
        "telefone": gen_phone(), "escolaridade": random.choice(ESCOL),
        "estadoCivil": random.choice(CIVIL), "filhosMenores": str(random.randint(0, 3)),
        "leiPreto": "Não", "guardaSabados": "Sim", "aceitaWhatsapp": "Sim",
        "localProva": "PARACATU/MG", "segundaInscricao": "Não",
        "stage": "inscricao_finalizada", "finalized": True,
    }

    extra = {
        "cpf": fmt_cpf(cpf), "nome": nome, "email": email,
        "cargo_codigo": codigo, "cargo_titulo": cargo,
        "codigo": codigo, "titulo": cargo,
        "protocolo": protocolo, "valor": valor, "concurso": concurso,
        "vaga_nome": concurso, "edital": ed, "localidade": "PARACATU/MG",
    }

    try:
        r = sess.post(f"{BASE}/api/inscricoes/submit", data={"payload": json.dumps(payload)}, timeout=30)
        if r.status_code != 200:
            print(f"[{i+1}] submit FAIL {r.status_code}: {r.text[:120]}")
            fail += 1
            continue
        # fluxo PIX completo
        for path in ("pix-generated", "pix-copied", "pix-downloaded"):
            rr = sess.post(f"{BASE}/api/track/{path}", json={"extra": extra}, timeout=30)
            if rr.status_code != 200:
                print(f"[{i+1}] {path} FAIL {rr.status_code}: {rr.text[:120]}")
        ok += 1
        print(f"[{i+1}] OK {nome} | ed{ed} {codigo} R${valor} | proto {protocolo}")
    except Exception as e:
        fail += 1
        print(f"[{i+1}] EXC: {e}")
    time.sleep(0.15)

print(f"\n=== CONCLUÍDO: {ok} inscrições OK, {fail} falhas ===")
