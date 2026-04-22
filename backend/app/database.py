from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


from app.core.config import settings

SQL_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQL_DATABASE_URL
)

SessionLocal= sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()