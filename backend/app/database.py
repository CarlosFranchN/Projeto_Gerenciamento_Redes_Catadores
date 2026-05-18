from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




from app.core.config import settings

SQL_DATABASE_URL = settings.DATABASE_URL

if SQL_DATABASE_URL and SQL_DATABASE_URL.startswith("postgres://"):
    SQL_DATABASE_URL = SQL_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    SQL_DATABASE_URL
)

SessionLocal= sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()