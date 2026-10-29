
CREATE TABLE nexus.clientes (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_empresa VARCHAR(100) NOT NULL,
    setor varchar(50) NOT NULL,
    cidade varchar(80) NOT NULL,
    estado varchar(2) NOT NULL,
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT data_nao_futura CHECK (data_cadastro <= CURRENT_DATE),
    CONSTRAINT estado_correto CHECK (LENGTH(estado) = 2)
);


CREATE TABLE nexus.servico (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_servico VARCHAR(250) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco_mensal NUMERIC(10,2) NOT NULL,
    custo_mensal NUMERIC(10,2) NOT NULL,
    ativo BOOLEAN NOT NULL,

    CONSTRAINT preco_mensal_nao_negativo CHECK (preco_mensal > 0),
    CONSTRAINT custo_mensal_nao_negativo CHECK (custo_mensal >= 0)

);


CREATE TABLE nexus.contratos (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente BIGINT NOT NULL,
    id_servico BIGINT NOT NULL,

    FOREIGN KEY (id_cliente) REFERENCES nexus.clientes(id),
    FOREIGN KEY (id_servico) REFERENCES nexus.servico(id),

    data_inicio DATE NOT NULL,
    data_fim DATE,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT data_fim_validade CHECK (data_fim IS NULL OR data_fim >= data_inicio),
    CONSTRAINT status_valido CHECK (status IN ('ativo', 'suspenso', 'cancelado'))
);


CREATE TABLE nexus.pagamentos (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_contrato BIGINT NOT NULL,
    FOREIGN KEY (id_contrato) REFERENCES nexus.contratos(id),
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    valor NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT valor_nao_negativo CHECK (valor > 0),
    CONSTRAINT status_valido CHECK (status IN ('pago', 'pendente', 'atrasado')),
    CONSTRAINT data_pagamento_valida CHECK (
        (status = 'pago' AND data_pagamento IS NOT NULL)
        OR
        (status IN ('pendente', 'atrasado') AND data_pagamento IS NULL)
        ),
    CONSTRAINT cobranca_unica UNIQUE (id_contrato, data_vencimento)

);

CREATE TABLE nexus.servidores (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_servidor VARCHAR(80) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
    capacidade_gb INTEGER NOT NULL,
    custo_mensal NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT capacidade_nao_negativa CHECK (capacidade_gb > 0),
    CONSTRAINT custo_mensal_nao_negativo CHECK (custo_mensal >= 0),
    CONSTRAINT status_valido CHECK (status IN ('ativo', 'inativo', 'manutencao'))

);

