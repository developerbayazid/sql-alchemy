from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import DATABASE_URL

base = declarative_base()

engine = create_async_engine(DATABASE_URL)
db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with db_session() as session:
        yield session