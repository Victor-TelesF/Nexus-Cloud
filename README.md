<p align="center">
  <img src="docs/assets/nexus-cloud-banner.svg" alt="Nexus Cloud — laboratório de SQL e análise de dados" width="100%">
</p>

# Nexus Cloud

Como distinguir o que uma empresa de nuvem vendeu, o que cobrou e o que de fato recebeu? Neste laboratório, você responde a pedidos do comercial, do financeiro e da infraestrutura usando dados fictícios da Nexus Cloud. O percurso tem 25 relatórios em PostgreSQL, quatro análises com gráficos e um dashboard executivo.

| Para… | Abra |
| --- | --- |
| Escolher um relatório e entender o pedido | [Os 30 desafios](docs/02-desafios-sql.md) |
| Retomar a última tentativa ou pedir revisão | [Checklist e evidências](docs/03-progresso.md) |
| Consultar o modelo e as regras de negócio | [Contexto da Nexus Cloud](docs/01-contexto-negocio.md) |
| Preparar os gráficos e o painel | [Entregáveis visuais](docs/04-visualizacoes-dashboard.md) |
| Entender como uma entrega será avaliada | [Critérios de correção](docs/05-criterios-correcao.md) |

## Trabalhar no ambiente local

1. Na primeira configuração, copie `.env.example` para `.env` e defina as credenciais. Use Docker com Compose.
2. Inicie o PostgreSQL 17 com `docker compose up -d db`. No VS Code, conecte a extensão PostgreSQL da Microsoft a `127.0.0.1`, usando o banco, o usuário, a senha e a porta do seu `.env` (padrão 5432).
3. Na base de estudo populada, abra a [pasta de consultas](sql/queries/), execute sua tentativa e compare as linhas retornadas com o pedido. Para pedir feedback ao Codex no repositório, escreva, por exemplo, **“Revise o relatório 12 e me dê uma pista para testar minha lógica.”** O fluxo está em [AGENTS.md](AGENTS.md).

Em um volume novo, o Compose inicia o banco vazio. O [modelo SQL](sql/models/model.sql) pressupõe que o schema `nexus` já exista. A carga de dados também é uma etapa separada. Para encerrar o ambiente preservando o volume, use `docker compose down`.

Na etapa visual, o [ambiente Python](pyproject.toml) inclui pandas, Matplotlib e seaborn. O roteiro recomenda Power BI para o painel final e admite uma biblioteca gráfica em Python.
