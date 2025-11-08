from app.database import SessionLocal
from app import crud,schemas

db = SessionLocal()
try:
    user = schemas.UsuarioCreate(username="admin", password="123") # Seu usuário inicial
    crud.create_user(db, user)
    print("Usuário 'admin' criado com sucesso!")
except Exception as e:
    print(f"Erro ao criar usuário (já existe?): {e}")
finally:
    db.close()