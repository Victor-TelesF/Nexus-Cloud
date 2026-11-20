# Catálogo de consultas e perguntas analíticas

O catálogo reúne as perguntas de negócio que orientam as consultas SQL 01–25, as análises visuais 26–29 e o painel 30. Os identificadores e as âncoras permanecem estáveis para referência nos artefatos.

Cada consulta tem uma população, um período e uma granularidade definidos pela pergunta. O [contexto de negócio](01-contexto-negocio.md) complementa essas definições; o [acompanhamento técnico](03-progresso.md) informa a implementação, os resultados exportados e as validações disponíveis. A presença de uma pergunta neste catálogo não implica implementação.

Os requisitos de extração, visualização e interpretação dos itens 26–30 estão na [especificação visual](04-visualizacoes-dashboard.md).

## Carteira de clientes e catálogo de serviços (01–05)

<a id="d01"></a>

### 01 · Distribuição geográfica

Consulta SQL: [01-distribuicao-geografica.sql](../sql/analysis/conhecendo_a_empresa/01-distribuicao-geografica.sql)

Em quais estados a Nexus Cloud possui mais clientes? Apresente a quantidade de clientes por estado, começando pelo maior.

<a id="d02"></a>

### 02 · Catálogo de serviços

Consulta SQL: [02-catalogo-servicos.sql](../sql/analysis/conhecendo_a_empresa/02-catalogo-servicos.sql)

Quais serviços disponíveis possuem mensalidade superior a R$ 300? Apresente seus nomes, categorias e preços, começando pelo mais caro.

<a id="d03"></a>

### 03 · Clientes recentes

Consulta SQL: [03-clientes-recentes.sql](../sql/analysis/conhecendo_a_empresa/03-clientes-recentes.sql)

Quais empresas se cadastraram nos últimos 90 dias? Apresente o nome, o setor, a cidade e a data de cadastro.

<a id="d04"></a>

### 04 · Infraestrutura disponível

Consulta SQL: [04-infraestrutura-servidores.sql](../sql/analysis/conhecendo_a_empresa/04-infraestrutura-servidores.sql)

Quantos servidores estão ativos e qual é a capacidade total de armazenamento deles?

<a id="d05"></a>

### 05 · Preços por categoria

Consulta SQL: [05-precos-por-categoria.sql](../sql/analysis/conhecendo_a_empresa/05-precos-por-categoria.sql)

Qual é o preço médio, o menor preço e o maior preço dos serviços em cada categoria?

## Contratos e operações (06–12)

<a id="d06"></a>

### 06 · Carteira de contratos

Consulta SQL: [06-carteira-contratos-ativos.sql](../sql/analysis/relacionamentos_e_operacoes/06-carteira-contratos-ativos.sql)

Quais empresas possuem contratos administrativamente ativos? Apresente a empresa, o serviço, o valor mensal e a data de início.

<a id="d07"></a>

### 07 · Clientes sem contratos

Consulta SQL: [07-clientes-sem-contratos.sql](../sql/analysis/relacionamentos_e_operacoes/07-clientes-sem-contratos.sql)

Quais empresas estão cadastradas, mas nunca contrataram nenhum serviço?

<a id="d08"></a>

### 08 · Serviços mais contratados

Consulta SQL: [08-servicos-mais-contratados.sql](../sql/analysis/relacionamentos_e_operacoes/08-servicos-mais-contratados.sql)

Quais serviços possuem mais contratos ativos? Apresente um ranking com os dez primeiros.

<a id="d09"></a>

### 09 · Clientes com múltiplos contratos

Consulta SQL: [09-clientes-multiplos-contratos.sql](../sql/analysis/relacionamentos_e_operacoes/09-clientes-multiplos-contratos.sql)

Quais empresas possuem três ou mais contratos ativos? Quantos contratos cada uma possui?

<a id="d10"></a>

### 10 · Serviços sem demanda

Consulta SQL: [10-servicos-sem-demanda.sql](../sql/analysis/relacionamentos_e_operacoes/10-servicos-sem-demanda.sql)

Quais serviços do catálogo nunca foram contratados, independentemente de estarem disponíveis atualmente?

<a id="d11"></a>

### 11 · Contratos vencidos

Consulta SQL: [11-contratos-ativos-vencidos.sql](../sql/analysis/relacionamentos_e_operacoes/11-contratos-ativos-vencidos.sql)

Quais contratos continuam registrados como ativos mesmo após sua data de encerramento? Apresente a empresa, o serviço, a data de encerramento e os dias decorridos desde então.

<a id="d12"></a>

### 12 · Clientes sem contratos ativos

Consulta SQL: [12-clientes-sem-contratos-ativos.sql](../sql/analysis/relacionamentos_e_operacoes/12-clientes-sem-contratos-ativos.sql)

Quais empresas já contrataram pelo menos um serviço, mas atualmente não possuem nenhum contrato administrativamente ativo?

## Receita e indicadores financeiros (13–19)

<a id="d13"></a>

### 13 · Receita mensal recebida

Consulta SQL: [13-receita-mensal-recebida.sql](../sql/analysis/relatorios_financeiros/13-receita-mensal-recebida.sql)

Quanto dinheiro a empresa efetivamente recebeu em cada mês? Considere a data do pagamento, não a data do vencimento.

<a id="d14"></a>

### 14 · Clientes inadimplentes

Consulta SQL: [14-clientes-inadimplentes.sql](../sql/analysis/relatorios_financeiros/14-clientes-inadimplentes.sql)

Quais clientes possuem cobranças registradas como atrasadas? Apresente a quantidade de cobranças e o valor total em aberto por cliente.

<a id="d15"></a>

### 15 · Maiores clientes por receita

Consulta SQL: [15-top-clientes-receita.sql](../sql/analysis/relatorios_financeiros/15-top-clientes-receita.sql)

Quais são os dez clientes que mais contribuíram para a receita efetivamente recebida pela Nexus Cloud?

<a id="d16"></a>

### 16 · Receita por categoria

Consulta SQL: [16-receita-por-categoria.sql](../sql/analysis/relatorios_financeiros/16-receita-por-categoria.sql)

Qual categoria de serviços gerou a maior receita recebida durante o histórico disponível?

<a id="d17"></a>

### 17 · Taxa de inadimplência

Consulta SQL: [17-taxa-inadimplencia.sql](../sql/analysis/relatorios_financeiros/17-taxa-inadimplencia.sql)

Qual percentual do valor total das cobranças registradas corresponde às cobranças atualmente classificadas como atrasadas?

<a id="d18"></a>

### 18 · Receita e custos operacionais

Consulta SQL: [18-receita-vs-custos.sql](../sql/analysis/relatorios_financeiros/18-receita-vs-custos.sql)

Qual é a receita mensal contratada pelos contratos administrativamente ativos e qual seria o custo mensal estimado de fornecimento desses serviços? Calcule também a diferença entre os valores.

<a id="d19"></a>

### 19 · Concentração de receita

Consulta SQL: [19-concentracao-cinco-clientes.sql](../sql/analysis/relatorios_financeiros/19-concentracao-cinco-clientes.sql)

Qual percentual de toda a receita recebida foi gerado individualmente pelos cinco maiores clientes?

## Séries temporais e análises avançadas (20–25)

<a id="d20"></a>

### 20 · Evolução das contratações

Consulta SQL: [20-evolucao-contratacoes-mensal.sql](../sql/analysis/analise_avancada/20-evolucao-contratacoes-mensal.sql)

Quantos novos contratos foram iniciados em cada mês do histórico disponível?

<a id="d21"></a>

### 21 · Cancelamentos

Consulta SQL: [21-churn-contratos-cancelados.sql](../sql/analysis/analise_avancada/21-churn-contratos-cancelados.sql)

Qual percentual do total de contratos registrados possui status cancelado? Apresente também a quantidade absoluta.

<a id="d22"></a>

### 22 · Crescimento da receita

Consulta SQL: [22-crescimento-receita-mensal.sql](../sql/analysis/analise_avancada/22-crescimento-receita-mensal.sql)

Como evoluiu a receita efetivamente recebida ao longo dos meses? Calcule a variação percentual de cada mês em relação ao anterior.

<a id="d23"></a>

### 23 · Desempenho por setor

Consulta SQL: [23-receita-por-setor.sql](../sql/analysis/analise_avancada/23-receita-por-setor.sql)

Quais setores econômicos dos clientes geraram mais receita para a Nexus Cloud?

<a id="d24"></a>

### 24 · Atraso nos pagamentos

Consulta SQL: [24-pagamentos-atrasados.sql](../sql/analysis/analise_avancada/24-pagamentos-atrasados.sql)

Entre as cobranças que foram pagas depois do vencimento, qual foi a quantidade de dias de atraso de cada pagamento? Qual é a média de dias de atraso?

<a id="d25"></a>

### 25 · Clientes acima da média

Consulta SQL: [25-clientes-acima-da-media.sql](../sql/analysis/analise_avancada/25-clientes-acima-da-media.sql)

Quais clientes geraram uma receita total superior à média de receita por cliente, considerando todos os clientes cadastrados, inclusive aqueles sem pagamentos?

## Visualizações e indicadores gerenciais (26–30)

As análises 26–29 usam Jupyter Notebook no VS Code, e o painel 30 tem implementação prevista em Python/Streamlit. Consulte a [configuração do ambiente](06-ambiente-analise.md).

<a id="d26"></a>

### 26 · Diagnóstico comercial

Notebook: [26-diagnostico-comercial.ipynb](../notebooks/26-diagnostico-comercial.ipynb)

Como evoluem as contratações e em quais períodos há crescimento ou queda? O escopo inclui um gráfico temporal e três observações sustentadas pelos dados.


<a id="d27"></a>

### 27 · Análise de receita

Notebook: [27-mix-receita-categorias.ipynb](../notebooks/27-mix-receita-categorias.ipynb)

Como a receita recebida se distribui por mês e categoria? A análise deve identificar as categorias mais relevantes e as mudanças na composição da receita.


<a id="d28"></a>

### 28 · Perfil dos clientes

Notebook: [28-segmentacao-carteira.ipynb](../notebooks/28-segmentacao-carteira.ipynb)

Como os clientes e a receita da carteira se distribuem por estado e setor econômico? A análise deve comparar esses segmentos e identificar concentrações.


<a id="d29"></a>

### 29 · Riscos financeiros

Notebook: [29-monitoramento-risco.ipynb](../notebooks/29-monitoramento-risco.ipynb)

Em quais clientes se concentram as cobranças atrasadas? A análise deve mostrar a distribuição dos valores em aberto e possíveis prioridades de acompanhamento.


<a id="d30"></a>

### 30 · Dashboard executivo

Aplicação inicial: [app.py](../dashboards/app.py)

O painel deve reunir indicadores de clientes, contratos, receita recebida, cobranças atrasadas, evolução mensal, serviços mais contratados e receita por categoria. O escopo inclui uma breve apresentação dos resultados mais relevantes.
