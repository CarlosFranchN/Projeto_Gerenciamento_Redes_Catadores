# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importar routers
from .routers import (
    auth,
    associacoes,
    producao,
    grupos,
    municipios,
    afiliados
)

# =============== CRIAR APP ===============
app = FastAPI(
    title="Rede de Catadores API",
    description="API para gerenciamento da Rede de Catadores do Ceará",
    version="1.0.1"
)

# =============== CORS MIDDLEWARE (ANTES DE TUDO) ===============
# Usa "*" para desenvolvimento - substitua por URLs específicos em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Permite QUALQUER origem (DEV ONLY)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD
    allow_headers=["*"],  # Authorization, Content-Type, X-Requested-With, etc.
    expose_headers=["*"],
)

# =============== MIDDLEWARE EXTRA PARA GARANTIR CORS ===============
# Este middleware roda DEPOIS do CORS padrão e força headers em TODAS as respostas
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Expose-Headers"] = "*"  # ← Expõe todos os headers
    
    if request.method == "OPTIONS":
        return JSONResponse(
            content={"status": "ok"},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Expose-Headers": "*",  # ← Aqui também
            }
        )
    
    return response

# =============== INCLUIR ROUTERS ===============
# (Agora que o CORS está configurado, inclua os routers)
app.include_router(auth.router)
app.include_router(associacoes.router)
app.include_router(producao.router)
app.include_router(grupos.router)
app.include_router(municipios.router)
app.include_router(afiliados.router)

# =============== ENDPOINTS GLOBAIS ===============
@app.get("/")
def root():
    return {"message": "API Rede de Catadores - OK", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# =============== HANDLER GLOBAL PARA OPTIONS ===============
# Captura QUALQUER rota OPTIONS que não foi tratada pelos routers
@app.options("/{full_path:path}")
async def global_options_handler(full_path: str):
    """Handler global para preflight CORS em qualquer rota"""
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Requested-With, Accept, Origin",
        }
    )