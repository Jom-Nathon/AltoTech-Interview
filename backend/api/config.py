from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    # Supabase settings
    SUPABASE_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    SUPABASE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'jommy348')
    SUPABASE_SERVER: str = os.getenv('POSTGRES_SERVER', 'supabase')
    SUPABASE_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    SUPABASE_DB: str = os.getenv('POSTGRES_DB', 'postgres')

    # Postgres settings
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'jommy348')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', 'postgres')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'relational')

    # TimescaleDB settings
    TIMESCALE_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    TIMESCALE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'jommy348')
    TIMESCALE_SERVER: str = os.getenv('POSTGRES_SERVER', 'timescaledb')
    TIMESCALE_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    TIMESCALE_DB: str = os.getenv('POSTGRES_DB', 'postgres')


    POSTGRES_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    TIMESCALE_URL: str = f"postgresql://{TIMESCALE_USER}:{TIMESCALE_PASSWORD}@{TIMESCALE_SERVER}:{TIMESCALE_PORT}/{TIMESCALE_DB}"
    SUPABASE_URL: str = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_SERVER}:{SUPABASE_PORT}/{SUPABASE_DB}"

    class Config:
        case_sensitive = True

settings = Settings() 
