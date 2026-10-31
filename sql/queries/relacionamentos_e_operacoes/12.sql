--Clientes sem contratos ativos
--Quais empresas já contrataram pelo menos um serviço,
--mas atualmente não possuem nenhum contrato administrativamente ativo?

SELECT c.nome_empresa AS Empresa,
COUNT(a.id) AS "Número de contratos"
FROM nexus.clientes c
JOIN nexus.contratos a ON a.id_cliente = c.id
WHERE a.status != 'ativo'
GROUP BY c.nome_empresa, c.id
ORDER BY "Número de contratos" DESC
LIMIT 50;


--verificando os status dos contratos pelo id do cliente, para verificar se a query acima esta correta.
SELECT e.nome_empresa, s.nome_servico, c.status AS "status do contrato"
FROM nexus.clientes e
JOIN nexus.contratos c ON c.id_cliente = e.id
JOIN nexus.servico s ON c.id_servico = s.id
WHERE e.id = 2329536075333960334;