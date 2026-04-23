from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app import models

db = SessionLocal()

print("🚀 Populando Grupos Oficiais...")

grupos_data = [
    {"nome": "ASCABOMJA", "qtd": 14},
    {"nome": "ASCAROSA", "qtd": 8},
    {"nome": "CATAVIP", "qtd": 33},
    {"nome": "JOSE DE ALENCAR", "qtd": 37},
    {"nome": "LAGOA REDONDA", "qtd": 12},
    {"nome": "MACHADO DE ASSIS", "qtd": 4},
    {"nome": "MULHERES LUTA EM CENA", "qtd": 50},
    {"nome": "PALMARES", "qtd": 22}
]

for g in grupos_data:
    existing = db.query(models.Grupo).filter(models.Grupo.nome == g["nome"]).first()
    if not existing:
        db.add(models.Grupo(
            nome=g["nome"],
            qtd_integrantes=g["qtd"],
            ativo=True
        ))

db.commit()
print("✅ Grupos concluídos!")
db.close()