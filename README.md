# Nexus Cloud

## Docker

O Compose inicia o PostgreSQL 17 e mantém os dados no volume `postgres_data`.
O serviço `app` é um comando sob demanda, pois o CLI atual termina após exibir
uma mensagem.

1. Crie o arquivo local de variáveis a partir do exemplo e ajuste a senha:

   ```bash
   cp .env.example .env
   ```

2. Inicie o banco:

   ```bash
   docker compose up -d db
   ```

3. Execute o CLI no container quando necessário:

   ```bash
   docker compose --profile cli run --rm app
   ```

O PostgreSQL fica acessível na máquina local em `localhost`, na porta definida
por `POSTGRES_PORT` (5432 por padrão). Entre containers, use o hostname `db`.
O banco só publica a porta no endereço local `127.0.0.1`.

`docker compose down` para e remove os containers, preservando os dados. A
integração da aplicação com o PostgreSQL ainda precisa ser implementada no
código do projeto.

## Executar SQL pelo VS Code

O workspace recomenda a extensão **PostgreSQL**, publicada pela Microsoft.
Instale-a pela aba Extensions (`Ctrl+Shift+X`) se o VS Code mostrar a
recomendação. Depois:

1. Inicie o banco com `docker compose up -d db`.
2. Abra a visão **PostgreSQL** na barra lateral e escolha **Add Connection**.
3. Informe servidor `127.0.0.1`, porta configurada em `POSTGRES_PORT` (5432 por
   padrão), usuário, senha e banco conforme seu `.env`.
4. Abra `sql/querys/01.sql`, conecte o editor à conexão salva e execute com
   `Shift+Enter` ou `Ctrl+Shift+E`.

A consulta de exemplo exibe o banco, o usuário e a versão do servidor no painel
de resultados. A extensão pode guardar a senha no cofre de credenciais do
sistema operacional; não coloque a senha em arquivos do workspace.
