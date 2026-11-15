-- 23 · Desempenho por setor
-- Fonte: docs/02-desafios-sql.md#d23
--
-- Quais setores econômicos dos clientes geraram mais receita para a Nexus Cloud?
SELECT cliente.setor, SUM(pagamento.valor) AS receita_recebida
FROM nexus.clientes cliente
JOIN nexus.contratos contrato ON contrato.id_cliente = cliente.id
JOIN nexus.pagamentos pagamento ON pagamento.id_contrato = contrato.id
WHERE pagamento.status = 'pago'
GROUP BY cliente.setor
ORDER BY receita_recebida DESC;
