from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResponse, status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    service = PedidoService(db)
    return service.criar_pedido(dados)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    service = PedidoService(db)
    pedido = service.buscar_pedido(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    service = PedidoService(db)
    return service.listar_pedidos()


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(
    pedido_id: int, dados: PedidoStatusUpdate, db: Session = Depends(get_db)
):
    service = PedidoService(db)
    pedido = service.alterar_status(pedido_id, dados.status)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido