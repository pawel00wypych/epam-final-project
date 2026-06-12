from fastapi import APIRouter, status, HTTPException
from app.db.simple_db import users_db
from uuid import uuid4
from datetime import datetime, timezone
from app.schemas.user import AuthModel, LoginModel
from app.core.security import hash_password

router = APIRouter()

@router.post("/auth", status_code=status.HTTP_201_CREATED)
def register_user(user_data: AuthModel):
    if user_data.login in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists",
        )

    if user_data.password != user_data.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    user_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    users_db[user_data.login] = {
                "id": user_id,
                "login": user_data.login,
                "hashed_password": hash_password(user_data.password),
                "created_at": created_at
    }
    return {
        "id": user_id,
        "login": user_data.login,
        "created_at": created_at
    }

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(login_data: LoginModel):
    return login_data