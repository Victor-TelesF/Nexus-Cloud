-- 18 · Receita e custos operacionais
-- Fonte: docs/02-desafios-sql.md#d18
--
-- Qual é a receita mensal contratada pelos contratos administrativamente ativos e qual seria o
-- custo mensal estimado de fornecimento desses serviços? Calcule também a diferença entre os
-- valores.

--Tentativa de exploração
SELECT 
    EXTRACT(YEAR FROM p.data_pagamento) AS Ano,
    TO_CHAR(DATE_TRUNC('month', p.data_pagamento), 'TMMonth') AS Mes,
    SUM(p.valor) AS "Faturamento Total",
    SUM(s.custo_mensal) AS "Custo Estimado",
    (SUM(p.valor) - SUM(s.custo_mensal)) AS "Margem Finançeira"
FROM nexus.contratos c 
JOIN nexus.pagamentos p ON p.id_contrato = c.id
JOIN nexus.servico s ON s.id = c.id_servico
WHERE c.status = 'ativo'
    AND EXTRACT(YEAR FROM p.data_pagamento) = 2026
GROUP BY 
    EXTRACT(YEAR FROM p.data_pagamento),
    DATE_TRUNC('month', p.data_pagamento)
ORDER BY 
    Ano,
    DATE_TRUNC('month', p.data_pagamento);


--Resposta correta
SELECT SUM(s.preco_mensal) AS preco, SUM(s.custo_mensal) AS custo, (SUM(s.preco_mensal) - SUM(s.custo_mensal)) AS margem
FROM nexus.contratos c
JOIN nexus.servico s ON c.id_servico = s.id
WHERE c.status = 'ativo';