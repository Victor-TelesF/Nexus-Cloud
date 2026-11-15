-- 22 · Crescimento da receita
-- Fonte: docs/02-desafios-sql.md#d22
--
-- Como evoluiu a receita efetivamente recebida ao longo dos meses? Calcule a variação percentual
-- de cada mês em relação ao anterior.

WITH resumo AS(
    SELECT EXTRACT(
        YEAR FROM p.data_pagamento
        ) AS ano,
    EXTRACT(
        MONTH FROM p.data_pagamento
        ) AS mes,
    SUM(p.valor) AS total
    FROM nexus.pagamentos p
    WHERE p.data_vencimento IS NOT NULL AND p.status = 'pago'
    GROUP BY ano, mes
    ORDER BY ano, mes
)
SELECT ano,mes,total,
ROUND(
    ((total / NULLIF(LAG(total, 1, 0) OVER(ORDER BY ano, mes), 0) - 1) * 100), 2
) AS variacao_percentual 
FROM resumo
ORDER BY ano, mes;

