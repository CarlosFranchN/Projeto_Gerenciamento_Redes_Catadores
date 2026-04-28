from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Importe o app principal, o Base do banco e a função que injeta o banco nas rotas
from app.main import app
from app.database import Base
from app.database import get_db # Ajuste se o seu get_db estiver em outro arquivo (ex: app/dependencies.py)
from app.models import Usuario
from app.dependencies import get_current_user

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
    
def test_criar_e_listar_municipio():
    """Testa a criação e listagem de um Município"""
    novo_municipio = {
        "nome": "Caucaia Teste 3",
        "uf": "CE",
        "qtd_integrantes": 120,
        "ativo": True
    }
    
    # Testa o POST (Criar)
    response_post = client.post("/api/municipios/", json=novo_municipio)
    assert response_post.status_code == 201
    
    # Testa o GET (Listar e verificar Paginação)
    response_get = client.get("/api/municipios/")
    assert response_get.status_code == 200
    data = response_get.json()
    
    # Verifica se a paginação veio certa e se Caucaia está lá
    assert data["total"] >= 1
    nomes_cadastrados = [item["nome"] for item in data["items"]]
    assert "Caucaia Teste 3" in nomes_cadastrados