from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app import models

db = SessionLocal()

print("🚀 Populando Municípios Oficiais...")

municipios_data = [
    {"nome": "Metropolitano", "qtd": 8}, {"nome": "Itapipoca", "qtd": 14},
    {"nome": "Amontada", "qtd": 22}, {"nome": "Itapina", "qtd": 2},
    {"nome": "Aracoiaba", "qtd": 17}, {"nome": "Mirama", "qtd": 17},
    {"nome": "Aratuba", "qtd": 1}, {"nome": "Ocara", "qtd": 18},
    {"nome": "Barreira", "qtd": 5}, {"nome": "Pacatuba", "qtd": 30},
    {"nome": "Baturité", "qtd": 18}, {"nome": "Paracuru", "qtd": 12},
    {"nome": "Boa Viagem", "qtd": 38}, {"nome": "Quixelô", "qtd": 19},
    {"nome": "Chorozinho", "qtd": 12}, {"nome": "Redenção", "qtd": 19},
    {"nome": "Granja", "qtd": 6}, {"nome": "Tururu", "qtd": 13},
    {"nome": "Guaramiranga", "qtd": 2}, {"nome": "Ubajara", "qtd": 3},
    {"nome": "Icó", "qtd": 27}, {"nome": "Uruburetama", "qtd": 13},
    {"nome": "CARIRI (Subsede)", "qtd": 159}
]

for m in municipios_data:
    existing = db.query(models.Municipio).filter(models.Municipio.nome == m["nome"]).first()
    if not existing:
        db.add(models.Municipio(
            nome=m["nome"],
            qtd_integrantes=m["qtd"],
            uf="CE",
            ativo=True
        ))

db.commit()
print("✅ Municípios concluídos!")
db.close()