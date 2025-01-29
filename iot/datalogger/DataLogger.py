from iot.datalogger.config import settings
from typing import Optional, Union
import time, json, os, datetime
from sqlmodel import Field, SQLModel, Session, SQLModel, create_engine, select, create_engine
import pika
from pika.exchange_type import ExchangeType
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)

credentials = pika.PlainCredentials('guest', 'guest')
connection_parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials
)

engine = create_engine(settings.TIMESCALE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session_timescale():
    with Session(engine) as session:
        yield session

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()
            channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(5)

class RawData(SQLModel, table=True):
    __tablename__ = "raw_data"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: int = Field(index=True)
    date_time: str = Field(index=True)
    device_id: str = Field(index=True)
    datapoint: str = Field(index=True)
    value: str = Field()  # Changed to str to handle all value types

class CurrentData(SQLModel, table=True):
    __tablename__ = "current_data"

    timestamp: int = Field(index=True)
    date_time: str = Field(index=True)
    device_id: str = Field(index=True, primary_key=True)
    datapoint: str = Field(index=True)
    value: str = Field(index=True)

def store_measurement(data: dict):
    try:
        with Session(engine) as session:
            # Extract common fields
            if "device_id" in data:
                device_id = str(data["device_id"])
                timestamp = int(time.mktime(datetime.datetime.strptime(data["datetime"], '%Y-%m-%d %H:%M:%S.%f').timetuple()))
                date_time = data["datetime"]
                
                # Store each measurement as a separate record
                for key, value in data.items():
                    if key not in ["device_id", "datetime"]:  # Skip metadata fields
                        if value is not None:
                            raw_data = RawData(
                                timestamp=timestamp,
                                date_time=date_time,
                                device_id=device_id,
                                datapoint=key,
                                value=str(value)  # Convert all values to string
                            )
                            session.add(raw_data)
                            logger.info(f"Stored {key} for device {device_id}")
            else:
                timestamp = int(time.mktime(datetime.datetime.strptime(data["datetime"], '%Y-%m-%d %H:%M:%S.%f').timetuple()))
                date_time = data["datetime"]
                for key, value in data.items():
                    if key not in ["datetime"]:  # Skip metadata fields
                        if value is not None:
                            raw_data = RawData(
                                timestamp=timestamp,
                                date_time=date_time,
                                device_id=key,
                                datapoint="kW",
                                value=str(value)  # Convert all values to string
                            )
                            session.add(raw_data)
                            logger.info(f"Stored {key} for device {device_id}")
            
            session.commit()
            
    except Exception as e:
        logger.error(f"Error storing data: {e}")

def on_message_recieved(ch, method, properties, body):

    try:
        parsed_data = json.loads(body)
        print(parsed_data)
        store_measurement(parsed_data)
                
    except Exception as e:
        print(f"Error storing data: {e}")

    
def main():
    connection, channel = connect_rabbitmq()
    create_db_and_tables()
    try:
        while True:
            queue = channel.queue_declare(queue='', exclusive=True)
            channel.queue_bind(exchange='pubsub', queue=queue.method.queue)
            channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_recieved)
            channel.start_consuming()
            print(f"Listening for data...")
            time.sleep(5)
    finally:
        connection.close()

if __name__ == "__main__":
    main()

