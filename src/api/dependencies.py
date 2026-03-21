from functools import wraps
from src.orm.database import SessionLocal

def with_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(*args, db=db, **kwargs)
            db.commit()
            return result
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    return wrapper