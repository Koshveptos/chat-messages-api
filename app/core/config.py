from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    app_name: str = "Chat API"
    database_url: str
    debug: bool = False


settings = Settings()  # type: ignore [call-arg]
