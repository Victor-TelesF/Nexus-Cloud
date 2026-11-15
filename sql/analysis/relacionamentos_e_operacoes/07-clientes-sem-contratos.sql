--Clientes sem contratos
--Quais empresas estão cadastradas, mas nunca contrataram nenhum serviço?
SELECT cliente.nome_empresa AS "Nome Empresa"
FROM nexus.clientes cliente
WHERE NOT EXISTS (
    SELECT id_cliente FROM nexus.contratos contrato 
    WHERE contrato.id_cliente = cliente.id)
ORDER BY "Nome Empresa" ASC;