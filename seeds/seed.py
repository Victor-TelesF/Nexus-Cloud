#!/usr/bin/env python
"""Carga sintética transacional do banco Nexus Cloud.

Uso local: uv run --env-file .env python seeds/seed.py --init-schema.
A conexão utiliza DATABASE_URL, PG* ou POSTGRES_* do Compose.
--init-schema cria o modelo somente quando o schema nexus está vazio ou ausente.
Registros existentes nunca são sobrescritos, nem sequências reiniciadas.
"""

from __future__ import annotations

import argparse
import calendar
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import sys

import psycopg
from psycopg import sql


VERSION = 2
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / 'sql' / 'models' / 'model.sql'
COUNTS = dict(clientes=1000, servico=20, contratos=5000, pagamentos=30000, servidores=30)
COLUMNS = {
    "clientes": ("id", "nome_empresa", "setor", "cidade", "estado", "data_cadastro"),
    "servico": ("id", "nome_servico", "categoria", "preco_mensal", "custo_mensal", "ativo"),
    "contratos": ("id", "id_cliente", "id_servico", "data_inicio", "data_fim", "status"),
    "pagamentos": ("id", "id_contrato", "data_vencimento", "data_pagamento", "valor", "status"),
    "servidores": ("id", "nome_servidor", "regiao", "capacidade_gb", "custo_mensal", "status"),
}
TYPES = {
    "clientes": ("bigint", "character varying", "character varying", "character varying", "character varying", "date"),
    "servico": ("bigint", "character varying", "character varying", "numeric", "numeric", "boolean"),
    "contratos": ("bigint", "bigint", "bigint", "date", "date", "character varying"),
    "pagamentos": ("bigint", "bigint", "date", "date", "numeric", "character varying"),
    "servidores": ("bigint", "character varying", "character varying", "integer", "numeric", "character varying"),
}


class LoadError(Exception):
    pass


def connection_settings():
    """Aceita o .env carregado por uv e as variáveis do serviço seed."""
    if os.environ.get('DATABASE_URL'):
        return dict(conninfo=os.environ['DATABASE_URL'])
    settings = {}
    for field, pg_name, compose_name in (
        ('host', 'PGHOST', 'POSTGRES_HOST'),
        ('port', 'PGPORT', 'POSTGRES_PORT'),
        ('user', 'PGUSER', 'POSTGRES_USER'),
        ('password', 'PGPASSWORD', 'POSTGRES_PASSWORD'),
        ('dbname', 'PGDATABASE', 'POSTGRES_DB'),
    ):
        value = os.environ.get(pg_name) or os.environ.get(compose_name)
        if value:
            settings[field] = value
    settings.setdefault('host', '127.0.0.1')
    settings.setdefault('port', '5432')
    if not settings.get('user') or not settings.get('dbname'):
        raise LoadError('Configure POSTGRES_USER e POSTGRES_DB; no uso local, carregue .env com uv run --env-file .env.')
    return settings


def initialize_schema(conn):
    """Inicializa o modelo local sem modificar tabelas já existentes."""
    existing = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'nexus'").fetchall()
    if existing:
        return
    model = MODEL_PATH.read_text(encoding='utf-8')
    conn.execute('CREATE SCHEMA IF NOT EXISTS nexus')
    conn.execute(model, prepare=False)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str, ensure_ascii=False).encode()).hexdigest()


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def month(day, offset):
    index = day.year * 12 + day.month - 1 + offset
    year, mm = divmod(index, 12)
    return date(year, mm + 1, min(day.day, calendar.monthrange(year, mm + 1)[1]))


def namespace(dataset):
    tag = hashlib.sha256(dataset.encode()).hexdigest()
    # Faixa estável de BIGINT, distante das identidades usuais. Não avança sequências.
    return (1 << 61) + (int(tag[:10], 16) << 16), tag[:10]


def inspect(conn):
    """Consulta o catálogo real; não executa DDL nem carrega arquivos SQL locais."""
    columns = conn.execute("""
        SELECT table_name, column_name, data_type, is_nullable, column_default,
               is_identity, identity_generation, character_maximum_length,
               numeric_precision, numeric_scale
        FROM information_schema.columns
        WHERE table_schema = 'nexus' ORDER BY table_name, ordinal_position
    """).fetchall()
    constraints = conn.execute("""
        SELECT r.relname, c.conname, c.contype, pg_get_constraintdef(c.oid)
        FROM pg_constraint c JOIN pg_class r ON r.oid = c.conrelid
        JOIN pg_namespace n ON n.oid = r.relnamespace
        WHERE n.nspname = 'nexus' ORDER BY r.relname, c.conname
    """).fetchall()
    indexes = conn.execute("""
        SELECT tablename, indexname, indexdef FROM pg_indexes
        WHERE schemaname = 'nexus' ORDER BY tablename, indexname
    """).fetchall()
    triggers = conn.execute("""
        SELECT r.relname, t.tgname, pg_get_triggerdef(t.oid)
        FROM pg_trigger t JOIN pg_class r ON r.oid = t.tgrelid
        JOIN pg_namespace n ON n.oid = r.relnamespace
        WHERE n.nspname = 'nexus' AND NOT t.tgisinternal ORDER BY r.relname, t.tgname
    """).fetchall()
    policies = conn.execute("""
        SELECT relname, relrowsecurity, relforcerowsecurity
        FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'nexus' AND c.relkind IN ('r', 'p') ORDER BY relname
    """).fetchall()
    tables = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='nexus'").fetchall()
    if {r[0] for r in tables} != set(COLUMNS):
        raise LoadError('Tabelas do schema nexus divergem do modelo; em um banco novo, use --init-schema.')
    nullable = {('contratos', 'data_fim'), ('pagamentos', 'data_pagamento')}
    lengths = {'clientes': {1: 100, 2: 50, 3: 80, 4: 2}, 'servico': {1: 250, 2: 50},
               'contratos': {5: 20}, 'pagamentos': {5: 20}, 'servidores': {1: 80, 2: 50, 5: 20}}
    required_checks = {'clientes': {'data_nao_futura', 'estado_correto'},
                       'servico': {'preco_mensal_nao_negativo', 'custo_mensal_nao_negativo'},
                       'contratos': {'data_fim_validade', 'status_valido'},
                       'pagamentos': {'valor_nao_negativo', 'status_valido', 'data_pagamento_valida'},
                       'servidores': {'capacidade_nao_negativa', 'custo_mensal_nao_negativo', 'status_valido'}}
    expected_links = {('contratos', 'FOREIGN KEY (id_cliente) REFERENCES nexus.clientes(id)'),
                      ('contratos', 'FOREIGN KEY (id_servico) REFERENCES nexus.servico(id)'),
                      ('pagamentos', 'FOREIGN KEY (id_contrato) REFERENCES nexus.contratos(id)')}
    if not expected_links <= {(r[0], r[3]) for r in constraints if r[2] == 'f'}:
        raise LoadError('Relacionamentos obrigatórios ausentes ou alterados.')
    if not any(r[0] == 'pagamentos' and r[2:] == ('u', 'UNIQUE (id_contrato, data_vencimento)') for r in constraints):
        raise LoadError('Unicidade de cobrança ausente ou alterada.')
    for table, names in COLUMNS.items():
        actual = [r for r in columns if r[0] == table]
        if tuple(r[1] for r in actual) != names or tuple(r[2] for r in actual) != TYPES[table]:
            raise LoadError(f"Estrutura incompatível em nexus.{table}; nenhuma alteração realizada.")
        if any((r[3] == 'YES') != ((table, r[1]) in nullable) for r in actual):
            raise LoadError(f'Obrigatoriedade alterada em nexus.{table}.')
        if any(actual[i][7] != size for i, size in lengths[table].items()):
            raise LoadError(f'Limites textuais alterados em nexus.{table}.')
        if any(r[2] == 'numeric' and r[8:10] != (10, 2) for r in actual):
            raise LoadError(f'Precisão monetária alterada em nexus.{table}.')
        if not required_checks[table] <= {r[1] for r in constraints if r[0] == table and r[2] == 'c'}:
            raise LoadError(f'Checks obrigatórios ausentes em nexus.{table}.')
        if actual[0][5:7] != ("YES", "ALWAYS"):
            raise LoadError(f"Identidade incompatível em nexus.{table}.")
        if not any(r[0] == table and r[2:] == ('p', 'PRIMARY KEY (id)') for r in constraints):
            raise LoadError(f"Chave primária incompatível em nexus.{table}.")
    if any(r[0] in COLUMNS for r in triggers) or any(r[0] in COLUMNS and (r[1] or r[2]) for r in policies):
        raise LoadError("Triggers ou políticas de acesso exigem revisão antes da carga.")
    return dict(columns=columns, constraints=constraints, indexes=indexes, triggers=triggers, policies=policies)


def generate(seed, today, dataset):
    rng = random.Random(seed)
    base, _ = namespace(dataset)
    first = month(today, -36)
    rows = {table: [] for table in COLUMNS}
    places = [("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Belo Horizonte", "MG"),
              ("Fortaleza", "CE"), ("Recife", "PE"), ("Curitiba", "PR"), ("Porto Alegre", "RS"),
              ("Brasília", "DF"), ("Salvador", "BA"), ("Manaus", "AM"), ("Goiânia", "GO")]
    sectors = ["Tecnologia", "Comércio", "Saúde", "Educação", "Finanças", "Indústria", "Logística", "Serviços"]
    stems = ["Aurora", "Horizonte", "Vértice", "Prisma", "Atlântico", "Orion", "Candeia", "Cedro", "Íris", "Solar"]
    suffixes = ["Sistemas", "Digital", "Soluções", "Brasil", "Grupo", "Negócios", "Redes", "Gestão"]
    risks, scales = [], []
    for i in range(1000):
        city, state = rng.choices(places, weights=[30, 13, 10, 8, 7, 9, 6, 6, 5, 2, 4])[0]
        registered = first + timedelta(days=int(rng.betavariate(1.2, 1.6) * (today - first).days))
        if i == 0:
            registered = first
        name = f"{rng.choice(stems)} {rng.choice(suffixes)}"
        rows['clientes'].append((base+i+1, name, rng.choices(sectors, [26, 22, 10, 9, 8, 8, 7, 10])[0], city, state, registered))
        risks.append(rng.betavariate(1.5, 7))
        scales.append(rng.lognormvariate(0, 0.8))

    groups = [("Hospedagem", "App", 69), ("Banco de dados", "DB", 149),
              ("Armazenamento", "Storage", 29), ("Computação", "Compute", 199)]
    tiers = ["Start", "Plus", "Pro", "Business", "Enterprise"]
    for i in range(20):
        category, label, price = groups[i // 5]
        price = money(Decimal(price) * Decimal(["1", "2.4", "5", "11", "24"][i % 5]))
        cost = money(price * Decimal(str(rng.uniform(0.28, 0.72))))
        rows['servico'].append((base+i+1, f"Nexus {label} {tiers[i % 5]}", category, price, cost, i not in (17, 19)))

    sizes = [min(36, max(1, int(rng.gammavariate(1.25, 4.4)) + 1)) for _ in range(5000)]
    delta = 30000 - sum(sizes)
    while delta:
        i = rng.randrange(5000)
        step = 1 if delta > 0 else -1
        if 1 <= sizes[i] + step <= 36:
            sizes[i] += step
            delta -= step

    seen = set()
    invoice_id = 0
    service_weights = [23, 17, 9, 4, 1, 14, 11, 7, 3, 1, 17, 10, 6, 2, 1, 9, 6, 0, 1, 0]
    for i, n in enumerate(sizes):
        state = rng.choices(['ativo', 'suspenso', 'cancelado'], [74, 9, 17])[0]
        if state == 'ativo':
            latest = today + timedelta(days=rng.randint(-25, 14))
            if n == 1:
                latest = min(latest, today)
        else:
            latest = month(today, -rng.randint(0, 36-n)) - timedelta(days=rng.randint(0, 20))
        start = max(first, month(latest, -(n-1)))
        # Recalcular sempre a partir do dia de início evita deriva em fevereiro.
        due_dates = [month(start, j) for j in range(n)]
        if state != 'ativo' and due_dates[-1] > today:
            raise LoadError("Cronologia interna inválida.")
        eligible = [j for j, c in enumerate(rows['clientes'][:900]) if c[5] <= start]
        customer = rng.choices(eligible, [scales[j] for j in eligible])[0]
        service = rng.choices(range(20), service_weights)[0]
        while (customer, service, start) in seen:
            # Evita contratos indistinguíveis sem modificar a cronologia.
            customer = rng.choices(eligible, [scales[j] for j in eligible])[0]
            service = rng.choices(range(20), service_weights)[0]
        seen.add((customer, service, start))
        end = min(today, due_dates[-1] + timedelta(days=rng.randint(0, 20))) if state == 'cancelado' else None
        contract_id = base+i+1
        rows['contratos'].append((contract_id, base+customer+1, base+service+1, start, end, state))
        agreed = rows['servico'][service][3] * Decimal(str(rng.uniform(0.83, 1.1)))
        for due in due_dates:
            paid = None
            if due > today:
                payment_state = 'pendente'
            elif rng.random() < risks[customer] * (1.3 if state == 'suspenso' else 0.7):
                payment_state = 'atrasado' if due < today else 'pendente'
            else:
                lag = (rng.randint(1, 55) if rng.random() < 0.16 + risks[customer]
                       else rng.randint(-5, 0))
                proposed = max(start, due + timedelta(days=lag))
                if proposed <= today:
                    payment_state, paid = 'pago', proposed
                else:
                    payment_state = 'atrasado' if due < today else 'pendente'
            amount = agreed * Decimal(str(rng.uniform(0.97, 1.04)))
            if paid is not None and paid > due:
                amount *= Decimal('1.02')
            invoice_id += 1
            rows['pagamentos'].append((base+invoice_id, contract_id, due, paid, money(amount), payment_state))

    for i in range(30):
        region = rng.choices(['br-sao-paulo', 'br-fortaleza', 'us-virginia', 'eu-frankfurt'], [49, 21, 20, 10])[0]
        capacity = rng.choices([512, 1024, 2048, 4096, 8192, 16384], [5, 14, 27, 29, 18, 7])[0]
        rows['servidores'].append((base+i+1, f"nx-{region}-{i+1:02d}", region, capacity,
                                  money(Decimal(capacity) * Decimal(str(rng.uniform(0.18, 0.49)))),
                                  rng.choices(['ativo', 'inativo', 'manutencao'], [83, 8, 9])[0]))
    naturalize_names(rows, seed)
    validate(rows, today)
    return rows


COMPANY_TYPES = {
    "Tecnologia": ("Sistemas", "Tecnologia", "Software", "Soluções Digitais", "Consultoria em TI"),
    "Comércio": ("Comercial", "Distribuidora", "Empório", "Atacado", "Mercado", "Casa de Materiais"),
    "Saúde": ("Clínica", "Laboratório", "Centro Médico", "Farmácia", "Odontologia"),
    "Educação": ("Colégio", "Escola", "Instituto de Ensino", "Centro Educacional", "Cursos"),
    "Finanças": ("Assessoria Financeira", "Crédito", "Gestão Financeira", "Consultoria Financeira"),
    "Indústria": ("Metalúrgica", "Indústria", "Têxtil", "Embalagens", "Móveis", "Alimentos"),
    "Logística": ("Transportes", "Logística", "Cargas", "Entregas", "Armazéns"),
    "Serviços": ("Consultoria", "Contabilidade", "Engenharia", "Arquitetura", "Manutenção", "Gestão"),
}
BRANDS = ("Aurora", "Horizonte", "Vértice", "Prisma", "Atlântico", "Orion", "Candeia", "Cedro", "Íris", "Solar",
          "Ipê", "Jatobá", "Aroeira", "Veredas", "Paineira", "Sabiá", "Mandacaru", "Canela", "Jacarandá", "Sereno",
          "Alvorada", "Essência", "Harmonia", "Caminhos", "Pontal", "Nascente", "Travessia", "Acácia", "Raízes", "Boa Vista")
QUALIFIERS = ("do Vale", "da Serra", "do Cerrado", "do Sol", "das Palmeiras", "do Lago", "da Lagoa", "do Campo",
              "do Norte", "do Sul", "do Litoral", "da Vila", "do Bosque", "dos Jardins", "da Praça", "da Colina")
HOST_NAMES = ("ipe", "jatoba", "aroeira", "cedro", "angico", "cajueiro", "acacia", "paineira", "peroba", "imbuia",
              "canela", "figueira", "sibipiruna", "jacaranda", "jequitiba", "sucupira", "jatobazinho", "guapuruvu",
              "carnauba", "buriti", "tucuma", "bacaba", "copaiba", "andiroba", "castanheira", "mangabeira",
              "pitangueira", "jabuticabeira", "cerejeira", "amendoeira")
ARTIFICIAL_TEXT = re.compile(r"\[[0-9a-f]{8,}\]|\b[0-9a-f]{8}-[0-9a-f-]{27,}\b|\s\d{4}(?:\s|$)|-[0-9a-f]{10}$", re.I)


def naturalize_names(rows, seed):
    """Vocabulário setorial e sorteios próprios preservam a série financeira v1."""
    rng = random.Random(f"nexus-names-v2:{seed}")
    used = set()
    for index, row in enumerate(rows['clientes']):
        for _ in range(10000):
            brand = rng.choice(BRANDS)
            kind = rng.choice(COMPANY_TYPES[row[2]])
            qualifier = rng.choice(QUALIFIERS) if rng.random() < .62 else ""
            # Ordem acompanha o uso corrente de cada designação empresarial.
            name = (f"{kind} {brand}" if row[2] in ('Comércio', 'Saúde', 'Educação', 'Indústria')
                    else f"{brand} {kind}")
            name = f"{name} {qualifier}".strip()
            if name.casefold() not in used:
                used.add(name.casefold())
                rows['clientes'][index] = (row[0], name, *row[2:])
                break
        else:
            raise LoadError('Vocabulário empresarial esgotado; nenhuma carga realizada.')
    hosts = list(HOST_NAMES)
    rng.shuffle(hosts)
    for index, row in enumerate(rows['servidores']):
        rows['servidores'][index] = (row[0], f"nx-{row[2]}-{hosts[index]}", *row[2:])


def require(condition, message):
    # Não usar assert: python -O também precisa rejeitar registros inválidos.
    if not condition:
        raise LoadError(message)


def validate(rows, today):
    """Valida tipos, domínios, nomes, cronologia e relacionamentos do gerador."""
    require({t: len(r) for t, r in rows.items()} == COUNTS, 'Quantidades internas inválidas.')
    clients = {r[0]: r for r in rows['clientes']}
    services = {r[0]: r for r in rows['servico']}
    contracts = {r[0]: r for r in rows['contratos']}
    first = month(today, -36)
    limits = {'clientes': {1: 100, 2: 50, 3: 80, 4: 2},
              'servico': {1: 250, 2: 50}, 'contratos': {5: 20},
              'pagamentos': {5: 20}, 'servidores': {1: 80, 2: 50, 5: 20}}
    optional = {'contratos': {4}, 'pagamentos': {3}}
    for table, records in rows.items():
        require(len({r[0] for r in records}) == len(records), f'IDs duplicados em {table}.')
        for row in records:
            require(len(row) == len(COLUMNS[table]), f'Colunas inválidas em {table}.')
            require(type(row[0]) is int and 0 < row[0] < 2**63, f'ID inválido em {table}.')
            for i, value in enumerate(row):
                require(value is not None or i in optional.get(table, set()), f'Obrigatório ausente em {table}.')
            for i, limit in limits[table].items():
                value = row[i]
                require(isinstance(value, str) and value == value.strip() and 0 < len(value) <= limit,
                        f'Texto inválido em {table}.')
                require(not ARTIFICIAL_TEXT.search(value), f'Marcador artificial em {table}.')
    for table in ('clientes', 'servico', 'servidores'):
        require(len({r[1].casefold() for r in rows[table]}) == len(rows[table]), f'Nomes repetidos em {table}.')
    for table, columns in {'servico': (3, 4), 'pagamentos': (4,), 'servidores': (4,)}.items():
        for row in rows[table]:
            for i in columns:
                value = row[i]
                require(isinstance(value, Decimal) and value.is_finite() and
                        0 <= value <= Decimal('99999999.99') and value == money(value), f'Moeda inválida em {table}.')
    for row in services.values():
        require(row[3] > 0 and type(row[5]) is bool, 'Preço ou atividade inválidos em servico.')
    for row in rows['servidores']:
        require(type(row[3]) is int and row[3] > 0 and row[5] in ('ativo', 'inativo', 'manutencao'),
                'Capacidade ou status inválidos em servidores.')
    for c in clients.values():
        require(type(c[5]) is date and first <= c[5] <= today and c[4] in
                ('SP', 'RJ', 'MG', 'CE', 'PE', 'PR', 'RS', 'DF', 'BA', 'AM', 'GO'), 'Cadastro ou UF inválidos.')
    for c in contracts.values():
        require(c[1] in clients and c[2] in services, 'Contrato órfão.')
        require(c[5] in ('ativo', 'suspenso', 'cancelado'), 'Status contratual inválido.')
        require(clients[c[1]][5] <= c[3] <= today, 'Contrato anterior ao cadastro ou futuro.')
        require(c[4] is None or c[3] <= c[4] <= today, 'Fim de contrato inválido.')
        require((c[5] == 'cancelado') == (c[4] is not None), 'Cancelamento incoerente na carga sintética.')
    billing_keys = set()
    for p in rows['pagamentos']:
        require(p[1] in contracts and p[4] > 0, 'Pagamento órfão ou valor inválido.')
        c = contracts[p[1]]
        require(c[3] <= p[2] <= today + timedelta(days=31), 'Vencimento incoerente.')
        require(c[4] is None or p[2] <= c[4], 'Cobrança após fim do contrato.')
        require(p[5] in ('pago', 'pendente', 'atrasado'), 'Status financeiro inválido.')
        require((p[5] == 'pago') == (p[3] is not None), 'Pagamento e status divergentes.')
        require(p[3] is None or c[3] <= p[3] <= today, 'Data de pagamento incoerente.')
        require(p[5] != 'atrasado' or p[2] < today, 'Atraso antes do vencimento.')
        require(p[5] != 'pendente' or p[2] >= today, 'Pendência vencida na data-base.')
        key = (p[1], p[2])
        require(key not in billing_keys, 'Cobrança duplicada.')
        billing_keys.add(key)


def load(conn, rows):
    """Compara todos os campos antes de inserir; nunca ignora colisões."""
    missing = {}
    for table, expected in rows.items():
        fields = sql.SQL(', ').join(map(sql.Identifier, COLUMNS[table]))
        existing = conn.execute(sql.SQL('SELECT {} FROM nexus.{} WHERE id BETWEEN %s AND %s ORDER BY id').format(
            fields, sql.Identifier(table)), (expected[0][0], expected[-1][0])).fetchall()
        expected_map = {r[0]: r for r in expected}
        for row in existing:
            if expected_map.get(row[0]) != row:
                raise LoadError(f"Colisão ou alteração em nexus.{table}; carga cancelada sem sobrescrever dados.")
        present = {r[0] for r in existing}
        missing[table] = [r for r in expected if r[0] not in present]
    # Outro identificador de carga não deve duplicar o mesmo catálogo/empresas.
    for table in ('clientes', 'servico', 'servidores'):
        expected = rows[table]
        name = sql.Identifier(COLUMNS[table][1])
        collision = conn.execute(sql.SQL(
            'SELECT EXISTS(SELECT 1 FROM nexus.{} WHERE lower(btrim({})) = ANY(%s) AND NOT (id = ANY(%s)))'
        ).format(sql.Identifier(table), name),
            ([r[1].strip().lower() for r in expected], [r[0] for r in expected])).fetchone()[0]
        if collision:
            raise LoadError(f'Nomes já existentes fora desta carga em nexus.{table}; use um banco vazio para outra carga independente.')
    # COPY inclui explicitamente as identidades, sem consumir nem reiniciar sequências.
    for table in ('clientes', 'servico', 'servidores', 'contratos', 'pagamentos'):
        if missing[table]:
            command = sql.SQL('COPY nexus.{} ({}) FROM STDIN').format(
                sql.Identifier(table), sql.SQL(', ').join(map(sql.Identifier, COLUMNS[table])))
            with conn.cursor().copy(command) as batch:
                for row in missing[table]:
                    batch.write_row(row)
    # Força validação de eventuais restrições postergadas antes de retornar.
    conn.execute('SET CONSTRAINTS ALL IMMEDIATE')
    for table, expected in rows.items():
        fields = sql.SQL(', ').join(map(sql.Identifier, COLUMNS[table]))
        actual = conn.execute(sql.SQL('SELECT {} FROM nexus.{} WHERE id BETWEEN %s AND %s ORDER BY id').format(
            fields, sql.Identifier(table)), (expected[0][0], expected[-1][0])).fetchall()
        if actual != expected:
            raise LoadError(f"Verificação final falhou em nexus.{table}.")
    return {t: len(missing[t]) for t in COUNTS}


def write_state(path, content):
    temporary = path.with_suffix('.tmp')
    with temporary.open('w', encoding='utf-8') as out:
        json.dump(content, out, ensure_ascii=False, sort_keys=True, indent=2, default=str)
        out.flush()
        os.fsync(out.fileno())
    os.replace(temporary, path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def report(counts, integrity):
    for table in COUNTS:
        print(f"{table}: {counts.get(table, 0):,}".replace(',', '.'))
    print(f"Erros de integridade: {integrity}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--dataset', default='nexus-cloud-v1', help='Identificador estável da carga; não permite duplicar o catálogo existente.')
    parser.add_argument('--as-of', type=date.fromisoformat, help='Data-base ISO; por padrão, data atual do banco.')
    parser.add_argument('--state-dir', type=Path, default=PROJECT_ROOT / '.nexus-seed')
    parser.add_argument('--init-schema', action='store_true', help='Cria o schema e as tabelas do modelo em um schema vazio.')
    parser.add_argument('--if-empty', action='store_true', help='Ignora a carga se qualquer tabela já tiver dados; usado pelo Compose.')
    parser.add_argument('--dry-run', action='store_true', help='Executa e valida a carga, mas desfaz a transação.')
    args = parser.parse_args(argv)
    _, tag = namespace(args.dataset)
    path = args.state_dir / f'{tag}.json'
    try:
        args.state_dir.mkdir(parents=True, exist_ok=True)
        # O lock de arquivo protege o manifesto; o lock PostgreSQL protege outros hosts.
        with (args.state_dir / f'{tag}.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with psycopg.connect(**connection_settings(), connect_timeout=10) as conn:
                conn.execute("SET LOCAL TIME ZONE 'America/Fortaleza'")
                conn.execute("SET LOCAL lock_timeout = '15s'")
                conn.execute("SELECT pg_advisory_xact_lock(736782501)")
                if args.init_schema:
                    initialize_schema(conn)
                schema = inspect(conn)
                for table in sorted(COLUMNS):
                    conn.execute(sql.SQL('LOCK TABLE nexus.{} IN SHARE ROW EXCLUSIVE MODE').format(sql.Identifier(table)))
                if args.if_empty:
                    occupied = any(conn.execute(sql.SQL('SELECT EXISTS(SELECT 1 FROM nexus.{})').format(
                        sql.Identifier(table))).fetchone()[0] for table in COLUMNS)
                    if occupied:
                        print('Carga inicial ignorada: o banco já contém dados; nenhum registro foi alterado.')
                        return 0
                current = conn.execute('SELECT CURRENT_DATE').fetchone()[0]
                identity = conn.execute("SELECT current_database(), (SELECT oid FROM pg_database WHERE datname=current_database())").fetchone()
                if path.exists():
                    state = json.loads(path.read_text(encoding='utf-8'))
                    if state['version'] != VERSION:
                        raise LoadError('Versão do manifesto incompatível; use o gerador original da carga, sem recriar registros.')
                    if (state['dataset'], state['seed']) != (args.dataset, args.seed):
                        raise LoadError('Parâmetros divergem do manifesto local; use a semente original.')
                    if state['database'] != list(identity):
                        raise LoadError('O manifesto pertence a outro banco de dados.')
                    today = date.fromisoformat(state['as_of'])
                    if args.as_of is not None and args.as_of != today:
                        raise LoadError('Data-base diverge do manifesto local.')
                    if state['schema_digest'] != digest(schema):
                        raise LoadError('O schema mudou desde a carga anterior; revisão necessária.')
                else:
                    today = args.as_of or current
                    state = dict(version=VERSION, dataset=args.dataset, seed=args.seed, as_of=today.isoformat(),
                                 database=list(identity), schema_digest=digest(schema), schema=schema)
                if today > current:
                    raise LoadError('A data-base não pode ser futura.')
                rows = generate(args.seed, today, args.dataset)
                plan_hash = digest(rows)
                if state.get('plan_digest', plan_hash) != plan_hash:
                    raise LoadError('O gerador difere do manifesto; carga interrompida.')
                state['plan_digest'] = plan_hash
                # Persistir ANTES do commit permite retomar até após queda do processo.
                if not args.dry_run:
                    write_state(path, state)
                inserted = load(conn, rows)
                if args.dry_run:
                    conn.rollback()
                    inserted = {t: 0 for t in COUNTS}
                    print('Simulação concluída: dados validados e transação revertida; nenhuma linha persistida.')
        report(inserted, 'nenhum')
        return 0
    except psycopg.IntegrityError as exc:
        report({}, f'sim; transação revertida (SQLSTATE {exc.sqlstate})')
        return 1
    except (LoadError, psycopg.Error, OSError, ValueError, KeyError, AssertionError) as exc:
        report({}, 'não confirmados; carga interrompida e sem commit')
        # Não imprime DSN, valores de linhas ou mensagens PostgreSQL com dados.
        detail = str(exc) if isinstance(exc, LoadError) else type(exc).__name__
        print(f'Carga interrompida: {detail}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
