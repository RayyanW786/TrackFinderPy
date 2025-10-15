from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PG_HOST: str = Field(..., description="Postgres host")
    PG_PORT: int = Field(..., description="Postgres port")
    PG_DB: str = Field(..., description="Postgres database")
    PG_USER: str = Field(..., description="Postgres user")
    PG_PASSWORD: str = Field(..., description="Postgres password")

    SCYLLA_HOSTS: str = Field(..., description="Comma-separated Scylla hosts")
    SCYLLA_KEYSPACE: str = Field(..., description="Scylla keyspace")

    REDIS_URL: str = Field(..., description="Redis URL")

    SECRET_KEY: str = Field(..., description="App secret")
    AUTH_PEPPER: str = Field(..., description="Argon2 pepper")

    MAX_UPLOAD_BYTES: int = Field(..., description="Max upload size in bytes")
    MAX_DECODED_SECONDS: int = Field(..., description="Max decoded audio seconds")

    RL_MATCH_PER_MINUTE: int = Field(
        ..., description="Rate limit /match per minute per IP"
    )
    RL_MATCH_PER_DAY: int = Field(..., description="Rate limit /match per day per user")
    RL_WS_MAX_CONNS_PER_USER: int = Field(..., description="Max WS conns per user")
    RL_WS_MAX_MSGS_PER_MIN: int = Field(..., description="WS messages per minute")

    ARGON2_TIME_COST: int = Field(..., description="Argon2 time cost")
    ARGON2_MEMORY_COST_MB: int = Field(..., description="Argon2 memory (MB)")
    ARGON2_PARALLELISM: int = Field(..., description="Argon2 parallelism")


settings = Settings()  # pyright: ignore[reportCallIssue]
