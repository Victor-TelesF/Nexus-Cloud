# Desafios da Nexus Cloud

A cada pedido, descubra quais dados respondem à pergunta e o que cada linha do resultado deve representar. As evidências de entrega e revisão ficam no [checklist](03-progresso.md).

Para 01–25, entregue a consulta SQL e o resultado obtido. Se houver um achado relevante, acrescente duas ou três frases interpretando-o. Para 26–29, entregue a extração e a análise visual. O 30 reúne os indicadores em um painel. Consulte os [entregáveis visuais](04-visualizacoes-dashboard.md).

Catálogo transcrito do roteiro de 30 desafios da conversa “Criar tabelas e perguntas SQL”. O texto expandido das cinco etapas foi fornecido pelo estudante. Os pedidos 01–12 também foram confrontados com os comentários das consultas na pasta de estudo.

## Etapa 1 · Conhecendo a empresa (01–05)

<a id="d01"></a>

### 01 · Distribuição geográfica

Em quais estados a Nexus Cloud possui mais clientes? Apresente a quantidade de clientes por estado, começando pelo maior.

<a id="d02"></a>

### 02 · Catálogo de serviços

Quais serviços disponíveis possuem mensalidade superior a R$ 300? Apresente seus nomes, categorias e preços, começando pelo mais caro.

<a id="d03"></a>

### 03 · Clientes recentes

Quais empresas se cadastraram nos últimos 90 dias? Apresente o nome, o setor, a cidade e a data de cadastro.

<a id="d04"></a>

### 04 · Infraestrutura disponível

Quantos servidores estão ativos e qual é a capacidade total de armazenamento deles?

<a id="d05"></a>

### 05 · Preços por categoria

Qual é o preço médio, o menor preço e o maior preço dos serviços em cada categoria?

## Etapa 2 · Relacionamentos e operações (06–12)

<a id="d06"></a>

### 06 · Carteira de contratos

Quais empresas possuem contratos administrativamente ativos? Apresente a empresa, o serviço, o valor mensal e a data de início.

<a id="d07"></a>

### 07 · Clientes sem contratos

Quais empresas estão cadastradas, mas nunca contrataram nenhum serviço?

<a id="d08"></a>

### 08 · Serviços mais contratados

Quais serviços possuem mais contratos ativos? Apresente um ranking com os dez primeiros.

<a id="d09"></a>

### 09 · Clientes com múltiplos contratos

Quais empresas possuem três ou mais contratos ativos? Quantos contratos cada uma possui?

<a id="d10"></a>

### 10 · Serviços sem demanda

Quais serviços do catálogo nunca foram contratados, independentemente de estarem disponíveis atualmente?

<a id="d11"></a>

### 11 · Contratos vencidos

Quais contratos continuam registrados como ativos mesmo após sua data de encerramento? Apresente a empresa, o serviço, a data de encerramento e os dias decorridos desde então.

<a id="d12"></a>

### 12 · Clientes sem contratos ativos

Quais empresas já contrataram pelo menos um serviço, mas atualmente não possuem nenhum contrato administrativamente ativo?

## Etapa 3 · Relatórios financeiros (13–19)

<a id="d13"></a>

### 13 · Receita mensal recebida

Quanto dinheiro a empresa efetivamente recebeu em cada mês? Considere a data do pagamento, não a data do vencimento.

<a id="d14"></a>

### 14 · Clientes inadimplentes

Quais clientes possuem cobranças registradas como atrasadas? Apresente a quantidade de cobranças e o valor total em aberto por cliente.

<a id="d15"></a>

### 15 · Maiores clientes por receita

Quais são os dez clientes que mais contribuíram para a receita efetivamente recebida pela Nexus Cloud?

<a id="d16"></a>

### 16 · Receita por categoria

Qual categoria de serviços gerou a maior receita recebida durante o histórico disponível?

<a id="d17"></a>

### 17 · Taxa de inadimplência

Qual percentual do valor total das cobranças registradas corresponde às cobranças atualmente classificadas como atrasadas?

<a id="d18"></a>

### 18 · Receita e custos operacionais

Qual é a receita mensal contratada pelos contratos administrativamente ativos e qual seria o custo mensal estimado de fornecimento desses serviços? Calcule também a diferença entre os valores.

<a id="d19"></a>

### 19 · Concentração de receita

Qual percentual de toda a receita recebida foi gerado individualmente pelos cinco maiores clientes?

## Etapa 4 · Análise avançada (20–25)

<a id="d20"></a>

### 20 · Evolução das contratações

Quantos novos contratos foram iniciados em cada mês do histórico disponível?

<a id="d21"></a>

### 21 · Cancelamentos

Qual percentual do total de contratos registrados possui status cancelado? Apresente também a quantidade absoluta.

<a id="d22"></a>

### 22 · Crescimento da receita

Como evoluiu a receita efetivamente recebida ao longo dos meses? Calcule a variação percentual de cada mês em relação ao anterior.

<a id="d23"></a>

### 23 · Desempenho por setor

Quais setores econômicos dos clientes geraram mais receita para a Nexus Cloud?

<a id="d24"></a>

### 24 · Atraso nos pagamentos

Entre as cobranças que foram pagas depois do vencimento, qual foi a quantidade de dias de atraso de cada pagamento? Qual é a média de dias de atraso?

<a id="d25"></a>

### 25 · Clientes acima da média

Quais clientes geraram uma receita total superior à média de receita por cliente, considerando todos os clientes cadastrados, inclusive aqueles sem pagamentos?

## Etapa 5 · Visualizações e dashboard (26–30)

<a id="d26"></a>

### 26 · Diagnóstico comercial

Analise a evolução das contratações e identifique períodos de crescimento ou queda. Crie um gráfico temporal e descreva três observações sustentadas pelos dados.

**Ferramentas do roteiro** · SQL + Python/Pandas

<a id="d27"></a>

### 27 · Análise de receita

Visualize a receita recebida por mês e por categoria. Identifique as categorias mais relevantes e mudanças na composição da receita.

**Ferramentas do roteiro** · SQL + visualização

<a id="d28"></a>

### 28 · Perfil dos clientes

Construa uma análise que compare clientes por estado e setor econômico, identificando a concentração da carteira e sua distribuição de receita.

**Ferramentas do roteiro** · SQL + visualização

<a id="d29"></a>

### 29 · Riscos financeiros

Produza uma análise das cobranças atrasadas por cliente, identificando concentração dos valores em aberto e possíveis prioridades de acompanhamento.

**Ferramentas do roteiro** · SQL + Python/Pandas

<a id="d30"></a>

### 30 · Dashboard executivo

Entregue um dashboard com indicadores de clientes, contratos, receita recebida, cobranças atrasadas, evolução mensal, serviços mais contratados e receita por categoria. Prepare também uma breve apresentação das descobertas mais relevantes.

**Ferramentas do roteiro** · Power BI ou Python
