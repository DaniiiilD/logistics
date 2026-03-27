from src.config import settings
from datetime import datetime, timedelta, timezone
import jwt

def create_access_token(data: dict) -> str:
    
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt