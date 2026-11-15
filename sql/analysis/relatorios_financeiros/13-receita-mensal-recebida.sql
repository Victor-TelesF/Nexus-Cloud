-- 13 · Receita mensal recebida
-- Fonte: docs/02-desafios-sql.md#d13
--
-- Quanto dinheiro a empresa efetivamente recebeu em cada mês?
-- Considere a data do pagamento, não a data do vencimento.

SELECT EXTRACT(YEAR FROM p.data_pagamento) AS ano, 
EXTRACT(MONTH FROM p.data_pagamento) AS mes,
SUM(p.valor) AS valor_total
FROM nexus.pagamentos p
WHERE p.data_pagamento IS NOT NULL AND p.status = 'pago'
GROUP BY ano, mes
ORDER BY ano, mes;