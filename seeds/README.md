# Dados fictícios para estudo

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

Se qualquer uma dessas tabelas já contiver registros, `--if-empty` ignora a carga. Isso também preserva uma base que você já utiliza para estudar; não completa bases parcialmente preenchidas. Um schema com estrutura incompatível gera um erro, sem adaptar ou apagar as tabelas existentes. Consulte `docker compose logs seed` se a carga terminar com código diferente de `0`.

Os dados ficam no volume `postgres_data`; o manifesto da carga, no volume `seed_state`. `docker compose down` preserva ambos. Para repetir apenas a verificação e a carga de uma base vazia, use `docker compose run --rm seed`.

## Reproduzir uma carga

A semente padrão é `42`. A data-base padrão é a data do PostgreSQL no fuso `America/Fortaleza`. Portanto, a mesma semente em datas-base diferentes pode produzir registros diferentes. Após uma carga, o manifesto conserva seus parâmetros para futuras verificações.

Para definir uma data-base explicitamente em uma base vazia:

```bash
docker compose run --rm seed python seeds/seed.py --init-schema --if-empty --seed 42 --as-of 2026-10-28
```

A data-base não pode ser futura. Os resultados numéricos das consultas de estudo podem diferir dos resultados já registrados no checklist, que identificam a base e a versão usadas em cada revisão.

## Execução local opcional

O fluxo Docker dispensa Python no computador. Para executar o script diretamente em Linux, macOS ou WSL, instale Python 3.13 ou superior e `uv`. Na raiz do repositório:

```bash
uv sync --locked
uv run --env-file .env python seeds/seed.py --init-schema --dry-run
```

`--dry-run` executa as validações e a inserção, mas reverte a transação, inclusive a criação do schema e das tabelas nessa execução. Para carregar uma base vazia de fato, use `--init-schema --if-empty` no lugar de `--init-schema --dry-run`.

A conexão aceita `DATABASE_URL`; quando ausente, usa `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD` e `PGDATABASE`, ou os equivalentes `POSTGRES_*` de `.env`. No host, o endereço padrão é `127.0.0.1` e a porta é `POSTGRES_PORT`. No serviço Docker, o endereço é `db` e a porta interna é `5432`.

O script resolve o modelo e o diretório padrão `.nexus-seed/` a partir de sua própria localização, independentemente do diretório corrente. O arquivo `.env` precisa ser carregado explicitamente, como no comando acima. `--state-dir` permite escolher outro diretório para o manifesto ao trabalhar com outro banco. Credenciais e manifestos locais são ignorados pelo Git.
