-- 21 · Cancelamentos
-- Fonte: docs/02-desafios-sql.md#d21
--
-- Qual percentual do total de contratos registrados possui status cancelado? Apresente também a
-- quantidade absoluta.

WITH resumo AS(
    SELECT COUNT(c.id) AS total_contratos,
    COUNT(c.id) FILTER(WHERE c.status = 'cancelado') AS contratos_cancelados
    FROM nexus.contratos c
)
SELECT total_contratos, contratos_cancelados, 
ROUND(
    (contratos_cancelados::NUMERIC / NULLIF(total_contratos, 0)) * 100, 2
) AS percentual_cancelado
FROM resumo;