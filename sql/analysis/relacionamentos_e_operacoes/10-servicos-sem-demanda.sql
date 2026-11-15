--Serviços sem demanda
--Quais serviços do catálogo nunca foram contratados, 
--independentemente de estarem disponíveis atualmente?
SELECT s.nome_servico, s.categoria
FROM nexus.servico s
WHERE NOT EXISTS (
    SELECT id_servico
    FROM nexus.contratos c
    WHERE c.id_servico = s.id
);