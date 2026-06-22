from fastapi import FastAPI
from app.api import api
app = FastAPI(title="EPAM final project", debug=True)
app.include_router(api.api_router)

@app.get("/")
def root():
    return {"message": "Hello World!"}