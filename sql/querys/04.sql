--infraestrutura disponível
--Quantos servidores estão ativos e qual é a capacidade total de armazenamento deles?
SELECT COUNT(nome_servidor) AS  "Quantidade de servidores ativos", 
SUM(capacidade_gb)/1024 AS "capacidade total TB"
FROM nexus.servidores 
WHERE status = 'ativo';