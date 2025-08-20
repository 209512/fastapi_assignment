# app/configs/base.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    EDGEDB_DSN: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve()
    MEDIA_DIR: Path = BASE_DIR / "media"

    class Config:
        env_file = ".env"

# settings 객체를 import시점에 생성해 사용
settings = Settings()