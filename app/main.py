from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Banco", description="API simples de conta bancária")


def buscar_conta(db: Session, conta_id: int) -> models.Conta:
    conta = db.get(models.Conta, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta


@app.post("/contas", response_model=schemas.ContaOut, status_code=201)
def criar_conta(dados: schemas.ContaCreate, db: Session = Depends(get_db)):
    conta = models.Conta(titular=dados.titular)
    db.add(conta)
    db.commit()
    db.refresh(conta)
    return conta


@app.post("/contas/{conta_id}/depositos", response_model=schemas.ContaOut)
def depositar(conta_id: int, op: schemas.Operacao, db: Session = Depends(get_db)):
    conta = buscar_conta(db, conta_id)
    conta.saldo += op.valor
    db.add(models.Transacao(conta_id=conta.id, tipo="deposito", valor=op.valor))
    db.commit()
    db.refresh(conta)
    return conta


@app.post("/contas/{conta_id}/saques", response_model=schemas.ContaOut)
def sacar(conta_id: int, op: schemas.Operacao, db: Session = Depends(get_db)):
    conta = buscar_conta(db, conta_id)
    if op.valor > conta.saldo:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    conta.saldo -= op.valor
    db.add(models.Transacao(conta_id=conta.id, tipo="saque", valor=op.valor))
    db.commit()
    db.refresh(conta)
    return conta


@app.get("/contas/{conta_id}/extrato", response_model=list[schemas.TransacaoOut])
def extrato(conta_id: int, db: Session = Depends(get_db)):
    return buscar_conta(db, conta_id).transacoes