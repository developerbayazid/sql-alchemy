from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, select


# Database connection
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/sales_db")


app = FastAPI()

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
        
        
metaData = MetaData()

# Table Define
users = Table(
    "users",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("firstname", String),
    Column("lastname", String)
)
               
        
@app.get('/user-list')
async def user_list():
    conn = await engine.connect()
    results = await conn.execute(select(users))
    data = results.mappings().all()
    await conn.close()
    
    return data