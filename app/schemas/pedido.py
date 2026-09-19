from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


class PedidoCreate(BaseModel):
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float


class PedidoStatusUpdate(BaseModel):
    status: StatusPedido


class PedidoResponse(BaseModel):
    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    status: str
    data_criacao: datetime

    class Config:
        from_attributes = True