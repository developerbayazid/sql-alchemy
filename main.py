from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Numeric, Enum as SQLEnum, Integer, BigInteger, String, Date, DateTime, select, Boolean, Float, Text, ForeignKey
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List

app = FastAPI()

# Database connection
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/sales_db")
db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



@app.get('/db-check')
async def db_check():
    
    try:
        conn = await engine.connect()
        await conn.close()
        return {
            "status" : "success",
            "message" : "DB Connected"
        }
    except Exception as e:
        return {
            "status" : "error",
            "message" : str(e)
        }
        

class UserValidator(BaseModel):
    firstname:str
    lastname:str
    email:str
    mobile:str
    password:str
    otp:str


class UserRole(Enum):
    admin = "admin"
    user = "user"
    manager = "manager"
     
        
DBModel = declarative_base()

class User(DBModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)
    otp = Column(String)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    def full_name(self):
        return f"{self.firstname} {self.lastname}"
               


# class ItemDB(DBModel):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     firstname = Column(String(100), nullable=False, default='Bayazid')
#     email = Column(String(50), nullable=False, unique=True, index=True)
#     mobile = Column(String(15), nullable=True, index=True)
#     is_active = Column(Boolean, default=True)
#     password = Column(String(500), nullable=False)
#     otp = Column(String(15), nullable=True)
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#     balance = Column(Float, default=0.00)
#     bio = Column(Text, nullable=True)
#     user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
#     user_role = Column(SQLEnum(UserRole), default=UserRole.user)
#     money = Column(Numeric(10, 2), default=0.00)
    



@app.get('/get-user')
async def get_user():
    async with db_session() as session:
        results = await session.get(User, 100)
        return{
            "fullName": results.full_name(),
            "email": results.email
        }

        
@app.get('/user-list')
async def user_list():
    async with db_session() as session:
        results = await session.execute(select(User))
        data = results.scalars().all()
        return data
    
    
    
@app.post('/create-user')
async def user_create(data: UserValidator):
    try:
        async with db_session() as session:
            user = User(**data.model_dump())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return{
                "status": "success",
                "user_id": user.id
            }
        
    except Exception as e:
        return {
            "error": str(e)
        }


@app.post('/user-create')
async def create_user(user: UserValidator):
    try:
        async with db_session() as session:
            result = User(**user.model_dump())
            session.add(result)
            await session.commit()
            return {
                "message" : "User Created successfully!"
            }
            
    except Exception as e:
        return {
            "message" : str(e)
        }




@app.post('/create-bulk-users')
async def create_bulk_users(data: List[UserValidator]):
    try:
        async with db_session() as session:
            users = [User(**eachUser.model_dump()) for eachUser in data]
            session.add_all(users)
            await session.commit()
            for eachUser in users:
                await session.refresh(eachUser)
                
            return {
                "status" : "success",
                "data" : users
            }
            
    except Exception as e:
        return {"error": str(e)}





class ProductModel(DBModel):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    img_url = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)



@app.get('/product/{id}')
async def get_product(id: int):
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.id == id)
            results = await session.execute(query)
            data = results.scalars().first()
            return {
                "message" : "success",
                "data" : data
            }
    
    except Exception as e:
        return {"error": str(e)}



@app.get("/products")
async def get_all_products():
    try:
        async with db_session() as session:
            query = select(ProductModel)
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message" : "success",
                "data" : data
            }
    
    except Exception as e:
        return {
            "message" : "fail",
            "error" : str(e)
        }




@app.get('/product/price/{price}')
async def get_product_by_price(price: int):
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.price == price)
            # query = select(ProductModel).where(ProductModel.price > price)
            query = select(ProductModel).where(ProductModel.price < price)
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    
    
@app.get('/product/search/{keyword}')
async def get_product_by_search(keyword: str):
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.name.ilike(f"%{keyword}%"))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    


@app.get('/product_in_not_in')
async def get_product_by_in_not_in():
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.id.in_([1, 2, 3, 4]))
            query = select(ProductModel).where(ProductModel.id.not_in([1, 2, 3, 4]))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    
@app.get('/product_in_range')
async def get_product_by_range():
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.price.between(1000, 5000))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}



