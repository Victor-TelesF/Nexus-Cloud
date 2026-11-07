-- 16 · Receita por categoria
-- Fonte: docs/02-desafios-sql.md#d16
--
-- Qual categoria de serviços gerou a maior receita recebida durante o histórico disponível?

--Receita total recebida, do inicio até o histórico atual por categoria

WITH resumo_receita AS (

    SELECT servico.categoria, 
    SUM(pagamento.valor)  AS receita_categoria,
    SUM(SUM(pagamento.valor)) OVER() AS receita_total_geral
    FROM nexus.contratos contrato
    JOIN nexus.servico servico ON contrato.id_servico = servico.id
    JOIN nexus.pagamentos pagamento ON contrato.id = pagamento.id_contrato
    WHERE pagamento.status = 'pago' AND pagamento.data_pagamento IS NOT NULL
    GROUP BY servico.categoria

)
SELECT categoria, 
'R$ '|| to_char(receita_categoria, 'FM999G999G990D99') AS "Receita Total por Categoria", 
ROUND((receita_categoria / receita_total_geral) * 100, 2) || '%' AS percentual
FROM resumo_receita
ORDER BY (receita_categoria / receita_total_geral) DESC;

