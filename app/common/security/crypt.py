import bcrypt


def hash_password(password: str) -> str:
    encoded = password.encode('utf-8')
    encoded_hash = bcrypt.hashpw(encoded, bcrypt.gensalt())
    password_hash = encoded_hash.decode('utf-8')
    return password_hash


def verify_password(password: str, password_hash: str) -> bool:
    encoded = password.encode('utf-8')
    encoded_hash = password_hash.encode('utf-8')
    return bcrypt.checkpw(encoded, encoded_hash)
