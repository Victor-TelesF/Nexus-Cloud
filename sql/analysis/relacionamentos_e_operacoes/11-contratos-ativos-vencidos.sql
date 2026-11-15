--Contratos vencidos
--Quais contratos continuam registrados como ativos mesmo após sua data de encerramento? 
--Apresente a empresa, o serviço, a data de encerramento e os dias decorridos desde então.
SELECT cl.nome_empresa, 
s.nome_servico, c.data_fim, 
(CURRENT_DATE - c.data_fim) AS "Dias decorridos"
FROM nexus.contratos c
JOIN nexus.clientes cl ON cl.id = c.id_cliente
JOIN nexus.servico s ON s.id = c.id_servico
WHERE c.status = 'ativo' 
AND c.data_fim IS NOT NULL 
AND c.data_fim < CURRENT_DATE;
