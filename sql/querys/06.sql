--Carteira de contratos
--Quais empresas possuem contratos administrativamente ativos? 
--Apresente a empresa, o serviço, o valor mensal e a data de início.

SELECT cliente.nome_empresa AS Empresa, 
servico.nome_servico  AS Servico,
servico.preco_mensal AS "Valor Mensal",
contrato.data_inicio AS "Data de contrato"
FROM nexus.contratos contrato
INNER JOIN nexus.clientes cliente
ON contrato.id_cliente = cliente.id
INNER JOIN nexus.servico servico
ON servico.id = contrato.id_servico
WHERE contrato.status = 'ativo'
ORDER BY "Valor Mensal" DESC
LIMIT 50; 
