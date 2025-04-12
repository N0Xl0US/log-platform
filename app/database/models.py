from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GeneralLog(Base):
    __tablename__ = 'general_logs'

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False)
    timestamp = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuthLog(Base):
    __tablename__ = 'auth_logs'

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    timestamp = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 