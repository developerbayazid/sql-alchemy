from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, delete, update, text, func, and_, or_, not_, Numeric, Enum as SQLEnum, Integer, BigInteger, String, Date, DateTime, select, Boolean, Float, Text, ForeignKey
from datetime import datetime


base = declarative_base()


class Student(base):
    __tablename__ = "students"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)