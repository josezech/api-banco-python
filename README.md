# API Banco

API REST de conta bancária desenvolvida em Python com FastAPI. Permite criar contas, realizar depósitos e saques e consultar o extrato, com validação das regras de negócio e testes automatizados.

Projeto criado como evolução dos estudos da [Trilha Python da DIO](https://github.com/digitalinnovationone/trilha-python-dio).

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![Testes](https://img.shields.io/badge/testes-pytest-brightgreen)

## Documentação interativa

![Swagger da API](docs/swagger.png)

## Funcionalidades

- Criação de contas bancárias
- Depósito com atualização de saldo
- Saque com bloqueio por saldo insuficiente
- Extrato com histórico de transações
- Validação de dados de entrada (valores devem ser positivos)
- Respostas de erro padronizadas (404, 400 e 422)

## Tecnologias

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/): framework da API
- [SQLAlchemy](https://www.sqlalchemy.org/): ORM e modelagem do banco
- [SQLite](https://www.sqlite.org/): banco de dados
- [Pydantic](https://docs.pydantic.dev/): validação dos dados
- [Pytest](https://docs.pytest.org/): testes automatizados

## Endpoints

| Método | Rota                          | Descrição                  |
|--------|-------------------------------|----------------------------|
| POST   | `/contas`                     | Cria uma nova conta        |
| POST   | `/contas/{conta_id}/depositos`| Realiza um depósito        |
| POST   | `/contas/{conta_id}/saques`   | Realiza um saque           |
| GET    | `/contas/{conta_id}/extrato`  | Lista as transações        |

### Exemplo de uso

Criar conta:

```json
POST /contas
{ "titular": "José" }
```

Resposta:

```json
{ "id": 1, "titular": "José", "saldo": 0.0 }
```

Depositar:

```json
POST /contas/1/depositos
{ "valor": 100 }
```

Sacar mais do que o saldo retorna erro `400`:

```json
{ "detail": "Saldo insuficiente" }
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

```bash
# 1. Clone o repositório
git clone https://github.com/josezech/api-banco-python.git
cd api-banco-python

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source .venv/bin/activate     # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a API
uvicorn app.main:app --reload
```

Acesse a documentação em http://127.0.0.1:8000/docs.

## Testes

```bash
python -m pytest -v
```

Os testes usam um banco SQLite em memória, sem afetar os dados reais.

## Estrutura do projeto

```
api-banco-python/
├── app/
│   ├── database.py    # conexão e sessão do banco
│   ├── models.py      # tabelas (Conta e Transacao)
│   ├── schemas.py     # validação de entrada e saída
│   └── main.py        # rotas da API
├── tests/
│   └── test_contas.py
├── docs/
│   └── swagger.png
├── requirements.txt
└── README.md
```

## Decisões de projeto

- **FastAPI** pela validação automática e pela documentação gerada a partir do código.
- **SQLite** para simplificar a execução local, sem instalar servidor de banco.
- **Separação em camadas** (modelos, schemas e rotas) para facilitar manutenção e testes.
- **Registro de transações** em tabela própria, o que permite gerar o extrato e auditar o saldo.

## Próximos passos

- [ ] Autenticação com JWT
- [ ] Migração para PostgreSQL
- [ ] Containerização com Docker
- [ ] Deploy online

## Autor

**José** · [GitHub](https://github.com/josezech) [Linkedin](https://www.linkedin.com/in/jos%C3%A9-zechinelli-j%C3%BAnior/)
