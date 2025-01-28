from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    # Timescale Settings
    # CONNECTION = "dbname=tsdb user=tsdbadmin password=e6odyjdedo6pjcsr host=k4js3f7yn4.ovbwjst5ro.tsdb.cloud.timescale.com port=34840 sslmode=require"
    CONNECTION : str = "postgres://tsdbadmin:e6odyjdedo6pjcsr@k4js3f7yn4.ovbwjst5ro.tsdb.cloud.timescale.com:34840/tsdb?sslmode=require"

    class Config:
        case_sensitive = True

settings = Settings() 
