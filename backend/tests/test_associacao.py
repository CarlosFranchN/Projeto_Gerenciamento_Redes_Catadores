from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# 1. Imports da sua aplicação
from app.database import Base, get_db
from app.models import Usuario
from app.dependencies import get_current_user
from app.main import app

from tests.config_test import engine, TestingSessionLocal, preparar_banco_inicial

preparar_banco_inicial()

client = TestClient(app)

app.dependency_overrides[get_current_user] = lambda: Usuario(id=1, username="admin", role="admin")

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


def test_criar_e_listar_associacao():
    """Testa a criação de uma Associação"""
    nova_associacao = {
        "nome": "Associação Teste Pytest3",
        "cnpj": "11.222.333/0002-44",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "qtd_integrantes": 45,
        "ativo": True
        # Nota: Não enviamos grupo_id nem municipio_id aqui para testar a criação simples
    }
    
    response_post = client.post("/api/associacoes/", json=nova_associacao)
    
    # Print de segurança: se der erro, queremos saber a fofoca toda
    if response_post.status_code != 201:
        print("❌ ERRO NO POST:", response_post.json())
        
    assert response_post.status_code == 201
    
    response_get = client.get("/api/associacoes/")
    assert response_get.status_code == 200
    data = response_get.json()
    
    assert data["total"] >= 1
    assert data["items"][-1]["cnpj"] == "11.222.333/0002-44"