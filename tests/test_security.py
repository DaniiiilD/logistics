from src.core.security import hash_tg_id, encrypt_tg_id, decrypt_tg_id

id_example = 123456789

def test_hash_tg_id_consistency():
    hash1 = hash_tg_id(id_example)
    hash2 = hash_tg_id(id_example)
    
    assert hash1 == hash2
    assert isinstance(hash1, str)
    
def test_encryption_roundtrip():
    encrypted_data = encrypt_tg_id(id_example)
    assert isinstance(encrypted_data, str)
    assert encrypted_data != str(id_example)

    decrypted_id = decrypt_tg_id(encrypted_data)
    
    assert decrypted_id == id_example
    assert isinstance(decrypted_id, int)