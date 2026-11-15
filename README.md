<p align="center">
  <img src="docs/assets/nexus-cloud-banner.svg" alt="Nexus Cloud — inteligência de dados e análise financeira em nuvem" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL 17">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/uv-Package_Manager-DE5FE9?style=for-the-badge&logo=astral&logoColor=white" alt="uv">
</p>

---

# Nexus Cloud · Analytics Engineering & Data Intelligence

Como uma provedora de infraestrutura em nuvem B2B consegue distinguir com precisão **o que vendeu**, **o que faturou** e **o que de fato entrou no caixa**?

O **Nexus Cloud** é um projeto completo de Engenharia Analítica e Inteligência de Negócios voltado para o setor de infraestrutura e serviços recorrentes (B2B SaaS / IaaS). O repositório abrange desde a modelagem relacional transacional e formulação de consultas analíticas avançadas em **PostgreSQL**, até a reconciliação financeira de fluxo de caixa, estudos de coorte/comportamento em **Jupyter Notebooks (Pandas)** e entrega de um **Dashboard Executivo interativo em Streamlit**.

---

## 📌 Sumário Executivo do Projeto

| Dimensão | Destaques do Projeto |
| :--- | :--- |
| **Domínio de Negócio** | Provedor de Nuvem B2B (Hospedagem, Banco de Dados, Armazenamento e Computação). |
| **Base Analisada** | 1.000 clientes, 20 serviços de catálogo, 5.000 contratos, 30.000 faturas e 30 servidores físicos. |
| **Receita Efetiva Reconciliada** | **R$ 6.858.603,06** recebidos ao longo de 36 meses históricos de operação. |
| **Taxa de Inadimplência** | **15,37%** do montante cobrado classificado atualmente em atraso (**R$ 1.308.648,71**). |
| **Entregáveis Técnicos** | 25 consultas e relatórios analíticos em SQL, 4 diagnósticos visuais e 1 painel executivo. |

---

## 🏗️ Modelo de Dados & Regras de Negócio

O schema transacional `nexus` foi desenhado com restrições estritas de integridade relacional, tipos monetários exatos (`NUMERIC(10,2)`), chaves compostas e validações cronológicas:

<p align="center">
  <img src="docs/assets/data-model.svg" alt="Modelo de dados do schema nexus" width="85%">
</p>

### Entidades do Negócio

* **`nexus.clientes`**: Empresas cadastradas por setor e região. Permite cadastros prospectivos sem contratação imediata.
* **`nexus.servico`**: Catálogo de produtos com preço mensal e custo operacional estimado por categoria.
* **`nexus.contratos`**: Contratações de serviços com ciclo de vida administrativo (`ativo`, `suspenso`, `cancelado`) e vigência temporal.
* **`nexus.pagamentos`**: Cobranças mensais geradas por contrato. Distingue data de vencimento da data efetiva de liquidação (`pago`, `pendente`, `atrasado`).
* **`nexus.servidores`**: Infraestrutura física instalada com capacidade (GB), custo mensal e localização geográfica em quatro regiões globais.

> 📖 **Regras e Decisões de Negócio:** Consulte os detalhes em [Contexto de Negócio](docs/01-contexto-negocio.md) e as definições DDL em [sql/models/model.sql](sql/models/model.sql).

---

## 🚀 Trilha Analítica & Descobertas Chave

O percurso é estruturado em cinco etapas sequenciais de maturidade analítica:

```
[ Etapa 1: Conhecendo a Empresa ] ────► Distribuição de clientes, catálogo e servidores disponíveis
                │
[ Etapa 2: Operações e Vínculos ] ────► Carteira de contratos, retenção de clientes e serviços sem demanda
                │
[ Etapa 3: Relatórios Financeiros ] ──► Caixa realizado, top clientes, taxa de inadimplência e margem
                │
[ Etapa 4: Análise Avançada ] ────────► Séries temporais, churn rate, janelas móveis (LAG) e outliers
                │
[ Etapa 5: Visualizações & BI ] ──────► Diagnóstico comercial, risco financeiro e Dashboard Executivo
```

### 1. Conhecendo a Empresa (Desafios 01 a 05)
* **Concentração Geográfica:** Forte presença em polos econômicos liderados por São Paulo e Rio de Janeiro.
* **Catálogo de Serviços:** 11 opções de serviços com mensalidade superior a R$ 300, cobrindo planos de entrada a corporativos.
* **Capacidade de Infraestrutura:** 27 servidores ativos totalizando **95,74 TB** de armazenamento distribuídos entre regiões no Brasil, EUA e Europa.

### 2. Relacionamentos e Operações (Desafios 06 a 12)
* **Ativação da Base:** Dos 1.000 clientes cadastrados, 184 nunca chegaram a contratar um serviço e 20 empresas cancelaram todos os contratos históricos e encontram-se inativas.
* **Concentração de Contratos:** 492 empresas possuem três ou mais contratos simultâneos ativos, evidenciando alto potencial de *expansion revenue* (upsell/cross-sell).
* **Eficiência do Portfólio:** Identificação de serviços do catálogo com demanda nula, subsidiando decisões de descontinuação de produtos.

### 3. Inteligência Financeira e Caixa (Desafios 13 a 19)
* **Reconciliação Contábil vs. Caixa:** Separação precisa entre regime de competência (vencimento) e regime de caixa (pagamento efetivo), totalizando **R$ 6,85M** recebidos em 36 meses.
* **Categoria Líder:** O segmento de **Banco de Dados** lidera as receitas, gerando **R$ 3.196.190,92** (46,60% de todo o caixa realizado).
* **Gestão de Risco e Inadimplência:** 660 clientes possuem cobranças atrasadas, somando **R$ 1,30M** em aberto. Os 5 maiores clientes foram analisados quanto ao impacto em caso de inadimplência.
* **Margem Operacional Teórica:** A receita mensal contratada ativa (R$ 1,06M/mês) supera o custo operacional direto estimado do catálogo (R$ 567k/mês), gerando margem de contribuição contratada de R$ 497k/mês.

### 4. Análise Avançada com Window Functions (Desafios 20 a 25)
* **Evolução Cronológica:** Acompanhamento mês a mês das novas contratações e cálculo de variação percentual de receita utilizando funções de janela (`LAG() OVER`).
* **Taxa de Cancelamento (*Logo Churn*):** 16,32% dos contratos gerados na história da empresa foram cancelados (816 de 5.000).
* **Comportamento de Liquidação:** De 7.107 faturas que foram pagas com atraso, mensurou-se a curva média de dias decorridos para guiar a régua de cobrança automática.
* **Clientes Acima da Média:** Identificação dos 310 clientes que geram faturamento superior à média geral de todos os cadastrados (incluindo base inativa).

### 5. Diagnósticos Visuais e Dashboard Executivo (Desafios 26 a 30)
* **Diagnóstico Comercial ([26-diagnostico-comercial.ipynb](notebooks/26-diagnostico-comercial.ipynb)):** Análise da curva de aceleração de contratações nos últimos 24 meses, decompondo novos clientes vs. expansão de contas existentes.
* **Análise de Mix de Receita ([27-mix-receita-categorias.ipynb](notebooks/27-mix-receita-categorias.ipynb)):** Evolução visual da participação das categorias no faturamento mensal.
* **Segmentação de Carteira ([28-segmentacao-carteira.ipynb](notebooks/28-segmentacao-carteira.ipynb)):** Matriz de concentração por estado e setor econômico.
* **Monitoramento de Risco ([29-monitoramento-risco.ipynb](notebooks/29-monitoramento-risco.ipynb)):** Curva de envelhecimento da dívida (*aging lists*) e concentração de saldo em aberto por cliente.
* **Painel Executivo ([dashboards/app.py](dashboards/app.py)):** Aplicação interativa em Streamlit reunindo os 7 KPIs estratégicos para a diretoria.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Banco de Dados** | PostgreSQL 17 | Armazenamento relacional, queries analíticas, CTEs e Window Functions. |
| **Linguagem & Análise** | Python 3.13 / Pandas | Extração de dados, manipulação de dataframes e estatística descritiva. |
| **Visualização & BI** | Matplotlib / Seaborn / Streamlit | Criação de gráficos analíticos e desenvolvimento do painel executivo. |
| **Infraestrutura** | Docker / Docker Compose | Orquestração do banco e do pipeline de carga de dados sintéticos. |
| **Gerenciamento de Pacotes** | uv (Astral) | Resolução ultra-rápida e determinística de dependências Python (`uv.lock`). |

---

## 📁 Estrutura do Repositório

```text
Nexus-Cloud/
├── docs/                           # Documentação técnica, regras e acompanhamento
│   ├── 01-contexto-negocio.md      # Regras de negócio, catálogo e decisões analíticas
│   ├── 02-desafios-sql.md          # Catálogo completo dos 30 desafios de análise
│   ├── 03-progresso.md             # Checklist oficial de entregas, status e pareceres
│   ├── 04-visualizacoes-dashboard.md # Especificações da etapa visual e do painel
│   ├── 05-criterios-correcao.md    # Rubrica de validação e critérios pedagógicos
│   ├── 06-ambiente-analise.md      # Guia de configuração de kernel e dependências
│   └── assets/                     # Diagramas e identidades visuais do projeto
├── sql/
│   ├── models/
│   │   └── model.sql               # DDL do banco (DDL, restrições e relacionamentos)
│   └── analysis/                   # Consultas SQL versionadas por etapa de maturidade
│       ├── conhecendo_a_empresa/   # Consultas 01 a 05
│       ├── relacionamentos_e_operacoes/ # Consultas 06 a 12
│       ├── relatorios_financeiros/ # Consultas 13 a 19
│       └── analise_avancada/       # Consultas 20 a 25
├── reports/                        # Resultados das consultas exportados em CSV
├── notebooks/                      # Análises exploratórias e diagnósticos visuais
│   ├── 26-diagnostico-comercial.ipynb                    # Diagnóstico comercial (curva de contratações)
│   ├── 27-mix-receita-categorias.ipynb                    # Análise de receita por categoria e mês
│   ├── 28-segmentacao-carteira.ipynb                    # Perfil dos clientes (estado vs. setor)
│   └── 29-monitoramento-risco.ipynb                    # Riscos financeiros e concentração de atrasos
├── dashboards/                     # Aplicação interativa em Streamlit
│   ├── app.py                      # Código da interface executiva do dashboard
│   ├── database.py                 # Conexão com o PostgreSQL via SQLAlchemy/psycopg
│   └── config.py                   # Parâmetros de ambiente e banco de dados
├── seeds/                          # Pipeline de geração de dados sintéticos realistas
│   ├── seed.py                     # Script de geração com sementes pseudoaleatórias
│   └── Dockerfile                  # Container do serviço de carga
├── compose.yaml                    # Orquestração dos serviços PostgreSQL e Seed
└── pyproject.toml                  # Configuração do projeto e dependências gerenciadas por uv
```

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
* **Docker** e **Docker Compose** instalados;
* **Python 3.13** e gerenciador **[uv](https://github.com/astral-sh/uv)** (recomendado) ou `pip`.

### 1. Clonar o repositório e configurar variáveis
```bash
git clone https://github.com/seu-usuario/Nexus-Cloud.git
cd Nexus-Cloud

# Copiar arquivo de exemplo para ambiente local
cp .env.example .env
```

### 2. Subir o banco de dados e carregar os dados
Execute o Compose para subir o PostgreSQL 17 e rodar o container de carga (`seed`):
```bash
docker compose up -d --build
docker compose wait seed
docker compose logs seed
```
> O serviço `seed` encerra com código `0` assim que a carga de 1.000 clientes, 5.000 contratos e 30.000 pagamentos for concluída.

### 3. Configurar o ambiente Python e dependências
Utilizando o `uv`:
```bash
uv sync --locked
```

### 4. Executar as análises e o dashboard
* **Jupyter Notebooks:** Abra os arquivos na pasta `notebooks/` selecionando o kernel Python gerado na pasta `.venv/`.
* **Dashboard Executivo Streamlit:**
  ```bash
  uv run streamlit run dashboards/app.py
  ```
  Acesse a aplicação no navegador em `http://localhost:8501`.

---

## 📋 Acompanhamento e Governança de Entregas

Todas as entregas de consultas, diagnósticos e revisões pedagógicas são rastreadas de forma transparente com hash de versão, métodos de verificação e pareceres formais no documento:

👉 **[Acesse o Checklist de Progresso e Evidências (docs/03-progresso.md)](docs/03-progresso.md)**

---

## 📄 Licença

Este projeto é desenvolvido para fins de estudo, portfólio e análise de dados. Fique à vontade para explorar, propor melhorias ou utilizá-lo como referência técnica.
