from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

db = SessionLocal()

print("🚀 Iniciando popularização de associações...")
print("="*70)

# =============== 1. Criar Tipo de Parceiro ===============
tipo_assoc = db.query(models.TipoParceiro).filter(
    models.TipoParceiro.nome == "ASSOCIACAO"
).first()

if not tipo_assoc:
    tipo_assoc = models.TipoParceiro(nome="ASSOCIACAO")
    db.add(tipo_assoc)
    db.commit()
    print("✅ Tipo de parceiro 'ASSOCIACAO' criado")
else:
    print("✅ Tipo de parceiro 'ASSOCIACAO' já existe")

# =============== 2. Dados Completos das Associações ===============
associacoes_data = [
    {
        "nome": "REDE DE CATADORES",
        "cnpj": "09.000.185/0001-09",
        "lider": "LEINA MARA",
        "telefone": "(85) 99119-2037",
        "bairro": "JOÃO XXIII",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "ACORES (Associação Ecológica dos Coletores de Materiais Recicláveis da Serrinha e Adjacências)",
        "cnpj": "04.989.221/0001-95",
        "lider": "LIDIANA SOUSA",
        "telefone": "(85) 99436-4061",
        "bairro": "SERRINHA",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "ARAN (Associação de Recicladores Amigos da Natureza)",
        "cnpj": "07.475.187/0001-29",
        "lider": "MARIA DA CONCEIÇÃO",
        "telefone": "(85) 98575-2728",
        "bairro": "BOM SUCESSO",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "ASCAJAN (Associação dos Catadores do Jangurussu)",
        "cnpj": "08.612.882/0001-58",
        "lider": "SEBASTIANA DO CARMO",
        "telefone": "(85) 98520-7116",
        "bairro": "JANGURUSSU",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "MOURA BRASIL",
        "cnpj": "24.293.438/0001-73",
        "lider": "FRANCISCA RAQUEL",
        "telefone": "(85) 99838-2731",
        "bairro": "MOURA BRASIL",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "MARAVILHA",
        "cnpj": "11.058.865/0001-25",
        "lider": "KELSON ALVES",
        "telefone": "(85) 99769-9760",
        "bairro": "VILA UNIÃO",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "RAIO DE SOL",
        "cnpj": "23.668.402/0001-64",
        "lider": "LEIDIVANIA MARIA",
        "telefone": "(85) 99234-0148",
        "bairro": "GENIBAÚ",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "ROSA VIRGINIA",
        "cnpj": "09.635.604/0001-89",
        "lider": "MUSAMARA PEREIRA",
        "telefone": "(85) 98962-1862",
        "bairro": "SANTA TEREZINHA",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "SOCRELP (Sociedade Comunitária de Reciclagem de Lixo do Pirambu)",
        "cnpj": "00.118.784/0001-57",
        "lider": "JANETE CABRAL",
        "telefone": "(85) 98613-0768",
        "bairro": "PIRAMBU",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    },
    {
        "nome": "VIVA A VIDA",
        "cnpj": "07.865.301/0001-27",
        "lider": "LAUDIRENE",
        "telefone": "(85) 98528-9578",
        "bairro": "FARIAS BRITO",
        "cidade": "FORTALEZA",
        "uf": "CE",
        "status": "ativo"
    }
]

# =============== 3. Criar/Atualizar Associações ===============
total_criadas = 0
total_atualizadas = 0

for assoc_data in associacoes_data:
    # Verifica se já existe pelo CNPJ
    existing_assoc = db.query(models.Associacao).filter(
        models.Associacao.cnpj == assoc_data["cnpj"]
    ).first()
    
    if existing_assoc:
        # Atualiza dados existentes
        existing_assoc.lider = assoc_data["lider"]
        existing_assoc.telefone = assoc_data["telefone"]
        existing_assoc.bairro = assoc_data["bairro"]
        existing_assoc.cidade = assoc_data["cidade"]
        existing_assoc.uf = assoc_data["uf"]
        existing_assoc.status = assoc_data["status"]
        
        # Atualiza nome do parceiro também
        if existing_assoc.parceiro_info:
            existing_assoc.parceiro_info.nome = assoc_data["nome"]
        
        total_atualizadas += 1
        print(f"  📝 Atualizada: {assoc_data['nome'][:50]}...")
    else:
        # Cria novo parceiro
        parceiro = models.Parceiro(
            nome=assoc_data["nome"],
            id_tipo_parceiro=tipo_assoc.id
        )
        db.add(parceiro)
        db.flush()  # Para pegar o ID gerado
        
        # Cria associação
        associacao = models.Associacao(
            parceiro_id=parceiro.id,
            cnpj=assoc_data["cnpj"],
            lider=assoc_data["lider"],
            telefone=assoc_data["telefone"],
            bairro=assoc_data["bairro"],
            cidade=assoc_data["cidade"],
            uf=assoc_data["uf"],
            status=assoc_data["status"],
            ativo=True
        )
        db.add(associacao)
        total_criadas += 1
        print(f"  ✅ Criada: {assoc_data['nome'][:50]}...")

db.commit()

# =============== 4. Resumo ===============
print("\n" + "="*70)
print("🎉 Popularização concluída!")
print(f"   ✅ {total_criadas} associações criadas")
print(f"   📝 {total_atualizadas} associações atualizadas")
print(f"   📊 Total: {total_criadas + total_atualizadas} associações")
print("="*70)

# =============== 5. Verificar ===============
total_geral = db.query(models.Associacao).count()
print(f"\n📈 Total de associações no banco: {total_geral}")

# =============== 6. Listar Todas ===============
print("\n" + "="*70)
print("📋 ASSOCIAÇÕES CADASTRADAS:")
print("="*70)
print(f"{'NOME':<50} {'BAIRRO':<20} {'PRESIDENTE':<25} {'CNPJ':<20}")
print("-"*115)

associacoes = db.query(models.Associacao).join(models.Parceiro).all()
for assoc in associacoes:
    nome = assoc.parceiro_info.nome[:48] + ".." if len(assoc.parceiro_info.nome) > 50 else assoc.parceiro_info.nome
    print(f"{nome:<50} {assoc.bairro:<20} {assoc.lider:<25} {assoc.cnpj:<20}")

print("="*70)

db.close()