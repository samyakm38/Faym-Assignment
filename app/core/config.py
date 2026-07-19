from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./payouts.db"

    ADVANCE_PERCENTAGE: float = 0.10
    WITHDRAWAL_COOLDOWN_HOURS: int = 24

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()