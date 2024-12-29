from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import Base
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_pgvector_extension(conn: AsyncSession):
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

async def get_db():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        # Criar todas as tabelas
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_db()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())