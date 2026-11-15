-- 14 · Clientes inadimplentes
-- Fonte: docs/02-desafios-sql.md#d14
--
-- Quais clientes possuem cobranças registradas como atrasadas? Apresente a quantidade de cobranças
-- e o valor total em aberto por cliente.
SELECT c.nome_empresa AS nome_empresa, 
COUNT(p.id) AS cobranças_atrasadas, 
SUM(p.valor) AS valor_total
FROM nexus.clientes c
JOIN nexus.contratos a ON c.id = a.id_cliente
JOIN nexus.pagamentos p ON p.id_contrato = a.id
WHERE p.status = 'atrasado'
GROUP BY c.id, nome_empresa
ORDER BY cobranças_atrasadas DESC;