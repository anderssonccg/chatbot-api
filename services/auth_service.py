import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt

ACCESS_TOKEN_DURATION = int(os.getenv("ACCESS_TOKEN_DURATION"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(id: str):
    token_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    token_data = {"sub": id, "exp": token_expiration}
    access_token = {
        "access_token": jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "Bearer",
    }
    return access_token


def decode_token(token: str):
    try:
        id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido"
        )
    return id


def create_verification_token(email: str):
    token_expiration = datetime.utcnow() + timedelta(hours=24)
    token_data = {"sub": email, "exp": token_expiration}
    access_token = {
        "access_token": jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "Bearer",
    }
    return access_token


def decode_verification_token(token: str):
    try:
        email = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get(
            "sub"
        )  # Retorna el email si es válido
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido"
        )
    return email
