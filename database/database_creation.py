import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, text, SQLModel


DATABASE_URL = (
    "sqlite+pysqlite:///:memory:" if os.getenv("TESTING") else "postgresql+psycopg2://fastapi:fastapi@db/fastapi"
)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
