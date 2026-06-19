from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from bcrypt import hashpw, gensalt, checkpw
from starlette.status import HTTP_401_UNAUTHORIZED
from jwt.exceptions import InvalidTokenError
from .config import settings
from app.schemas.user import InDbUser
from app.schemas.token import Token, TokenData
from ..db.simple_db import users_db

DUMMY_BCRYPT_HASH = "$2b$12$C6UzMDM.H6dfI/f/IKcEeO6tQKZwJvq0eYI7M5Iq2yI7h6/3VYf5G"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    salt = gensalt()
    pw_bytes = password.encode('utf-8')
    hashed_password = hashpw(pw_bytes, salt)
    return hashed_password.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(data: InDbUser, expires_delta: timedelta | None = None):

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {
            "sub": data.username,
            "user_id": data.id,
            "exp": expire,
        }

    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def get_user(db, username: str) -> InDbUser | None:
    if username in db:
        user_dict = db[username]
        return InDbUser(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        check_password(password, DUMMY_BCRYPT_HASH) # prevent from timing attacks
        return False
    if not check_password(password, user.hashed_password):
        return False
    return user

def login_for_access_token(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data=user,
        expires_delta=settings.access_token_expire_minutes
    )
    return Token(access_token=access_token, token_type='bearer')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        username = payload.get("sub")
        user_id = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user