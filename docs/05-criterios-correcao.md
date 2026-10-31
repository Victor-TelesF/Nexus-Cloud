# Como avaliar uma entrega

Comece pelo pedido e escreva, em uma frase, o que cada linha ou indicador deve representar. Uma consulta pode executar e ainda responder a outra pergunta.

| Critério | O que o revisor deve conferir |
| --- | --- |
| Aderência ao pedido | População, período, campos pedidos, unidade, nível de detalhe, ordenação e limite. Um limite usado para explorar dados pode omitir parte da entrega. |
| Lógica e PostgreSQL | Colunas e tipos do [modelo](../sql/models/model.sql), relacionamentos pelas chaves corretas e diferença entre filtrar registros e testar uma condição para a empresa inteira. |
| Agregações e dinheiro | O que cada grupo representa, duplicação após cruzamentos, base dos percentuais, meses de anos distintos e data efetiva do recebimento. |
| Casos de teste | Escolher um caso que possa contradizer a hipótese. Conforme a pergunta, considerar empresas homônimas, contrato aberto sem data final, ausência de cobranças, pagamento na virada do mês, empates ou denominador zero. |
| Legibilidade | Nomes que expressem a métrica e a unidade, organização da consulta e separação entre a entrega e uma consulta auxiliar de diagnóstico. |
| Eficiência | Verificar trabalho repetido ou expansão indevida de linhas. Separar hipótese de medição. Só pedir um plano de execução quando ele ajudar a investigar um problema concreto. |
| Resultado e interpretação | Conferir o resultado sobre a base identificada. A interpretação deve citar o período e uma observação verificável, sem atribuir causalidade que os dados não sustentam. |
| Gráfico ou dashboard | Conciliar valores com a extração, verificar eixos, rótulos, unidades, legenda e comportamento dos filtros usados. Avaliar se o leitor consegue responder à pergunta usando o visual. |

## Parecer e devolutiva

- **Correta.** A evidência disponível sustenta os requisitos determinantes e os casos de teste relevantes. A conclusão da entrega ainda depende dos artefatos previstos para a etapa.
- **Parcialmente correta.** Descreva o requisito atendido e o caso específico em que o resultado diverge.
- **Incorreta.** Identifique o primeiro ponto em que a consulta muda a população, a granularidade ou o indicador solicitado.
- **Inconclusiva.** Registre a evidência que falta. Uma tentativa ainda sem parecer começa como “sem revisão”.

**Exemplo de pista para o relatório 12.** Uma empresa tem dois contratos, um ativo e um cancelado. Ela deveria aparecer entre as empresas sem contratos ativos? Peça ao estudante que preveja o resultado e depois o confira com sua consulta.

O revisor registra o ID, a data, o arquivo, o método (leitura ou execução), o parecer e a próxima verificação no [checklist](03-progresso.md). O estudante faz a próxima tentativa em suas próprias palavras.
