from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.api.services.utilities.hash_password import verify_password
from src.orm.repositories.user import UserRepository
from src.orm.models.user import User
from src.orm.database import with_db

@with_db
def login_user(username: str, password: str, db: Session = None) -> User:
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(username)
    if not user:
        raise HTTPException(status_code=401, detail = "Неверный email или пароль")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail = 'неверный email или пароль')
    return user
