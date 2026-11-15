-- 24 · Atraso nos pagamentos
-- Fonte: docs/02-desafios-sql.md#d24
--
-- Entre as cobranças que foram pagas depois do vencimento, qual foi a quantidade de dias de atraso
-- de cada pagamento? Qual é a média de dias de atraso?

--quantidade de cobranças com pagamentos pagos atrasados
SELECT COUNT(
    CASE WHEN data_vencimento < data_pagamento THEN id END
    ) AS atrasado
 FROM nexus.pagamentos LIMIT 30;

--tabela dos dias de atraso de cada cobrança
SELECT id AS id_pagamento, id_contrato, data_vencimento, data_pagamento, 
(data_pagamento - data_vencimento) AS dias_atrasados
FROM nexus.pagamentos
WHERE data_pagamento > data_vencimento
GROUP BY id;

--média dos dias de cobranças pagas atrasadas
WITH tabela_dias_atrasados AS(
    SELECT data_vencimento, data_pagamento, 
    (data_pagamento - data_vencimento) AS dias_atrasados
    FROM nexus.pagamentos
    WHERE data_pagamento > data_vencimento
    GROUP BY id
)
SELECT AVG(dias_atrasados) AS media_de_dias_atrasados
FROM tabela_dias_atrasados;
