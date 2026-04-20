from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    
    # Verifica se já existe admin
    admin = db.query(models.Usuario).filter(
        models.Usuario.username == "admin"
    ).first()
    
    if admin:
        print("⚠️  Usuário 'admin' já existe!")
        db.close()
        return
    
    # Cria admin
    admin = models.Usuario(
        username="admin",
        hashed_password=get_password_hash("senha123"),
        nome="Administrador",
        role="admin",
        ativo=True
    )
    
    db.add(admin)
    db.commit()
    
    print("✅ Usuário admin criado com sucesso!")
    print("   Username: admin")
    print("   Senha: senha123")
    print("\n⚠️  Troque a senha após o primeiro login!")
    
    db.close()

if __name__ == "__main__":
    create_admin()