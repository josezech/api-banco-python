import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Banco em memória, isolado do banco.db real
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False)


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def criar_conta(client, titular="José"):
    return client.post("/contas", json={"titular": titular}).json()


def test_criar_conta(client):
    resposta = client.post("/contas", json={"titular": "José"})
    assert resposta.status_code == 201
    assert resposta.json()["saldo"] == 0


def test_deposito_aumenta_saldo(client):
    conta = criar_conta(client)
    resposta = client.post(f"/contas/{conta['id']}/depositos", json={"valor": 100})
    assert resposta.status_code == 200
    assert resposta.json()["saldo"] == 100


def test_saque_diminui_saldo(client):
    conta = criar_conta(client)
    client.post(f"/contas/{conta['id']}/depositos", json={"valor": 100})
    resposta = client.post(f"/contas/{conta['id']}/saques", json={"valor": 40})
    assert resposta.json()["saldo"] == 60


def test_saque_com_saldo_insuficiente(client):
    conta = criar_conta(client)
    resposta = client.post(f"/contas/{conta['id']}/saques", json={"valor": 10})
    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Saldo insuficiente"


def test_valor_negativo_e_rejeitado(client):
    conta = criar_conta(client)
    resposta = client.post(f"/contas/{conta['id']}/depositos", json={"valor": -5})
    assert resposta.status_code == 422


def test_conta_inexistente(client):
    resposta = client.get("/contas/999/extrato")
    assert resposta.status_code == 404


def test_extrato_lista_transacoes(client):
    conta = criar_conta(client)
    client.post(f"/contas/{conta['id']}/depositos", json={"valor": 100})
    client.post(f"/contas/{conta['id']}/saques", json={"valor": 30})
    extrato = client.get(f"/contas/{conta['id']}/extrato").json()
    assert [t["tipo"] for t in extrato] == ["deposito", "saque"]