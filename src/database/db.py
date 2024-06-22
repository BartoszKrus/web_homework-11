from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://postgres:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/rest_app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()