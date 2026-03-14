from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    auth,
    categoria,
    grupos,
    materiais,
    associacoes,
    estoque,
    municipios,
    parceiros,
    recebimentos,
    tipos_parceiro,
    vendas,
    relatorio,
    compradores,
    compras,
    financeiro,
    producao,
    audit)


app = FastAPI(
    title="Rede de Catadores API",
    description="API para gerenciamento da Rede de Catadores do Ceará",
    version="1.0.0"
)

origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001", # A linha crucial
    "http://127.0.0.1:8000", # A linha crucial
    "https://redecatadorescearaa.github.io",
    "null", # Para requisições de arquivos locais (file://)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(financeiro.router)       
app.include_router(categoria.router)
app.include_router(materiais.router)
app.include_router(associacoes.router)
app.include_router(estoque.router)
app.include_router(recebimentos.router) 
app.include_router(vendas.router)
app.include_router(relatorio.router)
app.include_router(compradores.router)
app.include_router(tipos_parceiro.router) 
app.include_router(parceiros.router)      
app.include_router(compras.router) 
app.include_router(producao.router)
app.include_router(audit.router)
app.include_router(grupos.router)
app.include_router(municipios.router)

@app.get("/")
def root():
    return {"message": "API Rede de Catadores - OOOOOOOOOOK", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "heaaaaaaaaaaaaaaaaaaaaaaaaaalthy"}