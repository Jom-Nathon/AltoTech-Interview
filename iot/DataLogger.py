
from config import settings

from sqlmodel import SQLModel, Field
from typing import Optional
import datetime, time
import asyncpg
import asyncio

#Timeseries data: TimescaleDB
#Realtime data: Supabase
#Relational data: PostgreSQL
class RawData(SQLModel, table=True):
    __tablename__ = "sensor_data"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: int
    datetime: datetime.datetime
    device_id: str
    datapoint: str
    value: str
    
    # Add TimescaleDB hypertable configuration
    class Config:
        arbitrary_types_allowed = True

class DataLogger:
    def __init__(self):
        # Initialize your database connections here
        pass
        
    def store_timescale(self, data):
        # Store data to TimescaleDB
        pass
        
    def store_supabase(self, data):
        # Store data to Supabase
        pass
        
    def process_message(self, message):
        # Process incoming messages from the event bus
        # Store to both TimescaleDB and Supabase
        self.store_timescale(message)
        self.store_supabase(message)
        
    def run(self):
        # Subscribe to the event bus and process messages
        while True:
            # Here you would subscribe to your event bus
            # and process incoming messages
            time.sleep(0.1)  # Small delay to prevent CPU overuse

async def main():
    conn = await asyncpg.connect(settings.CONNECTION)
    extensions = await conn.fetch("select extname, extversion from pg_extension")
    for extension in extensions:
        print(extension)
    await conn.close()

asyncio.run(main())