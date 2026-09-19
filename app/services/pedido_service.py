from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, StatusPedido
from app.repositories.pedido_repository import PedidoRepository


class PedidoService:
    def __init__(self, db: Session):
        self.repository = PedidoRepository(db)

    def criar_pedido(self, dados: PedidoCreate) -> Pedido:
        valor_total = dados.quantidade * dados.valor_unitario

        novo_pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=valor_total,
            status=StatusPedido.CRIADO.value,
        )

        return self.repository.criar(novo_pedido)

    def buscar_pedido(self, pedido_id: int) -> Pedido | None:
        return self.repository.buscar_por_id(pedido_id)

    def listar_pedidos(self) -> list[Pedido]:
        return self.repository.listar()

    def alterar_status(self, pedido_id: int, novo_status: StatusPedido) -> Pedido | None:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            return None
        pedido.status = novo_status.value
        return self.repository.atualizar(pedido)