-- 13 · Receita mensal recebida
-- Fonte: docs/02-desafios-sql.md#d13
--
-- Quanto dinheiro a empresa efetivamente recebeu em cada mês?
-- Considere a data do pagamento, não a data do vencimento.

SELECT EXTRACT(YEAR FROM p.data_pagamento) AS Ano, 
TO_CHAR(DATE_TRUNC('month', p.data_pagamento), 'TMMonth') AS Mes,
'R$ ' || SUM(p.valor) AS "Valor Total"
FROM nexus.pagamentos p
WHERE p.data_vencimento IS NOT NULL AND p.status = 'pago'
GROUP BY EXTRACT(YEAR FROM p.data_pagamento), DATE_TRUNC('month', p.data_pagamento)
ORDER BY Ano, DATE_TRUNC('month', p.data_pagamento);