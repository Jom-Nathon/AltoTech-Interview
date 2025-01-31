from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    # TimescaleDB settings
    TIMESCALE_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    TIMESCALE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'jommy348')
    TIMESCALE_SERVER: str = os.getenv('POSTGRES_SERVER', 'timescaledb')
    TIMESCALE_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    TIMESCALE_DB: str = os.getenv('POSTGRES_DB', 'postgres')

    TIMESCALE_URL: str = f"postgresql://{TIMESCALE_USER}:{TIMESCALE_PASSWORD}@{TIMESCALE_SERVER}:{TIMESCALE_PORT}/{TIMESCALE_DB}"

    class Config:
        case_sensitive = True

settings = Settings() 
