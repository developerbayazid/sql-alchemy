from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, delete, update, text, func, and_, or_, not_, Numeric, Enum as SQLEnum, Integer, BigInteger, String, Date, DateTime, select, Boolean, Float, Text, ForeignKey
from datetime import datetime


DBModel = declarative_base()


class User(DBModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, index=True, unique=True)
    mobile = Column(String(20), nullable=False, index=True)
    password = Column(String(500), nullable=False)
    otp = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    def full_name(self):
        return f"{self.firstname} {self.lastname}"



class CategoryModel(DBModel):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    # Relationship
    products = relationship("ProductModel", back_populates="categories")

    

class ProductModel(DBModel):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    img_url = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    # Relationship
    categories = relationship("CategoryModel", back_populates="products")