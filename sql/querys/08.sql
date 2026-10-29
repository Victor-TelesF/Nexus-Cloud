--Serviços mais contratados
--Quais serviços possuem mais contratos ativos? 
--Apresente um ranking com os dez primeiros.

SELECT nome_servico
FROM nexus.servico servico
WHERE servico.id IN (
    SELECT id_servico
    FROM nexus.contratos
    WHERE status = 'ativo')
LIMIT 10;