from fastapi import APIRouter

router = APIRouter()

@router.post("/auth")
def auth():
    return {"auth": "to be implemented"}

@router.post("/login")
def login():
    return {"login": "to be implemented"}