from fastapi import FastAPI
from .routers import materiais,associacoes,compradores,entrada_material,vendas


app = FastAPI(
    title="API Rede de Catadores"
)

app.include_router(materiais.router)
app.include_router(associacoes.router)
app.include_router(compradores.router)
app.include_router(entrada_material.router)
app.include_router(vendas.router)


@app.get('/')
def init():
    return {"Message": "Inicializadooooooo"}