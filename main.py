from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, select
from pydantic import BaseModel

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




