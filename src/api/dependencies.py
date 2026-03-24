from functools import wraps
from src.orm.database import db_factory

def in_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with db_factory.get_session() as session:
            try:
                result = await func(*args, session=session, **kwargs)
                await session.commit()  
                return result
            except Exception:
                await session.rollback()
                raise
    return wrapper