--infraestrutura disponível
--Quantos servidores estão ativos e qual é a capacidade total de armazenamento deles?
SELECT COUNT(nome_servidor) AS  "Quantidade de servidores ativos", 
(SUM(capacidade_gb)::NUMERIC / 1000):: NUMERIC(10,2) AS "capacidade total TB"
FROM nexus.servidores 
WHERE status = 'ativo';