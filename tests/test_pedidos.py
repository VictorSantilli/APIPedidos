from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

pedido_id_teste = None

def test_criar_pedido():
    global pedido_id_teste
    payload = {
        "cliente": "Cliente Teste",
        "produto": "Monitor 4K",
        "quantidade": 2,
        "valor_unitario": 1500.00
    }
    
    response = client.post("/pedidos", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["cliente"] == payload["cliente"]
    assert data["valor_total"] == 3000.00
    assert data["status"] == "CRIADO"
    
    # Guarda o ID gerado para usar nos testes de GET e PATCH
    pedido_id_teste = data["id"]

def test_consultar_pedido():
    response = client.get(f"/pedidos/{pedido_id_teste}")
    assert response.status_code == 200
    assert response.json()["id"] == pedido_id_teste

def test_consultar_pedido_inexistente():
    response = client.get("/pedidos/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pedido não encontrado"}

def test_listar_pedidos():
    response = client.get("/pedidos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_alterar_status():
    # O novo status é enviado no corpo da requisição (JSON)
    response = client.patch(
        f"/pedidos/{pedido_id_teste}/status",
        json={"status": "CONFIRMADO"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CONFIRMADO"

def test_alterar_status_persistido():
    # Confirma que a alteração foi gravada no banco
    response = client.get(f"/pedidos/{pedido_id_teste}")
    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMADO"

def test_alterar_status_invalido():
    response = client.patch(
        f"/pedidos/{pedido_id_teste}/status",
        json={"status": "BANANA"},
    )
    assert response.status_code == 422

def test_alterar_status_pedido_inexistente():
    response = client.patch(
        "/pedidos/999999/status",
        json={"status": "CANCELADO"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Pedido não encontrado"}