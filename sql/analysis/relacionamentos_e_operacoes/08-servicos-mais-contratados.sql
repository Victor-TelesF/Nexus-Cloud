--Serviços mais contratados
--Quais serviços possuem mais contratos ativos? 
--Apresente um ranking com os dez primeiros.
SELECT s.nome_servico AS Servico,
COUNT(c.id) AS Contrato
FROM nexus.servico s
JOIN nexus.contratos c ON s.id = c.id_servico
WHERE c.status = 'ativo'
GROUP BY s.nome_servico , s.id
ORDER BY Contrato DESC
LIMIT 10;