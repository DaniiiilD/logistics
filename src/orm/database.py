import contextvars
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


class Base(DeclarativeBase):
    pass


db_session = contextvars.ContextVar("db_session")


@asynccontextmanager
async def async_session_factory() -> AsyncGenerator[AsyncSession, None]:
    session_ = db_session.get(None)
    if session_:
        yield session_
    else:
        session_ = async_session()
        token = db_session.set(session_)
        try:
            yield session_
        except Exception:
            await session_.rollback()
            raise
        finally:
            await session_.close()
            db_session.reset(token)
