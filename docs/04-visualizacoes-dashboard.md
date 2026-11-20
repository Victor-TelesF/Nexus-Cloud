# Especificação de visualizações e dashboard

As análises 26–29 exploram evolução comercial, composição de receita, perfil da carteira e cobranças em atraso. O painel 30 reúne esses indicadores. As perguntas de negócio permanecem no [catálogo](02-desafios-sql.md#d26); o [acompanhamento técnico](03-progresso.md) concentra estados e evidências de validação.

A implementação utiliza Jupyter no VS Code para os notebooks e Python/Streamlit para o painel. O [guia do ambiente](06-ambiente-analise.md) descreve a execução local. Todos os resultados se referem à base sintética.

## 26 · Diagnóstico comercial

- **Pergunta de negócio:** como evoluem as contratações e em quais períodos há crescimento ou queda?
- **Dados necessários:** contratos identificados pela data de início, agregados por ano e mês. A fonte disponível é a [consulta 20](../sql/analysis/analise_avancada/20-evolucao-contratacoes-mensal.sql) e seu [CSV](../reports/analise_avancada/20_evolucao_contratacoes_mensal.csv). A exploração de cadastros usa `nexus.clientes` diretamente no banco.
- **Métrica e cálculo:** quantidade de novos contratos por mês de início, independentemente do status atual. Conferir meses sem movimento e meses incompletos antes de interpretar mudanças.
- **Visualização:** série temporal de contratos. O [notebook 26](../notebooks/26-diagnostico-comercial.ipynb) contém um gráfico de contratos e outro de cadastros de clientes.
- **Estado atual:** em desenvolvimento, com código e imagens salvas. O recorte inclusivo entre o mês final e o mês situado 24 meses antes pode abranger 25 competências; a janela deve ser conferida em relação ao título. O notebook ainda não reúne as três observações sustentadas por valores previstas no catálogo. Comparar cadastros e contratos agregados não demonstra quanto do crescimento veio de novos clientes ou de expansão de contas existentes.
- **Validação prevista:** comparar os pontos com o relatório 20, declarar o intervalo efetivo e conferir a interpretação. Sem validação analítica integral registrada.

## 27 · Receita por mês e categoria

- **Pergunta de negócio:** quais categorias mais contribuem para os recebimentos e como a composição muda ao longo dos meses?
- **Dados necessários:** cobranças pagas, data efetiva de pagamento e categoria do serviço associado ao contrato. Os CSVs dos relatórios [13](../reports/relatorios_financeiros/13_receita_mensal_recebida.csv) e [16](../reports/relatorios_financeiros/16_receita_recebida_por_categoria.csv) fornecem totais separados por mês e por categoria; o cruzamento mês/categoria está na consulta incorporada ao notebook.
- **Métricas e cálculo:** receita recebida por mês e categoria; participação de cada categoria no total do mesmo recorte. A atribuição temporal usa pagamento, e cobranças abertas ficam fora. Preço atual do catálogo não substitui o valor recebido.
- **Visualização:** composição acumulada por categoria, série mensal total e séries mensais por categoria. O [notebook 27](../notebooks/27-mix-receita-categorias.ipynb) contém essas consultas e gráficos, além de uma exploração de contratos pagantes e recebimentos por contrato.
- **Estado atual:** em desenvolvimento, com resultados e imagens salvos. Ainda faltam interpretação consolidada das mudanças de composição e validação integral da execução, dos valores e dos visuais.
- **Validação prevista:** conciliar a soma das categorias em cada mês com o relatório 13, no mesmo recorte, e o acumulado com o relatório 16. A conferência dos CSVs agregados não valida por si só a consulta mensal por categoria do notebook.

## 28 · Perfil dos clientes

- **Pergunta de negócio:** como a carteira e sua receita se distribuem por estado e setor econômico?
- **Dados necessários:** cadastro de clientes, estado, setor e recebimentos associados por contrato. Os relatórios [01](../sql/analysis/conhecendo_a_empresa/01-distribuicao-geografica.sql) e [23](../sql/analysis/analise_avancada/23-receita-por-setor.sql) são referências parciais; não fornecem sozinhos toda a segmentação prevista.
- **Métricas e cálculo:** quantidade de clientes e receita recebida por estado e setor, com período explícito. Cada cliente deve contar uma vez na sua população, inclusive sem recebimentos; várias cobranças não podem multiplicar a contagem de empresas.
- **Visualização prevista:** comparação entre concentração de clientes e de receita nos segmentos. O tipo de gráfico permanece em aberto.
- **Estado atual:** planejada. O [notebook 28](../notebooks/28-segmentacao-carteira.ipynb) contém somente a descrição do escopo, sem extração ou gráfico.
- **Validação prevista:** conciliar contagens com o cadastro, verificar clientes sem receita e conferir totais financeiros no período escolhido.

## 29 · Riscos financeiros

- **Pergunta de negócio:** em quais clientes se concentram as cobranças atrasadas e quais valores justificam acompanhamento prioritário?
- **Dados necessários:** cliente, contrato, cobrança, valor, vencimento e status atual. O [relatório 14](../reports/relatorios_financeiros/14_clientes_cobrancas_atrasadas.csv) oferece contagem e saldo atrasado por cliente.
- **Métricas e cálculo:** quantidade e valor das cobranças com status `atrasado`, e participação de cada cliente no saldo atrasado total da data de referência. Cobranças pendentes e pagamentos já regularizados não compõem esse saldo.
- **Visualização prevista:** concentração dos atrasos por cliente, com cobertura informada quando houver recorte dos maiores saldos. O tipo de gráfico permanece em aberto; faixas de envelhecimento da dívida não integram uma implementação existente.
- **Estado atual:** planejada. O [notebook 29](../notebooks/29-monitoramento-risco.ipynb) contém somente a descrição do escopo.
- **Validação prevista:** conciliar quantidade e valores com o relatório 14 e explicitar a cobertura do recorte. O modelo registra status atual, sem permitir reconstruir toda a trajetória histórica de inadimplência.

## 30 · Dashboard executivo

O painel deve responder às perguntas abaixo e acompanhar uma breve apresentação dos resultados. Esta tabela descreve requisitos; os indicadores ainda não estão implementados.

| Indicador | Definição e recorte a apresentar | Fonte de referência |
| --- | --- | --- |
| Clientes | Quantidade de empresas cadastradas no recorte declarado, sem duplicação por contrato ou cobrança. | Relatórios 01 e 28 |
| Contratos | Quantidade de contratos; explicitar se considera todos ou apenas os administrativamente ativos. | Relatórios 06 e 11 |
| Receita recebida | Soma de cobranças pagas, atribuída à data efetiva de pagamento no período. | Relatório 13 |
| Cobranças atrasadas | Valor em aberto com status atrasado na data de referência. | Relatórios 14 e 29 |
| Evolução mensal | Série de receita recebida por ano e mês, com indicação de lacunas e períodos incompletos. | Relatórios 13 e 22 |
| Serviços mais contratados | Ranking com o status dos contratos e o limite apresentados; o relatório 08 considera ativos. | Relatório 08 |
| Receita por categoria | Recebimentos por categoria no mesmo período dos demais indicadores financeiros. | Relatórios 16 e 27 |

**Estado atual:** estrutura inicial em [dashboards/app.py](../dashboards/app.py), com configuração da página e título. Os módulos de configuração e conexão existem, mas a página não os utiliza. Não há métricas, consultas, gráficos ou filtros na interface. A apresentação dos resultados também permanece pendente.

**Validação prevista:** abrir o painel pela forma documentada, comparar os totais com as fontes no mesmo recorte e testar os filtros que forem implementados. A apresentação deverá identificar período, observação, valor de suporte e limitações.

## Critérios de publicação dos visuais

Cada análise deve vincular sua extração, o notebook ou aplicação e o visual renderizado ou uma forma de abri-lo. Período, unidade dos eixos, filtros e origem dos dados precisam estar identificados. A validação inclui execução sequencial, reconciliação e inspeção visual, conforme os [critérios analíticos](05-criterios-correcao.md).
