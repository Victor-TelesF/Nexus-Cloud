# Jupyter e Streamlit no VS Code

O ambiente local utiliza **Jupyter Notebook** nas análises 26–29 e **Streamlit** no painel 30. pandas, Matplotlib e seaborn estão disponíveis no mesmo ambiente Python. A [especificação visual](04-visualizacoes-dashboard.md) distingue funcionalidades existentes e requisitos planejados.

## Preparação

1. Abra a pasta **Nexus-Cloud** inteira no VS Code, pois as configurações em `.vscode/` pertencem a essa raiz. Abrir somente `notebooks/` não carrega essas configurações.
2. Instale as extensões recomendadas pelo projeto: Python, Pylance, Jupyter e PostgreSQL da Microsoft. Elas estão listadas em [.vscode/extensions.json](../.vscode/extensions.json); a recomendação não instala extensões automaticamente.
3. Com Python 3.13 ou superior e [uv](https://docs.astral.sh/uv/getting-started/installation/) disponíveis, execute **Terminal → Run Task → Nexus: sincronizar ambiente Python**. A tarefa usa `uv sync --locked` para preparar `.venv` a partir de `pyproject.toml` e `uv.lock`. Repita após mudanças nas dependências, não a cada notebook.
4. Em **Python: Select Interpreter**, escolha o Python de `.venv` caso o VS Code já tenha guardado outro interpretador. O padrão do projeto aponta para `.venv`, mas não substitui uma seleção anterior do editor.

## Notebooks sem ajuste manual de caminho

Crie os arquivos `.ipynb` em [notebooks/](../notebooks/). No seletor **Select Kernel**, escolha **Python Environments → .venv**. O kernel é o processo Python que executa as células; ele precisa usar o ambiente com as dependências do projeto.

Em [.vscode/settings.json](../.vscode/settings.json), a opção `jupyter.notebookFileRoot` está definida como `${workspaceFolder}`. Assim, notebooks locais abertos neste workspace começam a executar na raiz do repositório, mesmo quando o arquivo está em uma subpasta. Caminhos como `sql/analysis/` passam a partir dessa raiz, e os módulos Python do projeto podem ser importados sem adicionar a pasta pai a `sys.path` em cada notebook. `python.analysis.extraPaths` também inclui a raiz para o editor reconhecer esses imports.

Reinicie o kernel dos notebooks que já estavam abertos antes da mudança. Para conferir o diretório, execute uma vez em uma célula:

```python
from pathlib import Path

Path.cwd()
```

O resultado deve ser a pasta **Nexus-Cloud**. Não use `Path.cwd().parent` para ajustar o caminho: a execução já parte da raiz. Essa configuração é do VS Code para kernels locais; ela não configura um servidor Jupyter externo.

Os comandos opcionais `%load_ext autoreload` e `%autoreload 2` recarregam módulos locais editados. Eles não alteram o diretório de execução e não estão habilitados no workspace.

## Abrir o Streamlit

Execute **Terminal → Run Task → Nexus: iniciar Streamlit**. Abra **http://127.0.0.1:8501** no navegador ou no **Simple Browser** do VS Code. O servidor roda no ambiente `.venv`; sua interface é uma página web, enquanto a edição continua no VS Code. Encerre com `Ctrl+C` no terminal da tarefa.

O arquivo inicial é [dashboards/app.py](../dashboards/app.py). Ele configura a página e exibe o título; os indicadores, gráficos e filtros ainda estão planejados. A abertura dessa página não valida acesso ao banco. A tarefa inicia na raiz do repositório e inclui essa raiz no `PYTHONPATH`, permitindo compartilhar módulos locais com os notebooks. A configuração [.streamlit/config.toml](../.streamlit/config.toml) mantém o servidor local e habilita a atualização ao salvar.

Se preferir o terminal, execute na raiz:

```bash
uv run --locked python -m streamlit run dashboards/app.py
```

Mantenha as extrações em `sql/analysis/`, as explorações em `notebooks/` e o painel em `dashboards/`. As configurações não iniciam o PostgreSQL nem executam consultas ou carga de dados. Para conectar suas análises, use o endereço local e as credenciais do seu `.env`, sem gravar senhas nos notebooks ou nas saídas salvas. A tarefa do Streamlit não injeta as variáveis de `.env` no processo. Ao importar `dashboards.database`, o módulo `dashboards.config` lê esse arquivo com Pydantic Settings, a partir do diretório de execução. Esse caminho exige `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_DB` e `POSTGRES_PASSWORD`; o host padrão é `127.0.0.1`, com opção `DB_HOST`. O suporte a `DATABASE_URL` descrito no gerador de dados não é usado por essa configuração do dashboard.

## Referências

[notebooks e seleção de kernel no VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks), [interpretador padrão](https://code.visualstudio.com/docs/python/settings-reference), [opções da extensão Jupyter](https://github.com/microsoft/vscode-jupyter/blob/main/package.json) e [configuração do Streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml).
