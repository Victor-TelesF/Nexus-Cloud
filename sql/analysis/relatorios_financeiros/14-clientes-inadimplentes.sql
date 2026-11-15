-- 14 · Clientes inadimplentes
-- Fonte: docs/02-desafios-sql.md#d14
--
-- Quais clientes possuem cobranças registradas como atrasadas? Apresente a quantidade de cobranças
-- e o valor total em aberto por cliente.
SELECT c.nome_empresa AS "Nome Empresa", 
COUNT(p.id) AS "Cobranças Atrasadas", 
'R$ '|| SUM(p.valor) AS "Valor Total"
FROM nexus.clientes c
JOIN nexus.contratos a ON c.id = a.id_cliente
JOIN nexus.pagamentos p ON p.id_contrato = a.id
WHERE p.status = 'atrasado'
GROUP BY c.id, "Nome Empresa"
ORDER BY "Cobranças Atrasadas" DESC;