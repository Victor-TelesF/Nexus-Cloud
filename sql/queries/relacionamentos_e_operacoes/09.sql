--Clientes com múltiplos contratos
--Quais empresas possuem três ou mais contratos ativos? 
--Quantos contratos cada uma possui?
SELECT c.nome_empresa AS cliente,
COUNT(a.id) AS "contratos ativos"
FROM nexus.clientes c
JOIN nexus.contratos a ON a.id_cliente = c.id
WHERE a.status = 'ativo' 
GROUP BY c.nome_empresa
HAVING COUNT(a.id) >= 3
ORDER BY "contratos ativos" DESC
LIMIT 20;
