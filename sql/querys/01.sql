
--01. Distribuição geográfica
--Em quais estados a Nexus Cloud possui mais clientes? 
--Apresente a quantidade de clientes por estado, começando pelo maior.

SELECT estado, COUNT(id) AS clientes 
FROM nexus.clientes
GROUP BY estado
ORDER BY clientes DESC
limit 20;
