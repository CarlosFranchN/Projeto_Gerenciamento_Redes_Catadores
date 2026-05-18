# backend/app/main.py
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings

# Importar routers
from .routers import (
    auth,
    associacoes,
    producao,
    grupos,
    municipios,
    afiliados
)


if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        # Define a porcentagem de transações capturadas para monitoramento de performance.
        # 1.0 significa 100%. Em produção com muito tráfego, você pode reduzir isso (ex: 0.2).
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# =============== CRIAR APP ===============
app = FastAPI(
    title="Rede de Catadores API",
    description="API para gerenciamento da Rede de Catadores do Ceará",
    version="1.0.1"
)

origins = [
    "http://localhost:5173", # Para você desenvolver localmente
    "https://projeto-gerenciamento-redes-catadores.onrender.com", # Substitua pela URL final do seu React
]

# =============== CORS MIDDLEWARE (ANTES DE TUDO) ===============
# Usa "*" para desenvolvimento - substitua por URLs específicos em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD
    allow_headers=["*"],  # Authorization, Content-Type, X-Requested-With, etc.
    expose_headers=["*"],
)



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

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

