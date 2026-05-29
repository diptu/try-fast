from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load local .env if available
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)


class Settings(BaseSettings):
    SERVICE_NAME: str = "User Service"
    SERVICE_VERSION: str = "0.1.0"
    PORT: int = 8001

    DATABASE_URL: str | None = None
    DEFAULT_USER_IMAGE: str = (
        "microblog-platform/apps/user-service/user_service/assets/user.png"
    )

    model_config = SettingsConfigDict(extra="ignore", env_file=None)


settings = Settings()
settings = Settings()
