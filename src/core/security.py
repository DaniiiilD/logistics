from cryptography.fernet import Fernet
import hashlib
from src.core.config import settings

cipher = Fernet(settings.ENCRYPTION_KEY.encode())

def hash_tg_id(tg_id: int) -> str:
    encode_tg_str = str(tg_id).encode()
    hash = hashlib.sha256(encode_tg_str).hexdigest()
    return hash

def encrypt_tg_id(tg_id: int) -> str:
    tg_bytes = str(tg_id).encode()
    encrypted_bytes = cipher.encrypt(tg_bytes)
    encrypted_str = encrypted_bytes.decode()
    return encrypted_str

def decrypt_tg_id(encrypted_str: str) -> int:
    decrypted_str = cipher.decrypt(encrypted_str.encode())
    return int(decrypted_str.decode())