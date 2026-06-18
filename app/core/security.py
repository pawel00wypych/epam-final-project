from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from bcrypt import hashpw, gensalt, checkpw
from starlette.status import HTTP_401_UNAUTHORIZED
from jwt.exceptions import InvalidTokenError
from .config import settings
from app.schemas.user import UserLogin, InDbUser
from app.schemas.token import Token, TokenData
from ..db.simple_db import users_db

DUMMY_BCRYPT_HASH = "$2b$12$C6UzMDM.H6dfI/f/IKcEeO6tQKZwJvq0eYI7M5Iq2yI7h6/3VYf5G"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
            "sub": data.login,
            "user_id": data.id,
            "exp": expire,
        }

    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def get_user(db, login: str) -> InDbUser | None:
    if login in db:
        user_dict = db[login]
        return InDbUser(**user_dict)
    return None

def authenticate_user(login: str, password: str):
    user = get_user(users_db, login)
    if not user:
        check_password(password, DUMMY_BCRYPT_HASH) # prevent from timing attacks
        return False
    if not check_password(password, user.hashed_password):
        return False
    return user

def login_for_access_token(login_data: UserLogin) -> Token:
    user = authenticate_user(login_data.login, login_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='incorrect login or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data=user, expires_delta=access_token_expires)
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
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(users_db, login=token_data.login)
    if user is None:
        raise credentials_exception
    return user