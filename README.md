<p align="center">
  <img src="docs/assets/nexus-cloud-banner.svg" alt="Nexus Cloud — laboratório de SQL e análise de dados com PostgreSQL" width="100%">
</p>

<p align="center">
  <strong>De perguntas de negócio a consultas SQL.</strong><br>
  Um projeto de estudo sobre os dados de uma empresa fictícia de serviços em nuvem.
</p>

<p align="center">
  <a href="#o-projeto">O projeto</a> ·
  <a href="#modelo-de-dados">Modelo de dados</a> ·
  <a href="#exercícios">Exercícios</a> ·
  <a href="#ambiente-local">Ambiente local</a>
</p>

## O projeto

O Nexus Cloud é um exercício prático de **PostgreSQL e análise de dados**. A partir de uma base fictícia com clientes, serviços, contratos, pagamentos e servidores, o projeto explora como transformar perguntas de negócio em consultas e interpretar seus resultados.

O foco está no raciocínio: compreender os relacionamentos, escolher filtros e agregações adequados e verificar se cada consulta realmente responde à pergunta proposta.

| Em estudo | Aplicação no projeto |
| :--- | :--- |
| Modelagem relacional | Chaves primárias, estrangeiras e restrições de integridade |
| Consultas SQL | Filtros, ordenação, funções de data e subconsultas |
| Análise de dados | Agregações, rankings e cruzamento entre tabelas |
| Leitura crítica | Interpretação dos resultados e revisão da lógica das consultas |

**Momento atual:** ambiente local recriado e banco populado; as primeiras oito perguntas estão respondidas. Os exercícios seguintes estão em desenvolvimento. Visualizações com Python fazem parte da evolução planejada.

> Os dados são fictícios e têm finalidade educacional. Os resultados descrevem apenas o cenário simulado.

## Modelo de dados

As cinco tabelas estão organizadas no schema `nexus`. O modelo conecta clientes e serviços por meio de contratos, que possuem seus respectivos pagamentos. Os servidores representam a infraestrutura e são analisados separadamente.

<p align="center">
  <img src="docs/assets/data-model.svg" alt="Modelo relacional: clientes e serviços possuem contratos; contratos possuem pagamentos. Servidores não têm chaves estrangeiras para as demais tabelas." width="100%">
</p>

| Tabela | O que representa |
| :--- | :--- |
| `clientes` | Empresas cadastradas, setor e localização |
| `servico` | Catálogo, categorias, preços e custos mensais |
| `contratos` | Vínculo entre cliente e serviço, datas e situação contratual |
| `pagamentos` | Cobranças dos contratos, valores, vencimentos e situação do pagamento |
| `servidores` | Região, capacidade de armazenamento, custo e situação operacional |

A definição das tabelas e das restrições está em [`sql/models/model.sql`](sql/models/model.sql).

## Exercícios

Cada arquivo reúne a pergunta original e a consulta elaborada durante o estudo. As oito primeiras respostas exploram:

| Nº | Pergunta / tema | Consulta |
| :---: | :--- | :---: |
| 01 | Distribuição de clientes por estado | [Abrir](sql/querys/01.sql) |
| 02 | Serviços disponíveis com mensalidade acima de R$ 300 | [Abrir](sql/querys/02.sql) |
| 03 | Empresas cadastradas nos últimos 90 dias | [Abrir](sql/querys/03.sql) |
| 04 | Quantidade e capacidade dos servidores ativos | [Abrir](sql/querys/04.sql) |
| 05 | Preço médio, mínimo e máximo por categoria | [Abrir](sql/querys/05.sql) |
| 06 | Empresas e serviços com contratos ativos | [Abrir](sql/querys/06.sql) |
| 07 | Clientes que nunca contrataram um serviço | [Abrir](sql/querys/07.sql) |
| 08 | Ranking dos dez serviços com mais contratos ativos | [Abrir](sql/querys/08.sql) |

As respostas fazem parte de um processo de aprendizado e revisão. Sua presença no repositório não significa que todos os critérios de correção já foram validados.

## Ambiente local

O banco utiliza **PostgreSQL 17**, executado com **Docker Compose**. As consultas são trabalhadas diretamente no **VS Code**, com a extensão PostgreSQL da Microsoft recomendada pelo workspace.

### Iniciar o banco

Com Docker e Docker Compose disponíveis, crie o arquivo de configuração na primeira execução:

```bash
cp .env.example .env
```

Ajuste as credenciais no `.env`, incluindo a senha, e inicie o serviço:

```bash
docker compose up -d db
```

O banco fica disponível em `127.0.0.1:5432`, ou na porta definida em `POSTGRES_PORT`. Os dados persistem no volume `postgres_data`.

> O ambiente de estudo atual já está populado. Em uma instalação nova, o Compose inicia somente o PostgreSQL: a criação do schema, das tabelas e a carga de dados não são automáticas. O repositório contém a definição das tabelas, mas ainda não inclui um script de população.

### Executar as consultas no VS Code

1. Instale a extensão **PostgreSQL**, da Microsoft (`ms-ossdata.vscode-pgsql`), recomendada pelo projeto.
2. Na visão PostgreSQL, escolha **Add Connection** e informe os parâmetros de conexão:

   | Parâmetro | Valor |
   | :--- | :--- |
   | Servidor | `127.0.0.1` |
   | Porta | `POSTGRES_PORT` do `.env` — padrão `5432` |
   | Banco | `POSTGRES_DB` do `.env` |
   | Usuário | `POSTGRES_USER` do `.env` |
   | Senha | `POSTGRES_PASSWORD` do `.env` |

3. Abra um arquivo em [`sql/querys/`](sql/querys/), selecione a conexão e execute a consulta pelo editor.
4. Confira o resultado e compare-o com a pergunta registrada no início do arquivo.

Para encerrar os containers e preservar o volume de dados:

```bash
docker compose down
```

## Organização

```text
Nexus-Cloud/
├── docs/assets/           # Imagens da documentação
├── sql/
│   ├── models/model.sql  # Definição das tabelas e restrições
│   └── querys/           # Perguntas e consultas do estudo
├── src/nexus_cloud/      # Estrutura inicial do pacote Python
├── .env.example          # Exemplo de configuração local
├── compose.yaml          # PostgreSQL e perfil opcional do CLI
├── Dockerfile            # Ambiente do pacote Python
└── pyproject.toml        # Metadados e dependências Python
```

## Próximos passos

- Continuar os exercícios e revisar a lógica das respostas.
- Documentar resultados e interpretações das análises.
- Explorar visualizações com Python, pandas, Matplotlib e seaborn.

O pacote Python ainda é uma estrutura inicial; a integração com o banco e as visualizações serão desenvolvidas em etapas posteriores.
