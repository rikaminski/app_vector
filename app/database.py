
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()