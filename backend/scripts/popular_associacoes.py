from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app import models

db = SessionLocal()

print("🚀 Populando Associações Oficiais...")

associacoes_data = [
    {"nome": "REDE DE CATADORES", "cnpj": "09.000.185/0001-09", "bairro": "JOÃO XXIII", "qtd": 0}, # Coordenadoria
    {"nome": "ACORES", "cnpj": "04.989.221/0001-95", "bairro": "SERRINHA", "qtd": 20},
    {"nome": "ARAN", "cnpj": "07.475.187/0001-29", "bairro": "BOM SUCESSO", "qtd": 30},
    {"nome": "ASCAJAN", "cnpj": "08.612.882/0001-58", "bairro": "JANGURUSSU", "qtd": 40},
    {"nome": "MOURA BRASIL", "cnpj": "24.293.438/0001-73", "bairro": "MOURA BRASIL", "qtd": 23},
    {"nome": "MARAVILHA", "cnpj": "11.058.865/0001-25", "bairro": "VILA UNIÃO", "qtd": 7},
    {"nome": "RAIO DE SOL", "cnpj": "23.668.402/0001-64", "bairro": "GENIBAÚ", "qtd": 22},
    {"nome": "ROSA VIRGINIA", "cnpj": "09.635.604/0001-89", "bairro": "SANTA TEREZINHA", "qtd": 25},
    {"nome": "SOCRELP", "cnpj": "00.118.784/0001-57", "bairro": "PIRAMBU", "qtd": 10},
    {"nome": "VIVA A VIDA", "cnpj": "07.865.301/0001-27", "bairro": "FARIAS BRITO", "qtd": 5}
]

for data in associacoes_data:
    existing = db.query(models.Associacao).filter(models.Associacao.nome == data["nome"]).first()
    if not existing:
        db.add(models.Associacao(
            nome=data["nome"],
            cnpj=data["cnpj"],
            bairro=data["bairro"],
            cidade="Fortaleza",
            uf="CE",
            qtd_integrantes=data["qtd"],
            ativo=True
        ))

db.commit()
print("✅ Associações concluídas!")
db.close()