-- 19 · Concentração de receita
-- Fonte: docs/02-desafios-sql.md#d19
--
-- Qual percentual de toda a receita recebida foi gerado individualmente pelos cinco maiores
-- clientes?

WITH total_por_cliente AS (
    SELECT 
        c.id,
        c.nome_empresa,
        SUM(p.valor) AS total_cliente,
        SUM(SUM(p.valor)) OVER() AS total_geral
    FROM nexus.clientes c
    JOIN nexus.contratos a ON a.id_cliente = c.id
    JOIN nexus.pagamentos p ON a.id = p.id_contrato
    WHERE p.status = 'pago' AND p.data_pagamento IS NOT NULL
    GROUP BY c.id, c.nome_empresa
),
grandes_clientes AS (
    SELECT 
        total_cliente,
        total_geral,
        (total_cliente / total_geral) * 100 AS percentual_contribuicao
    FROM total_por_cliente
    ORDER BY total_cliente DESC
    LIMIT 5
)
SELECT 
    MAX(total_geral) AS "Total Geral da Empresa",
    SUM(total_cliente) AS "Contribuição",
    ROUND(SUM(percentual_contribuicao), 2) AS "Percentual de contribuição"
FROM grandes_clientes;

SELECT c.nome_empresa AS Cliente, ROUND(
    (SUM(p.valor) / SUM(SUM(p.valor)) OVER()) * 100, 2
) || '%' AS "Percentual de contribuição"
FROM nexus.clientes c
JOIN nexus.contratos a ON a.id_cliente = c.id
JOIN nexus.pagamentos p ON a.id = p.id_contrato
WHERE p.status = 'pago' AND p.data_pagamento IS NOT NULL
GROUP BY c.nome_empresa, c.id
ORDER BY 
    ((SUM(p.valor) / SUM(SUM(p.valor)) OVER()) * 100) DESC
LIMIT 5;

