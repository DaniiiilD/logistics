from src.core.config import settings
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


async def get_current_user_payload(request: Request) -> dict:

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


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(get_current_user_payload)) -> int:
        if payload["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Недостаточео прав")
        return payload["id"]
