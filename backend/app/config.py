from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./regtrace.db"
    openai_api_key: str = ""
    data_dir: str = ""
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def resolved_data_dir(self) -> Path:
        if self.data_dir:
            return Path(self.data_dir)
        here = Path(__file__).resolve()
        # backend/app/config.py -> repo data/
        return here.parents[2] / "data"

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://") and "+psycopg" not in url:
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    @property
    def use_openai(self) -> bool:
        return bool(self.openai_api_key.strip())


settings = Settings()
