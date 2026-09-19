from sqlalchemy.orm import Session
from app.models.pedido import Pedido


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def listar(self) -> list[Pedido]:
        return self.db.query(Pedido).all()

    def atualizar(self, pedido: Pedido) -> Pedido:
        self.db.commit()
        self.db.refresh(pedido)
        return pedido