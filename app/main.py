from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from .utils.db import engine, Base, check_db_connection
from . import models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connection()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    engine.connect().execute(text("SELECT 1"))
    return { "status" : "ok" , "db" : "connected" }