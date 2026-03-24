from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

class DatabaseFactory:
    def __init__(self):
        self.session_factory = async_sessionmaker(
            engine,
            class_ = AsyncSession,
            expire_on_commit= False
        )
        
    def get_session(self) -> AsyncSession:
        return self.session_factory()
    
db_factory = DatabaseFactory()