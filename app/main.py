from fastapi import FastAPI
from app.database import Base, engine
from app.api import pedidos

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Pedidos")

app.include_router(pedidos.router)


@app.get("/health")
def health():
    return {"status": "ok"}