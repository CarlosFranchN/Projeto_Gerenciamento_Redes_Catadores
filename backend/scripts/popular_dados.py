from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

db = SessionLocal()

# Grupos
grupos_data = [
    {"nome": "ASCABOMJA", "integrantes": 14},
    {"nome": "ASCAROSA", "integrantes": 8},
    {"nome": "CATAVIP", "integrantes": 33},
    {"nome": "JOSÉ DE ALENCAR", "integrantes": 37},
    {"nome": "LAGOA REDONDA", "integrantes": 12},
    {"nome": "MACHADO DE ASSIS", "integrantes": 4},
    {"nome": "MULHERES LUTA EM CENA", "integrantes": 50},
    {"nome": "PALMARES", "integrantes": 22},
    {"nome": "VIVA A VIDA", "integrantes": 5},
]

for grupo_data in grupos_data:
    grupo = models.Grupo(**grupo_data)
    db.add(grupo)

# Municípios
municipios_data = [
    {"nome": "Metropolitano", "uf": "CE", "qtd_grupos": 8},
    {"nome": "Amontada", "uf": "CE", "qtd_grupos": 22},
    {"nome": "Aracoiaba", "uf": "CE", "qtd_grupos": 17},
    {"nome": "Aratuba", "uf": "CE", "qtd_grupos": 1},
    {"nome": "Barreira", "uf": "CE", "qtd_grupos": 5},
    {"nome": "Baturité", "uf": "CE", "qtd_grupos": 18},
    {"nome": "Boa Viagem", "uf": "CE", "qtd_grupos": 38},
    {"nome": "Chorozinho", "uf": "CE", "qtd_grupos": 12},
    {"nome": "Granja", "uf": "CE", "qtd_grupos": 6},
    {"nome": "Guaramiranga", "uf": "CE", "qtd_grupos": 2},
    {"nome": "Icó", "uf": "CE", "qtd_grupos": 27},
    {"nome": "Itapipoca", "uf": "CE", "qtd_grupos": 14},
    {"nome": "Itapiúna", "uf": "CE", "qtd_grupos": 2},
    {"nome": "Miraíma", "uf": "CE", "qtd_grupos": 17},
    {"nome": "Ocara", "uf": "CE", "qtd_grupos": 18},
    {"nome": "Pacatuba", "uf": "CE", "qtd_grupos": 30},
    {"nome": "Paracuru", "uf": "CE", "qtd_grupos": 12},
    {"nome": "Quixelô", "uf": "CE", "qtd_grupos": 19},
    {"nome": "Redenção", "uf": "CE", "qtd_grupos": 19},
    {"nome": "Tururu", "uf": "CE", "qtd_grupos": 13},
    {"nome": "Ubajara", "uf": "CE", "qtd_grupos": 3},
]

for municipio_data in municipios_data:
    municipio = models.Municipio(**municipio_data)
    db.add(municipio)

db.commit()
db.close()

print("✅ Grupos e municípios populados com sucesso!")