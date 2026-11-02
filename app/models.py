from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Conta(Base):
    __tablename__ = "contas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titular: Mapped[str] = mapped_column(String(100))
    saldo: Mapped[float] = mapped_column(default=0.0)
    transacoes: Mapped[list["Transacao"]] = relationship(back_populates="conta")


class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    conta_id: Mapped[int] = mapped_column(ForeignKey("contas.id"))
    tipo: Mapped[str] = mapped_column(String(10))
    valor: Mapped[float]
    data: Mapped[datetime] = mapped_column(default=datetime.now)
    conta: Mapped["Conta"] = relationship(back_populates="transacoes")