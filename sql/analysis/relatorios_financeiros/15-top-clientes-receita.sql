-- 15 · Maiores clientes por receita
-- Fonte: docs/02-desafios-sql.md#d15
--
-- Quais são os dez clientes que mais contribuíram para a receita efetivamente recebida pela Nexus
-- Cloud?

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
LIMIT 10;


SELECT 
    c.nome_empresa, 
    SUM(p.valor) AS valor_somado_cliente,
    ROUND((SUM(p.valor) / SUM(SUM(p.valor)) OVER ()) * 100, 4) AS "Porcentagem"
FROM nexus.clientes c
JOIN nexus.contratos a ON a.id_cliente = c.id
JOIN nexus.pagamentos p ON a.id = p.id_contrato
WHERE p.status = 'pago' AND p.data_pagamento IS NOT NULL
GROUP BY c.nome_empresa, c.id
ORDER BY ((SUM(p.valor) / SUM(SUM(p.valor)) OVER()) * 100) DESC
LIMIT 10;
