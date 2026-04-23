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
# 1. Configurar um Banco de Dados "Fake" (SQLite na memória)
# Ele nasce vazio, fazemos os testes e quando o teste acaba, ele some!
from env_test_db import SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de teste
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    return Usuario(id=1, username="admin_teste", role="admin")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# 3. Criar o "Cliente" que vai simular o navegador/React
client = TestClient(app)

# =====================================================================
# AQUI COMEÇAM OS TESTES DE VERDADE
# =====================================================================

def test_criar_e_listar_associacao():
    """Testa a criação de uma Associação"""
    nova_associacao = {
        "nome": "Associação Teste Pytest",
        "cnpj": "11.222.333/0001-44",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "qtd_integrantes": 45,
        "ativo": True
        # Nota: Não enviamos grupo_id nem municipio_id aqui para testar a criação simples
    }
    
    response_post = client.post("/api/associacoes/", json=nova_associacao)
    assert response_post.status_code == 201
    
    response_get = client.get("/api/associacoes/")
    assert response_get.status_code == 200
    data = response_get.json()
    
    assert data["total"] >= 1
    assert data["items"][-1]["cnpj"] == "11.222.333/0001-44"