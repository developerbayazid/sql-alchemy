from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Numeric, Enum, Integer, BigInteger, String, Date, DateTime, select, Boolean, Float, Text, ForeignKey
from pydantic import BaseModel
from datetime import datetime

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


class UserRole(enum.Enum):
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
    
    def full_name(self):
        return f"{self.firstname} {self.lastname}"
               


class ItemDB(DBModel):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), nullable=False, default='Bayazid')
    email = Column(String(50), nullable=False, unique=True, index=True)
    mobile = Column(String(15), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    password = Column(String(500), nullable=False)
    otp = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    balance = Column(Float, default=0.00)
    bio = Column(Text, nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.user)
    money = Column(Numeric(10, 2), default=0.00)
    



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
async def user_create():
    async with db_session() as session:
        user = User(firstname="demo", lastname="demo", email="demo@live2.com", mobile="02393", password="abc@demo", otp="239")
        session.add(user)
        await session.commit()
        return{
            "status" : "success",
            "message" : "user created!"
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




