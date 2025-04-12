from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# You might want to move this to an environment variable
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/logdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 