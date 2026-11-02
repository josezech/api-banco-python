from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContaCreate(BaseModel):
    titular: str = Field(min_length=1, max_length=100)


class Operacao(BaseModel):
    valor: float = Field(gt=0)


class ContaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titular: str
    saldo: float


class TransacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo: str
    valor: float
    data: datetime