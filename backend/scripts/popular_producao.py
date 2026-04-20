from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from decimal import Decimal

db = SessionLocal()

print("🚀 Iniciando popularização de produção...")

# =============== 1. Buscar Associação "Rede de Catadores" ===============
rede = db.query(models.Associacao).filter(
    models.Associacao.cnpj == "09.000.185/0001-09"
).first()

if not rede:
    print("❌ Associação 'Rede de Catadores' não encontrada!")
    print("Execute primeiro: python popular_associacoes.py")
    db.close()
    exit()

print(f"✅ Associação encontrada: {rede.parceiro_info.nome if rede.parceiro_info else 'Rede de Catadores'}")
print(f"   ID: {rede.id}")

# =============== 2. Dados de Produção ===============
producao_data = [
    {"mes": 1,  "kg": Decimal("37655.0")},
    {"mes": 2,  "kg": Decimal("32626.5")},
    {"mes": 3,  "kg": Decimal("26805.9")},
    {"mes": 4,  "kg": Decimal("35855.0")},
    {"mes": 5,  "kg": Decimal("38118.0")},
    {"mes": 6,  "kg": Decimal("36184.5")},
    {"mes": 7,  "kg": Decimal("49744.0")},
    {"mes": 8,  "kg": Decimal("39233.5")},
    {"mes": 9,  "kg": Decimal("36517.0")},
    {"mes": 10, "kg": Decimal("41127.5")},
    {"mes": 11, "kg": Decimal("30212.5")},
    {"mes": 12, "kg": Decimal("32913.3")},
]

# =============== 3. Deletar Produção Existente (para evitar duplicatas) ===============
deletados = db.query(models.ProducaoMensal).filter(
    models.ProducaoMensal.associacao_id == rede.id
).delete()

if deletados > 0:
    print(f"🗑️  {deletados} registros de produção existentes deletados")

# =============== 4. Criar Nova Produção ===============
ano = 2024
total_kg = Decimal("0")

for prod in producao_data:
    producao = models.ProducaoMensal(
        associacao_id=rede.id,
        mes=prod["mes"],
        ano=ano,
        kg=prod["kg"],
        valor_venda=None,
        observado=None
    )
    db.add(producao)
    total_kg += prod["kg"]

db.commit()

# =============== 5. Resumo ===============
print("\n" + "="*60)
print("🎉 Popularização concluída!")
print(f"   📊 Associação: Rede de Catadores (ID: {rede.id})")
print(f"   📅 Ano: {ano}")
print(f"   📦 Meses: {len(producao_data)}")
print(f"   ⚖️  Total: {total_kg:,.1f} kg")
print("="*60)

# =============== 6. Verificar ===============
total_no_banco = db.query(
    models.ProducaoMensal.kg
).filter(
    models.ProducaoMensal.associacao_id == rede.id,
    models.ProducaoMensal.ano == ano
).all()

soma = sum([float(p[0]) for p in total_no_banco])
print(f"\n✅ Verificação: {len(total_no_banco)} registros no banco")
print(f"   Soma: {soma:,.1f} kg")

db.close()