# Critérios de validação analítica

A validação verifica se a consulta, o resultado e sua interpretação respondem à pergunta de negócio. A execução sem erro é uma condição técnica; a aderência depende da população, da granularidade e das regras do indicador.

As perguntas estão no [catálogo](02-desafios-sql.md), as definições no [contexto de negócio](01-contexto-negocio.md) e os arquivos de cada entrega no [resumo dos desafios](03-progresso.md).

## Consulta e modelo

- Identificar o que cada linha representa: cliente, serviço, contrato, cobrança, mês ou indicador agregado. Conferir população, campos, filtros, ordenação e limites.
- Conferir nomes, tipos, chaves e restrições no [modelo SQL](../sql/models/model.sql). Nomes de empresa ou serviço não têm garantia de unicidade; a identidade vem da chave.
- Verificar a cardinalidade dos relacionamentos antes de agregar. Uma associação com várias cobranças pode repetir o preço mensal de um contrato e multiplicar contagens ou custos.
- Distinguir a seleção de registros individuais de condições sobre todos os registros de uma entidade. A existência de um contrato cancelado não demonstra ausência de contratos ativos.
- Conferir o tratamento de valores nulos, ausência de relacionamentos, conjuntos vazios e denominadores iguais a zero. A população da média deve corresponder à definição do indicador.

## Valores e períodos

- Separar receita mensal contratada, valor das cobranças e receita recebida. Para caixa, conferir status pago e data efetiva de pagamento.
- Preservar precisão monetária na apuração. Distinguir número de texto formatado e arredondar a apresentação sem alterar a seleção de rankings ou as comparações.
- Declarar numerador, denominador, unidade e período das taxas. Quantidade de clientes, quantidade de cobranças e valor cobrado produzem indicadores diferentes.
- Distinguir status administrativo de vigência em uma data. Datas finais são inclusivas conforme a regra do domínio; filtros relativos exigem data de referência.
- Separar meses de anos diferentes, ordenar séries cronologicamente e explicitar lacunas ou meses incompletos. A linha anterior observada pode não representar o mês civil anterior.
- Identificar custos e preços usados na estimativa mensal. A diferença do relatório 18 é um valor estimado em reais; os dados disponíveis não sustentam lucro operacional comprovado. A proporção histórica do relatório 21 não mede logo churn.

## Reconciliação e casos de verificação

A conferência deve usar um cálculo ou fonte independente quando disponível. Comparar apenas duas apresentações da mesma agregação não valida os registros de origem. Somar CSVs por mês, categoria e setor verifica a consistência entre exportações, mas não substitui uma nova apuração das cobranças no banco.

Os casos de verificação dependem da pergunta: entidades homônimas, contrato sem data final, cliente sem cobrança ou recebimento, pagamento na virada do mês, datas exatamente no limite, empates em rankings e denominador zero. A ausência de um caso na base sintética deve ficar registrada como limitação.

Uma execução de validação no PostgreSQL deve ser precedida pela inspeção do SQL, usar transação somente leitura e identificar data, fuso, versão do arquivo e limites de execução. Comparações monetárias podem usar `Decimal`. Hipóteses de desempenho exigem medições ou planos de execução pertinentes ao problema.

## Visualizações e interpretação

Os valores apresentados em gráficos e painéis devem conciliar com suas fontes no mesmo período e recorte. Conferir eixos, unidades, rótulos, legendas, filtros, cobertura de rankings e períodos incompletos. As [especificações visuais](04-visualizacoes-dashboard.md) definem os indicadores de cada análise.

Uma saída salva no notebook documenta uma execução anterior. Para validar a versão atual, é necessária execução sequencial com as fontes identificadas, seguida de conferência dos valores e inspeção visual. A interpretação deve apresentar observações sustentadas pelos dados, sem atribuir causalidade a associações nem extrapolar os resultados sintéticos para empresas reais.

## Registro da validação

O registro local de cada revisão identifica arquivo ou trecho, versão quando disponível, data, fonte, método, resultado e limitações. O resumo público indica a situação da entrega e aponta para seus arquivos.

Uma análise pode estar implementada e ainda ter validação pendente. Um resultado é validado somente no escopo e na versão examinados; alterações posteriores exigem conferir os pontos afetados. Quando faltarem dados, execução ou visual, o registro deve indicar o que permanece sem confirmação.
