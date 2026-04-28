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

# =====================================================================
# AQUI COMEÇAM OS TESTES DE VERDADE
# =====================================================================

def test_listar_grupos_paginados():
    """Testa se a rota GET /api/grupos/ devolve a estrutura de paginação correta"""
    # Faz uma requisição GET para a API
    response = client.get("/api/grupos/") # Ajuste a rota se a sua não tiver o /api/
    
    # 1. Valida se a resposta foi Sucesso (200 OK)
    assert response.status_code == 200
    
    # 2. Transforma a resposta em JSON
    data = response.json()
    
    # 3. Valida se o Dicionário de Paginação que criamos está lá
    assert "total" in data
    assert "page" in data
    assert "items" in data
    assert "pages" in data
    
    # Como o banco de testes nasce vazio, a lista de items deve ser zero no começo
    assert type(data["items"]) == list

def test_criar_e_listar_grupo():
    """Testa o fluxo de criar um grupo e ver se ele aparece na lista"""
    # 1. Cria um grupo enviando um POST
    novo_grupo = {
            "nome": "Grupo Teste Pytest2",
            "cidade": "Fortaleza",
            "uf": "CE",
            "qtd_integrantes": 15,
            "ativo": True
        }
    response_post = client.post("/api/grupos/", json=novo_grupo)
    
    assert response_post.status_code == 201 # ou 201 dependendo do seu FastAPI
    data_post = response_post.json()
    assert data_post["nome"] == "Grupo Teste Pytest2"
    
    # 2. Faz um GET para garantir que o total agora é 1
    response_get = client.get("/api/grupos/")
    data_get = response_get.json()
    
    assert data_get["total"] >= 1
    assert data_get["items"][0]["qtd_integrantes"] == 15