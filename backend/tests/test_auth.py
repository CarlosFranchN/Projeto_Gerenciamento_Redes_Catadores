from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from sqlalchemy.pool import StaticPool

import app.models
from app.database import Base, get_db
from app.models import Usuario
from app.dependencies import get_current_user
from app.main import app

# =====================================================================
# CONFIGURAÇÃO DO BANCO FAKE
# =====================================================================
from env_test_db import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas ANTES de rodar qualquer teste
Base.metadata.create_all(bind=engine)

# =====================================================================
# OVERRIDES (Enganando o FastAPI para os testes)
# =====================================================================
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return Usuario(id=1, username="admin_teste", role="admin")

# Aplica os overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Cria o cliente simulado
client = TestClient(app)

# =====================================================================
# AQUI COMEÇAM OS TESTES DE VERDADE
# =====================================================================
def test_criar_e_listar_usuario():
    """Testa a criação de um novo usuário para acessar o sistema"""
    
    novo_usuario = {
        "username": "gestor_teste_99", 
        "password": "senha_muito_segura_123", 
        "nome": "Carlos Gestor",
        "role": "operador",
        "ativo": True
    }
    
    response_post = client.post("/api/usuarios/", json=novo_usuario)
    
    # Se der erro, imprime o motivo para facilitar nossa vida
    if response_post.status_code != 201:
        print("❌ MOTIVO DO ERRO:", response_post.json())
            
    assert response_post.status_code == 201
    
    # Conferimos se a API escondeu a senha na resposta
    data_post = response_post.json()
    assert data_post["username"] == "gestor_teste_99"
    assert "password" not in data_post 
    assert "hashed_password" not in data_post