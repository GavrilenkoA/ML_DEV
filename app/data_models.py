from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base



Base = declarative_base()


DEFAULT_CREDITS = 10


class User(Base):
    __tablename__ = "users_data"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    credits = Column(Integer, default=DEFAULT_CREDITS)


class Predictions(Base):
    __tablename__ = "predictions"

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    diagnosis = Column(String(3), nullable=False)
    score = Column(Float, nullable=False)
    email = Column(String(50), nullable=False)
