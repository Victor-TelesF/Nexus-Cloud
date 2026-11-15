--Clientes sem contratos ativos
--Quais empresas já contrataram pelo menos um serviço,
--mas atualmente não possuem nenhum contrato administrativamente ativo?
SELECT c.nome_empresa AS Empresa,
COUNT(a.id) AS "Número de contratos"
FROM nexus.clientes c
JOIN nexus.contratos a ON a.id_cliente = c.id
WHERE NOT EXISTS (
    SELECT a2.id
    FROM nexus.contratos a2
    WHERE a2.id_cliente = c.id AND a2.status = 'ativo'
)
GROUP BY c.nome_empresa, c.id
ORDER BY "Número de contratos" DESC
LIMIT 50;