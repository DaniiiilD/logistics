from src.config import settings
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Request, HTTPException
from jwt import PyJWKError


def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_user_if_from_token(request: Request) -> int:

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except PyJWKError:
        raise HTTPException(status_code=401, detail="Токен невалиден или протух")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="В токене нет user_id")

    return int(user_id_str)
