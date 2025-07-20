import jwt

SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"


def create_jwt(username: str, expires_at: int) -> str:
    """where experies_at is a unix_timestamp"""

    payload = {
        "sub": username,
        "exp": expires_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
