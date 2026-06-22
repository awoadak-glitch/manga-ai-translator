from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    database_url: str = "sqlite:///./data/app.db"
    media_root: str = "./data/media"
    backend_cors_origins: str = "http://localhost:3000"
    demo_mode: bool = True
    translation_provider: str = "demo"
    openai_api_key: str | None = None
    libretranslate_url: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


settings = Settings()
