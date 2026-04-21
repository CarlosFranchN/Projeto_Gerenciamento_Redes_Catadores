import sys
import os

# 1. MÁGICA DO IMPORT: Adiciona a pasta 'backend' no radar do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app import models

def popular_banco():
    db = SessionLocal()
    print("🔄 Iniciando a inserção de dados...")

    try:
        # Grupos (Adaptado para o novo models.py usando 'descricao')
        grupos_data = [
            {"nome": "ASCABOMJA", "descricao": "14 integrantes"},
            {"nome": "ASCAROSA", "descricao": "8 integrantes"},
            {"nome": "CATAVIP", "descricao": "33 integrantes"},
            {"nome": "JOSÉ DE ALENCAR", "descricao": "37 integrantes"},
            {"nome": "LAGOA REDONDA", "descricao": "12 integrantes"},
            {"nome": "MACHADO DE ASSIS", "descricao": "4 integrantes"},
            {"nome": "MULHERES LUTA EM CENA", "descricao": "50 integrantes"},
            {"nome": "PALMARES", "descricao": "22 integrantes"},
            {"nome": "VIVA A VIDA", "descricao": "5 integrantes"},
        ]

        for grupo_data in grupos_data:
            # Verifica se já existe para não duplicar se rodar 2 vezes
            existe = db.query(models.Grupo).filter(models.Grupo.nome == grupo_data["nome"]).first()
            if not existe:
                grupo = models.Grupo(**grupo_data)
                db.add(grupo)

        # Municípios (Adaptado para o novo models.py usando 'regiao')
        municipios_data = [
            {"nome": "Metropolitano", "uf": "CE", "regiao": "8 grupos"},
            {"nome": "Amontada", "uf": "CE", "regiao": "22 grupos"},
            {"nome": "Aracoiaba", "uf": "CE", "regiao": "17 grupos"},
            {"nome": "Aratuba", "uf": "CE", "regiao": "1 grupos"},
            {"nome": "Barreira", "uf": "CE", "regiao": "5 grupos"},
            {"nome": "Baturité", "uf": "CE", "regiao": "18 grupos"},
            {"nome": "Boa Viagem", "uf": "CE", "regiao": "38 grupos"},
            {"nome": "Chorozinho", "uf": "CE", "regiao": "12 grupos"},
            {"nome": "Granja", "uf": "CE", "regiao": "6 grupos"},
            {"nome": "Guaramiranga", "uf": "CE", "regiao": "2 grupos"},
            {"nome": "Icó", "uf": "CE", "regiao": "27 grupos"},
            {"nome": "Itapipoca", "uf": "CE", "regiao": "14 grupos"},
            {"nome": "Itapiúna", "uf": "CE", "regiao": "2 grupos"},
            {"nome": "Miraíma", "uf": "CE", "regiao": "17 grupos"},
            {"nome": "Ocara", "uf": "CE", "regiao": "18 grupos"},
            {"nome": "Pacatuba", "uf": "CE", "regiao": "30 grupos"},
            {"nome": "Paracuru", "uf": "CE", "regiao": "12 grupos"},
            {"nome": "Quixelô", "uf": "CE", "regiao": "19 grupos"},
            {"nome": "Redenção", "uf": "CE", "regiao": "19 grupos"},
            {"nome": "Tururu", "uf": "CE", "regiao": "13 grupos"},
            {"nome": "Ubajara", "uf": "CE", "regiao": "3 grupos"},
        ]

        for municipio_data in municipios_data:
            existe = db.query(models.Municipio).filter(models.Municipio.nome == municipio_data["nome"]).first()
            if not existe:
                municipio = models.Municipio(**municipio_data)
                db.add(municipio)

        # Salva tudo no banco de uma vez
        db.commit()
        print("✅ Grupos e municípios populados com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao popular banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()