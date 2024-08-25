from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# deprecated
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base


DB_URL: str = 'sqlite+aiosqlite:///./app.db'

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()
Base = declarative_base()
