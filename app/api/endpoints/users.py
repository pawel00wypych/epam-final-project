from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.simple_db import users_db
from uuid import uuid4
from datetime import datetime, timezone
from app.schemas.user import AuthModel, UserPublic
from app.schemas.token import Token
from app.core.security import (hash_password,
                               login_for_access_token)

router = APIRouter()

@router.post("/auth", response_model=UserPublic,
             status_code=status.HTTP_201_CREATED)
def register_user(user_data: AuthModel):
    if user_data.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    if user_data.password != user_data.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    user_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    hashed_password = hash_password(user_data.password)

    users_db[user_data.username] = {
                    "id": user_id,
                    "username": user_data.username,
                    "hashed_password": hashed_password,
                    "created_at": created_at
    }

    return {
        "id": user_id,
        "username": user_data.username,
        "created_at": created_at
    }

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_for_access_token(form_data.username, form_data.password)