--Preços por categoria
--Qual é o preço médio, o menor preço e o maior preço dos serviços em cada categoria?
SELECT categoria AS Categoria, ROUND(AVG(preco_mensal), 2) AS "Preço Médio",
MIN(preco_mensal) AS "Menor Preço",
MAX(preco_mensal) AS "Maior Preço"
FROM nexus.servico 
GROUP BY Categoria
ORDER BY "Preço Médio"
LIMIT 20;