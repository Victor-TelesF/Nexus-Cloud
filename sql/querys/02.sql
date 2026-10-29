--Catálogo de serviços
--Quais serviços disponíveis possuem mensalidade superior a R$ 300? 
--Apresente seus nomes, categorias e preços, começando pelo mais caro.

SELECT nome_servico AS Serviço, categoria, preco_mensal AS preço
FROM nexus.servico
WHERE preco_mensal > 300 AND ativo = TRUE
ORDER BY preço DESC
LIMIT 10;