from functools import wraps
from src.orm.database import async_session_factory


def in_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            try:
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise

    return wrapper
