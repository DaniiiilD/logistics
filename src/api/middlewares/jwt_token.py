from src.config import settings
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Request, HTTPException, Depends
from jwt import PyJWKError


def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user_payload(request: Request) -> int:

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
    role = payload.get("role")

    if not user_id_str or not role:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    return {"id": int(user_id_str), "role": role}


async def require_driver(payload: dict = Depends(get_current_user_payload)) -> int:
    """(проверка на водителя) и return его user_id"""
    if payload["role"] != "driver":
        raise HTTPException(status_code=403, detail="Доступ только для водителей!")
    return payload["id"]


async def require_company(payload: dict = Depends(get_current_user_payload)) -> int:
    """(пускает только компании) и return его user_id"""
    if payload["role"] != "company":
        raise HTTPException(status_code=403, detail="Доступ только для комапний!")
    return payload["id"]
