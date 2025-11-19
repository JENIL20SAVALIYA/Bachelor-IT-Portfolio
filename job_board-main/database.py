from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker,Session
from models.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine,autocommit = False,autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
