# Gráficos e dashboard executivo

O comercial quer saber quando a procura mudou. O financeiro precisa distinguir dinheiro recebido de cobranças que ainda exigem acompanhamento. Os desafios 26–29 respondem a essas perguntas com gráficos. O 30 reúne as descobertas para a diretoria. Os enunciados completos estão no [catálogo](02-desafios-sql.md#d26).

## As quatro análises

| Pedido | Entrega | Como conferir |
| --- | --- | --- |
| [26 · Diagnóstico comercial](02-desafios-sql.md#d26) | Extração SQL e gráfico temporal em Python/pandas com a evolução das contratações. Escreva **três observações**, identificando os períodos de crescimento ou queda e os valores que sustentam a leitura. | Compare os pontos do gráfico com os novos contratos do relatório 20. Identifique meses sem contratações e períodos incompletos para interpretar a curva. |
| [27 · Análise de receita](02-desafios-sql.md#d27) | Extração SQL e visualização da **receita recebida por mês e categoria**. Mostre quais categorias mais contribuíram e como a participação delas mudou ao longo dos meses. | Escolha um mês e compare a soma das categorias com o caixa mensal do relatório 13. Atribua cada recebimento ao mês do pagamento. |
| [28 · Perfil dos clientes](02-desafios-sql.md#d28) | Extração SQL e visualização que permita comparar o número de clientes e a receita da carteira **por estado e por setor econômico**. Identifique onde há concentração de clientes e onde há concentração de receita. | Confira se uma empresa com várias cobranças conta uma única vez no total da carteira e se uma empresa sem recebimentos continua representada na distribuição de clientes. |
| [29 · Riscos financeiros](02-desafios-sql.md#d29) | Extração SQL e análise em Python/pandas com gráfico das cobranças atrasadas por cliente. Identifique onde se concentra o saldo em aberto e justifique prioridades de acompanhamento. | Concilie o saldo com as cobranças classificadas como atrasadas no relatório 14. Se exibir apenas uma parte dos clientes, informe a cobertura do recorte. |

Em cada item, vincule no [checklist](03-progresso.md) a extração SQL, o arquivo de análise e o gráfico renderizado ou uma forma de abri-lo. Identifique período, unidade dos eixos e filtros relevantes. A escolha do tipo de gráfico em 27–29 cabe ao estudante.

## 30 · Dashboard executivo

Entregue o **painel em Power BI ou Python** e uma **breve apresentação das descobertas mais relevantes**. O painel deve permitir responder às sete perguntas abaixo. As referências indicam trabalhos de apoio. Confira seus resultados antes de reutilizá-los.

| Indicador ou visual pedido | Pergunta que a diretoria deve conseguir responder | Referência para conferir |
| --- | --- | --- |
| Clientes | Qual o tamanho da carteira cadastrada? | Distribuição de clientes em 01 e 28 |
| Contratos | Quantos contratos existem no recorte apresentado? Se o indicador mostrar apenas os ativos, seu título explicita esse critério? | Situação administrativa em 06 e 11 |
| Receita recebida | Quanto entrou em caixa no período? | Receita efetiva em 13 |
| Cobranças atrasadas | Qual o montante em atraso na data de referência? | Saldo em aberto em 14 e 29 |
| Evolução mensal | Como o indicador mudou ao longo dos meses? A ilustração do roteiro usa a receita recebida. | Séries em 13 e 22 |
| Serviços mais contratados | Quais serviços lideram o ranking e quais contratos entram na contagem? | Ranking de ativos em 08, se esse for o recorte adotado |
| Receita por categoria | Quais categorias mais contribuíram para os recebimentos? | Receita por categoria em 16 e 27 |

**Apresentação.** Situe a diretoria no período analisado. Para cada descoberta escolhida, indique o que mudou ou se concentrou, mostre o dado que sustenta a afirmação e explique por que ele interessa ao negócio. O roteiro deixa a duração e o formato em aberto.

**Conferência final.** Abra o painel pelo caminho que será entregue ao leitor. Compare os totais com as consultas no mesmo recorte e teste os filtros utilizados. Anexe ao item 30 os links do painel, das fontes e da apresentação. Os números ilustrativos da conversa devem ser substituídos pelos valores apurados na base de estudo.
