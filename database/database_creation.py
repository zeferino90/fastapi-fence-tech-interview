# init my sqlalchemy database with postgresl

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = 'postgresql'
USER = 'user'
PASSWORD = 'user'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
