from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    # https://openrouter.ai/settings/keys
    OPEN_ROUTER_API_KEY: str = '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'
    OPENAI_API_KEY: str = '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'
    ANTROPIC_API_KEY: str = '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'

    class Config:
        case_sensitive = True

settings = Settings() 
