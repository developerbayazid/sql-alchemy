from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/sales_db")
db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)