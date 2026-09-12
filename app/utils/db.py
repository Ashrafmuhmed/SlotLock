from sqlalchemy import create_engine,  text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def check_db_connection():
    try:
        engine.connect().execute(text("SELECT 1"))
        print("db connected")
        return True
    except Exception as e:
        print("error with connection %s", e)
        return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()