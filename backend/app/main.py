from fastapi import FastAPI
from .routers import materiais,associacoes


app = FastAPI(
    title="API Rede de Catadores"
)

# app.include_router(materiais.router)
# app.include_router(associacoes.router)
app.include_router(associacoes.router)


@app.get('/')
def init():
    return {"Message": "Inicializadooooooo"}