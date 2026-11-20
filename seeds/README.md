# Geração de dados sintéticos

Na raiz do repositório, com `.env` configurado a partir de [`.env.example`](../.env.example), execute:

```bash
docker compose up -d --build
docker compose wait seed
docker compose logs seed
```

O serviço `seed` aguarda o PostgreSQL ficar saudável e executa [seed.py](seed.py) com `--init-schema --if-empty`. Ele cria o schema `nexus` e suas tabelas a partir de [model.sql](../sql/models/model.sql), gera os registros e valida a carga em uma transação. Uma falha reverte as alterações dessa execução.

O contêiner da carga encerra após o trabalho; não precisa ficar em execução. No log de uma primeira carga bem-sucedida, as quantidades inseridas são:

| Tabela | Registros |
| --- | ---: |
| `clientes` | 1.000 |
| `servico` | 20 |
| `contratos` | 5.000 |
| `pagamentos` | 30.000 |
| `servidores` | 30 |

Se qualquer uma dessas tabelas já contiver registros, `--if-empty` ignora a carga. Esse comportamento preserva a base existente e não completa bases parcialmente preenchidas. Um schema com estrutura incompatível gera um erro, sem adaptar ou apagar as tabelas existentes. Consulte `docker compose logs seed` se a carga terminar com código diferente de `0`.

Os dados ficam no volume `postgres_data`; o manifesto da carga, no volume `seed_state`. `docker compose down` preserva ambos. Para repetir apenas a verificação e a carga de uma base vazia, use `docker compose run --rm seed`.

## Reproduzir uma carga

A semente padrão é `42`. A data-base padrão é a data do PostgreSQL no fuso `America/Fortaleza`. Portanto, a mesma semente em datas-base diferentes pode produzir registros diferentes. Após uma carga, o manifesto conserva seus parâmetros para futuras verificações.

Para definir uma data-base explicitamente em uma base vazia:

```bash
docker compose run --rm seed python seeds/seed.py --init-schema --if-empty --seed 42 --as-of 2026-10-28
```

A data-base não pode ser futura. A semente e a data-base não são suficientes para identificar sozinhas uma execução: preserve também a versão do gerador e os parâmetros do manifesto. Uma nova carga pode produzir resultados diferentes dos [CSVs disponíveis](../reports/).

## Execução local opcional

O fluxo Docker dispensa Python no computador. Para executar o script diretamente em Linux, macOS ou WSL, instale Python 3.13 ou superior e `uv`. Na raiz do repositório:

```bash
uv sync --locked
uv run --env-file .env python seeds/seed.py --init-schema --dry-run
```

`--dry-run` executa as validações e a inserção, mas reverte a transação, inclusive a criação do schema e das tabelas nessa execução. Para carregar uma base vazia de fato, use `--init-schema --if-empty` no lugar de `--init-schema --dry-run`.

A conexão aceita `DATABASE_URL`; quando ausente, usa `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD` e `PGDATABASE`, ou os equivalentes `POSTGRES_*` de `.env`. No host, o endereço padrão é `127.0.0.1` e a porta é `POSTGRES_PORT`. No serviço Docker, o endereço é `db` e a porta interna é `5432`.

O script resolve o modelo e o diretório padrão `.nexus-seed/` a partir de sua própria localização, independentemente do diretório corrente. O arquivo `.env` precisa ser carregado explicitamente, como no comando acima. `--state-dir` permite escolher outro diretório para o manifesto ao trabalhar com outro banco. Credenciais e manifestos locais são ignorados pelo Git.

## Validação e limites

O gerador valida tipos, chaves, valores, cronologia e quantidades antes da carga e compara os registros persistidos com os registros esperados. Há testes em [tests/test_seed.py](../tests/test_seed.py), incluindo cenários de reversão, repetição de carga e preservação de bases existentes. Os testes de integração exigem PostgreSQL descartável via `NEXUS_SEED_TEST_DSN` e criam bancos temporários.

Na revisão documental de 18/11/2026, o comportamento foi conferido pela leitura do código, do Dockerfile e do Compose. Não houve nova carga, execução desses testes ou alteração dos volumes. A base representa um domínio fictício, com distribuições e valores definidos pelo gerador; não é uma amostra de operação real.
