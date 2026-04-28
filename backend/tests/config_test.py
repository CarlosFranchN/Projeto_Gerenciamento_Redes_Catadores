from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool, NullPool
from fastapi.testclient import TestClient
import pytest

from app.database import Base, get_db
from app.main import app
from env_test_db import SQLALCHEMY_DATABASE_URL

# Configuração do Motor
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=NullPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def preparar_banco_inicial():
    """Cria as tabelas uma única vez"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def limpar_banco_total():
    """Apaga tudo se necessário"""
    Base.metadata.drop_all(bind=engine)