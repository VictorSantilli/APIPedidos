# API de Pedidos

Projeto da disciplina de Desenvolvimento de Sistemas Distribuídos — Trabalho 1.

API REST simples para gerenciamento de pedidos, construída em camadas (API / Service / Repository), com persistência em PostgreSQL. Aplicação e banco executam como containers separados, orquestrados via Docker Compose.

> **Nota:** O desenvolvimento da base de código deste projeto, a configuração da infraestrutura Docker e a redação desta documentação contaram com o auxílio e revisão de ferramentas de Inteligência Artificial (IA).

## Arquitetura

```
Cliente → API de Pedidos (FastAPI) → PostgreSQL
```

- **Camada de API (Controller)**: recebe requisições HTTP e produz respostas.
- **Camada de Service**: concentra as regras de negócio (cálculo de `valor_total`, definição do `status` inicial, validações de existência).
- **Camada de Repository**: abstrai o acesso ao banco de dados (persistência).

As três camadas rodam no mesmo container (`pedidos`). O PostgreSQL roda em um container separado (`postgres`), comunicando-se com a aplicação pela rede interna do Docker Compose.

## Estrutura do projeto

```
APIPedidos/
├── app/
│   ├── main.py                      # inicialização do FastAPI
│   ├── database.py                  # configuração da conexão com o banco
│   ├── models/pedido.py             # modelo persistente (SQLAlchemy)
│   ├── schemas/pedido.py            # entrada e saída da API (Pydantic)
│   ├── repositories/pedido_repository.py  # persistência
│   ├── services/pedido_service.py   # regras de negócio
│   └── api/pedidos.py               # endpoints
├── tests/                           # testes automatizados da aplicação
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Modelo de Pedido

| Campo            | Descrição                                                    |
| ---------------- | ------------------------------------------------------------ |
| `id`             | Identificador do pedido                                      |
| `cliente`        | Identificação textual do cliente                             |
| `produto`        | Identificação textual do produto                             |
| `quantidade`     | Quantidade solicitada                                        |
| `valor_unitario` | Preço de uma unidade                                         |
| `valor_total`    | Calculado pela aplicação (`quantidade × valor_unitario`)     |
| `status`         | Estado atual do pedido (`CRIADO`, `CONFIRMADO`, `CANCELADO`) |
| `data_criacao`   | Instante em que o pedido foi registrado                      |

## Como executar

Pré-requisito: Docker Desktop instalado e em execução.

```bash
docker compose up --build
```

Isso sobe dois containers:

- `pedidos`: aplicação FastAPI, disponível em `http://localhost:8000`
- `postgres`: banco de dados PostgreSQL

Para derrubar os containers mantendo os dados salvos:

```bash
docker compose down
```

Para derrubar os containers **e apagar os dados** (remove o volume):

```bash
docker compose down -v
```

## Testes automatizados

O projeto possui uma camada de testes automatizados construída com `pytest` e `httpx` para validar a saúde da API e as regras de negócio dos pedidos.

### Executar testes via Docker (recomendado)

Como a arquitetura utiliza o Docker para isolar a aplicação e o banco PostgreSQL, a forma ideal de executar os testes é dentro do próprio container da aplicação.

1. Certifique-se de que os containers estão em execução:

   ```bash
   docker compose up -d
   ```

2. Execute a bateria de testes através do container `pedidos`:

   ```bash
   docker compose exec pedidos pytest
   ```

### Executar testes localmente

Caso prefira executar o projeto fora do ambiente Docker, certifique-se de que instalou todas as dependências locais (`pip install -r requirements.txt`) e execute o interpretador com o módulo `pytest`:

```bash
python -m pytest
```

## Documentação interativa

Com a aplicação em execução, acesse:

```
http://localhost:8000/docs
```

## Endpoints

| Método  | Rota                   | Descrição                                |
| ------- | ---------------------- | ---------------------------------------- |
| `POST`  | `/pedidos`             | Cria um novo pedido                      |
| `GET`   | `/pedidos`             | Lista todos os pedidos                   |
| `GET`   | `/pedidos/{id}`        | Consulta um pedido específico            |
| `PATCH` | `/pedidos/{id}/status` | Altera o status de um pedido             |
| `GET`   | `/health`              | Verifica se a aplicação está operacional |

### Exemplo — Criar pedido

**Requisição:**

```http
POST /pedidos
Content-Type: application/json

{
  "cliente": "Joao",
  "produto": "Teclado",
  "quantidade": 2,
  "valor_unitario": 150.0
}
```

**Resposta (201 Created):**

```json
{
  "id": 1,
  "cliente": "Joao",
  "produto": "Teclado",
  "quantidade": 2,
  "valor_unitario": 150.0,
  "valor_total": 300.0,
  "status": "CRIADO",
  "data_criacao": "2026-08-30T00:00:00"
}
```

## Persistência

Os dados do PostgreSQL são armazenados em um volume Docker nomeado (`pedidos_data`), independente do ciclo de vida dos containers. Isso garante que:

- Reiniciar o container da aplicação (`docker compose restart pedidos`) **não apaga** os pedidos.
- Reiniciar o container do banco (`docker compose restart postgres`) **também não apaga** os pedidos.
- Os dados só são removidos se o volume for explicitamente apagado (`docker compose down -v`).

## Configuração

A URL de conexão com o banco não fica fixa no código — é definida pela variável de ambiente `DATABASE_URL`, configurada no `docker-compose.yml`:

```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/pedidos
```

Repare que o host usado é `postgres` (nome do serviço no Docker Compose), não `localhost`, pois os containers se comunicam pela rede interna do Compose usando o nome do serviço como endereço.

## Tecnologias utilizadas

- **FastAPI** — framework web
- **Uvicorn** — servidor ASGI
- **SQLAlchemy** — ORM
- **psycopg2** — driver PostgreSQL
- **Pydantic** — validação de dados
- **pytest / httpx** — testes automatizados
- **PostgreSQL 16** — banco de dados
- **Docker / Docker Compose** — containerização e orquestração
