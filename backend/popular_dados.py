from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.core.security import get_password_hash
from datetime import datetime

db = SessionLocal()

# 1. Criar admin se não existir
admin = db.query(models.Usuario).filter(
    models.Usuario.username == "admin"
).first()

if not admin:
    admin = models.Usuario(
        username="admin",
        hashed_password=get_password_hash("senha123"),
        nome="Administrador",
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("✅ Admin criado!")

# 2. Criar tipo de parceiro ASSOCIACAO
tipo = db.query(models.TipoParceiro).filter(
    models.TipoParceiro.nome == "ASSOCIACAO"
).first()

if not tipo:
    tipo = models.TipoParceiro(nome="ASSOCIACAO")
    db.add(tipo)
    db.commit()

# 3. Criar associações de exemplo
associacoes_data = [
    {"nome": "Rede de Catadores", "cnpj": "09.000.185/0001-09", "bairro": "João XXIII", "lider": "Leina Mara"},
    {"nome": "ACORES", "cnpj": "04.989.221/0001-95", "bairro": "Serrinha", "lider": "—"},
    {"nome": "ARAN", "cnpj": "07.475.187/0001-29", "bairro": "Bonsucesso", "lider": "—"},
]

for assoc_data in associacoes_data:
    # Cria parceiro
    parceiro = models.Parceiro(
        nome=assoc_data["nome"],
        id_tipo_parceiro=tipo.id
    )
    db.add(parceiro)
    db.flush()
    
    # Cria associação
    associacao = models.Associacao(
        parceiro_id=parceiro.id,
        cnpj=assoc_data["cnpj"],
        bairro=assoc_data["bairro"],
        lider=assoc_data["lider"],
        status="ativo",
        ativo=True
    )
    db.add(associacao)

db.commit()

# 4. Criar produção de exemplo
from decimal import Decimal

producao_data = [
    {"mes": 1, "kg": Decimal("37655.0")},
    {"mes": 2, "kg": Decimal("32626.5")},
    {"mes": 3, "kg": Decimal("26805.9")},
    {"mes": 4, "kg": Decimal("35855.0")},
    {"mes": 5, "kg": Decimal("38118.0")},
    {"mes": 6, "kg": Decimal("36184.5")},
    {"mes": 7, "kg": Decimal("49744.0")},
    {"mes": 8, "kg": Decimal("39233.5")},
    {"mes": 9, "kg": Decimal("36517.0")},
    {"mes": 10, "kg": Decimal("41127.5")},
    {"mes": 11, "kg": Decimal("30212.5")},
    {"mes": 12, "kg": Decimal("32913.3")},
]

# Pega primeira associação
assoc = db.query(models.Associacao).first()
if assoc:
    for prod in producao_data:
        producao = models.ProducaoMensal(
            associacao_id=assoc.id,
            mes=prod["mes"],
            ano=2024,
            kg=prod["kg"]
        )
        db.add(producao)
    
    db.commit()
    print("✅ Produção criada!")

db.close()
print("🎉 Dados iniciais populados com sucesso!")