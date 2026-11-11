from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    app_env: str = 'development'
    database_url: str = 'sqlite:///./assistant.db'
    secret_key: str = 'change-me-before-use'
    access_token_minutes: int = 60
    allowed_origins: str = 'http://localhost:3000'
    llm_provider: str = 'gemini'
    gemini_api_key: str = ''
    gemini_model: str = 'gemini-2.5-flash'
    retrieval_enabled: bool = True
    retrieval_backend: str = 'demo'
    qdrant_url: str = ''
    qdrant_api_key: str = ''
    qdrant_collection: str = 'assistant_knowledge'
    embedding_model: str = 'gemini-embedding-001'
    embedding_dimension: int = 768

settings = Settings()
