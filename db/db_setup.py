from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/text_compare"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True   #use new async api of latest version in sqlalchemy
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=True, bind=engine, future=True
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()