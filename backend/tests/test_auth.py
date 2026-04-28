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

from tests.config_test import engine, TestingSessionLocal, preparar_banco_inicial

preparar_banco_inicial()

client = TestClient(app)

app.dependency_overrides[get_current_user] = lambda: Usuario(id=1, username="admin_teste", role="admin")


@pytest.fixture(autouse=True)
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Injeta a sessão da transação no FastAPI
    app.dependency_overrides[get_db] = lambda: session

    yield session 

    session.close()
    transaction.rollback()
    connection.close()
    
def test_criar_e_listar_usuario():
    """Testa a criação de um novo usuário para acessar o sistema"""
    
    novo_usuario = {
        "username": "gestor_teste_999", 
        "password": "senha_muito_segura_1234", 
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
    assert data_post["username"] == "gestor_teste_999"
    assert "password" not in data_post 
    assert "hashed_password" not in data_post