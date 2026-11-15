-- 25 · Clientes acima da média
-- Fonte: docs/02-desafios-sql.md#d25
--
-- Quais clientes geraram uma receita total superior à média de receita por cliente, considerando
-- todos os clientes cadastrados, inclusive aqueles sem pagamentos?

WITH receita_cliente AS(
SELECT c.id, c.nome_empresa,
    COALESCE(
        SUM(
            CASE
                WHEN pagamento.status = 'pago' AND pagamento.data_pagamento IS NOT NULL
                THEN pagamento.valor
                ELSE 0
            END
        ),
        0
    ) AS receita_total
    FROM nexus.clientes c
    LEFT JOIN nexus.contratos contrato ON contrato.id_cliente = c.id
    LEFT JOIN nexus.pagamentos pagamento ON pagamento.id_contrato = contrato.id
    GROUP BY c.id, c.nome_empresa
),
media_geral AS(
    SELECT COALESCE(AVG(receita_total),0) AS media
    FROM receita_cliente
)
SELECT r.id, r.nome_empresa, r.receita_total
FROM receita_cliente r
CROSS JOIN media_geral m
WHERE r.receita_total > m.media
ORDER BY r.receita_total DESC;