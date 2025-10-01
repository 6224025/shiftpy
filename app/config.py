from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    APP_TITLE: str 
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()