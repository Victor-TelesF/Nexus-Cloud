# Análises em Jupyter

Os notebooks complementam as consultas SQL com exploração em pandas e visualizações em Matplotlib. Eles utilizam CSVs de `reports/` e consultas diretas ao PostgreSQL por meio de `dashboards.database`.

## Conteúdo atual

- [00 · Exploração inicial](00-exploracao-inicial.ipynb): leitura de tabelas e inspeção de tipos e preenchimento, com saídas salvas. Não é uma análise finalizada.
- [26 · Diagnóstico comercial](26-diagnostico-comercial.ipynb): série mensal de contratos e exploração dos cadastros de clientes, com gráficos salvos. Interpretação e validação pendentes.
- [27 · Receita por categoria](27-mix-receita-categorias.ipynb): composição acumulada, receita mensal e consulta por mês/categoria, com gráficos salvos. Interpretação e validação pendentes.
- [28 · Perfil dos clientes](28-segmentacao-carteira.ipynb) e [29 · Riscos financeiros](29-monitoramento-risco.ipynb): somente a descrição do escopo; análises ainda planejadas.

O [acompanhamento técnico](../docs/03-progresso.md) registra o estado e as evidências. As saídas salvas não comprovam a execução sequencial da versão atual.

## Execução

Abra a raiz **Nexus-Cloud** no VS Code e selecione o kernel Python de `.venv`. O diretório de execução está configurado como a raiz do repositório, inclusive para notebooks em subpastas. Assim, caminhos como `reports/analise_avancada/20_evolucao_contratacoes_mensal.csv` partem dessa raiz.

O preparo do ambiente, as extensões e as tarefas estão no [guia de ambiente](../docs/06-ambiente-analise.md). Os CSVs permitem ler os resultados exportados, mas os notebooks 26 e 27 também importam `dashboards.database`: essa importação exige `.env` configurado. As células com `pd.read_sql` ou `pd.read_sql_table` dependem do PostgreSQL disponível.

As perguntas permanecem no [catálogo](../docs/02-desafios-sql.md#d26), e os requisitos de dados, métricas e gráficos estão na [especificação visual](../docs/04-visualizacoes-dashboard.md).
