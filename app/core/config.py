from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    database_url: str

    class Config:
        env_file = ".env_dev" # .env for production

settings = Settings()
