--Clientes recentes
--Quais empresas se cadastraram nos últimos 90 dias?
--Apresente o nome, o setor, a cidade e a data de cadastro.

SELECT nome_empresa, setor, cidade, data_cadastro 
FROM nexus.clientes
WHERE data_cadastro >=  CURRENT_DATE - INTERVAL '90 days'
ORDER BY data_cadastro DESC
LIMIT 20;