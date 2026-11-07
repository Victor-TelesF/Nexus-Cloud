-- 17 · Taxa de inadimplência
-- Fonte: docs/02-desafios-sql.md#d17
--
-- Qual percentual do valor total das cobranças registradas corresponde às cobranças atualmente
-- classificadas como atrasadas?
SELECT 'R$ ' || to_char(SUM(p.valor), 'FM999G999G990D99') AS "Valor Total", 
'R$ ' || to_char(SUM(CASE WHEN p.status = 'atrasado' THEN p.valor ELSE 0 END), 'FM999G999G990D99') AS "Total Atrasado",
ROUND(
    (SUM(CASE WHEN p.status = 'atrasado' THEN p.valor ELSE 0 END) / SUM(p.valor)) *100, 2
) || '%' AS "Taxa de Inadimplência"
FROM nexus.pagamentos p;