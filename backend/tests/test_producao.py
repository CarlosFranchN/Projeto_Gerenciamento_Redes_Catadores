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

def test_criar_e_listar_producao():
    """Testa a criação de uma produção vinculada a uma associação"""
    
    # 1. Primeiro, criamos uma Associação para ser a "dona" dessa produção
    nova_assoc = {
        "nome": "Associação Recicla Teste 2",
        "cnpj": "55.444.333/0001-22",
        "bairro": "Messejana",
        "cidade": "Fortaleza",
        "uf": "CE",
        "qtd_integrantes": 20,
        "ativo": True
    }
    res_assoc = client.post("/api/associacoes/", json=nova_assoc)
    assert res_assoc.status_code == 201
    
    # Pegamos o ID que o banco acabou de gerar para essa associação
    assoc_id = res_assoc.json()["id"]
    
    # 2. Agora sim, criamos a Produção usando esse ID
    nova_producao = {
        "mes": 4, # Abril
        "ano": 2026,
        "categoria": "PET",
        "peso_kg": 2500.50,
        "valor_gerado": 5000.00,
        "tipo_registro": "PRODUCAO",
        "associacao_id": assoc_id
    }
    
    res_prod = client.post("/api/producao/", json=nova_producao)
    assert res_prod.status_code == 201
    
    # 3. Fazemos o GET filtrando pelo ano
    res_get = client.get("/api/producao/?ano=2026")
    assert res_get.status_code == 200

    data = res_get.json()
    
    # Confere se a lista tem pelo menos 1 item
    assert len(data) >= 1
    
    # Como data já é a lista, iteramos diretamente sobre ela
    categorias_cadastradas = [item["categoria"] for item in data]
    assert "PET" in categorias_cadastradas