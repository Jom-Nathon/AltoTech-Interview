from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    # Supabase settings
    SUPABASE_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    SUPABASE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'jommy348')
    SUPABASE_SERVER: str = os.getenv('POSTGRES_SERVER', 'supabase')
    SUPABASE_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    SUPABASE_DB: str = os.getenv('POSTGRES_DB', 'postgres')

    SUPABASE_URL: str = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_SERVER}:{SUPABASE_PORT}/{SUPABASE_DB}"

    class Config:
        case_sensitive = True

settings = Settings() 
