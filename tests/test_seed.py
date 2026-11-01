"""Regressões da carga; integração exige um servidor PostgreSQL descartável.

NEXUS_SEED_TEST_DSN habilita testes que criam e removem bancos temporários
com nomes nexus_seed_test_<uuid>. Não use uma conexão de produção.
"""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo

from seeds import seed


class ConnectionTests(unittest.TestCase):
    def test_compose_environment_uses_container_host_and_internal_port(self):
        environment = {
            'POSTGRES_HOST': 'db', 'POSTGRES_PORT': '5432',
            'POSTGRES_USER': 'student', 'POSTGRES_PASSWORD': 'a password # with spaces',
            'POSTGRES_DB': 'study',
        }
        with patch.dict(os.environ, environment, clear=True):
            self.assertEqual(seed.connection_settings(), {
                'host': 'db', 'port': '5432', 'user': 'student',
                'password': 'a password # with spaces', 'dbname': 'study',
            })

    def test_database_url_takes_precedence_over_compose_settings(self):
        url = 'postgresql://student:password@elsewhere:5433/study'
        with patch.dict(os.environ, {'DATABASE_URL': url, 'POSTGRES_HOST': 'db'}, clear=True):
            self.assertEqual(seed.connection_settings(), {'conninfo': url})

    def test_missing_credentials_provide_local_setup_hint(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(seed.LoadError, '--env-file'):
                seed.connection_settings()


@unittest.skipUnless(os.environ.get('NEXUS_SEED_TEST_DSN'), 'Exige PostgreSQL descartável via NEXUS_SEED_TEST_DSN')
class LoadTests(unittest.TestCase):
    def setUp(self):
        self.database = 'nexus_seed_test_' + uuid.uuid4().hex
        self.admin = psycopg.connect(os.environ['NEXUS_SEED_TEST_DSN'], autocommit=True)
        self.admin.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(self.database)))
        self.dsn = make_conninfo(os.environ['NEXUS_SEED_TEST_DSN'], dbname=self.database)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(self.drop_database)

    def drop_database(self):
        try:
            self.admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(self.database)))
        finally:
            self.admin.close()

    def run_seed(self, *arguments):
        output = StringIO()
        errors = StringIO()
        with patch.dict(os.environ, {'DATABASE_URL': self.dsn}), redirect_stdout(output), redirect_stderr(errors):
            code = seed.main(['--state-dir', self.directory.name, *arguments])
        return code, output.getvalue(), errors.getvalue()

    def snapshot(self):
        with psycopg.connect(self.dsn) as conn:
            return {table: conn.execute(sql.SQL('SELECT * FROM nexus.{} ORDER BY id').format(
                sql.Identifier(table))).fetchall() for table in seed.COUNTS}

    def test_dry_run_rolls_back_schema_and_does_not_save_manifest(self):
        code, output, errors = self.run_seed('--init-schema', '--dry-run')
        self.assertEqual(code, 0, errors)
        self.assertIn('transação revertida', output)
        with psycopg.connect(self.dsn) as conn:
            self.assertIsNone(conn.execute("SELECT to_regnamespace('nexus')").fetchone()[0])
        self.assertEqual(list(Path(self.directory.name).glob('*.json')), [])

    def test_initial_load_retry_and_explicit_replay_preserve_all_rows(self):
        # O caminho do modelo também precisa funcionar fora da raiz do projeto.
        previous = Path.cwd()
        try:
            os.chdir(self.directory.name)
            code, _, errors = self.run_seed('--init-schema', '--if-empty')
        finally:
            os.chdir(previous)
        self.assertEqual(code, 0, errors)
        before = self.snapshot()
        self.assertEqual({table: len(rows) for table, rows in before.items()}, seed.COUNTS)
        code, output, errors = self.run_seed('--init-schema', '--if-empty')
        self.assertEqual(code, 0, errors)
        self.assertIn('Carga inicial ignorada', output)
        self.assertEqual(self.snapshot(), before)
        code, _, errors = self.run_seed()
        self.assertEqual(code, 0, errors)
        self.assertEqual(self.snapshot(), before)

    def test_partially_populated_database_is_preserved(self):
        with psycopg.connect(self.dsn) as conn:
            seed.initialize_schema(conn)
            conn.execute("""INSERT INTO nexus.clientes (nome_empresa, setor, cidade, estado)
                         VALUES ('Existing company', 'Tecnologia', 'Fortaleza', 'CE')""")
        before = self.snapshot()
        code, output, errors = self.run_seed('--init-schema', '--if-empty')
        self.assertEqual(code, 0, errors)
        self.assertIn('Carga inicial ignorada', output)
        self.assertEqual(self.snapshot(), before)

    def test_incompatible_existing_table_is_not_replaced(self):
        with psycopg.connect(self.dsn) as conn:
            conn.execute('CREATE SCHEMA nexus')
            conn.execute('CREATE TABLE nexus.clientes (id INTEGER PRIMARY KEY)')
            conn.execute('INSERT INTO nexus.clientes VALUES (7)')
        code, _, errors = self.run_seed('--init-schema', '--if-empty')
        self.assertEqual(code, 1)
        self.assertIn('divergem do modelo', errors)
        with psycopg.connect(self.dsn) as conn:
            self.assertEqual(conn.execute('SELECT * FROM nexus.clientes').fetchall(), [(7,)])
            self.assertEqual(conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'nexus'").fetchall(), [('clientes',)])


if __name__ == '__main__':
    unittest.main()
