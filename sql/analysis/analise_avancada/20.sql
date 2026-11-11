-- 20 · Evolução das contratações
-- Fonte: docs/02-desafios-sql.md#d20
--
-- Quantos novos contratos foram iniciados em cada mês do histórico disponível?
SELECT EXTRACT(YEAR FROM data_inicio) AS ano, 
EXTRACT(MONTH FROM data_inicio) AS mes, 
COUNT(id) AS quantidade_contratos
FROM nexus.contratos
WHERE data_inicio IS NOT NULL
GROUP BY ano, mes
ORDER BY ano, mes;
