from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise RAG Assistant"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:YOUR_PASSWORD"
        "@localhost:5432/enterprise_rag"
    )

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3.1:8b"
    EMBEDDING_MODEL: str = "bge-m3"
    EMBEDDING_DIMENSION: int = 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
