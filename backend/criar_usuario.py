from app.database import SessionLocal
from app import crud,schemas

db = SessionLocal()
try:
    user = schemas.UsuarioCreate(
        username="gestao.rede",
        password="Rede123!") 
    crud.create_user(db, user)
    print("Usuário 'admin' criado com sucesso!")
except Exception as e:
    print(f"Erro ao criar usuário (já existe?): {e}")
finally:
    db.close()