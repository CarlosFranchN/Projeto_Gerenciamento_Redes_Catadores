from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import materiais,associacoes,compradores,entrada_material,vendas


app = FastAPI(
    title="API Rede de Catadores"
)

origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001", # A linha crucial
    "null", # Para requisições de arquivos locais (file://)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(materiais.router)
app.include_router(associacoes.router)
app.include_router(compradores.router)
app.include_router(entrada_material.router)
app.include_router(vendas.router)


@app.get('/')
def init():
    return {"Message": "Inicializadooooooo"}