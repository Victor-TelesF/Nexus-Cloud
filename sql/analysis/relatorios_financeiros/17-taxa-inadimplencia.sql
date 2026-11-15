-- 17 · Taxa de inadimplência
-- Fonte: docs/02-desafios-sql.md#d17
--
-- Qual percentual do valor total das cobranças registradas corresponde às cobranças atualmente
-- classificadas como atrasadas?
SELECT SUM(p.valor) AS valor_total, 
SUM(CASE WHEN p.status = 'atrasado' THEN p.valor ELSE 0 END) AS "Total Atrasado",
ROUND(
    (SUM(CASE WHEN p.status = 'atrasado' THEN p.valor ELSE 0 END) / SUM(p.valor)) *100, 2
) AS taxa_inadimplencia
FROM nexus.pagamentos p;