from iot.datalogger_supabase.config import settings
from typing import Optional
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

engine = create_engine(settings.SUPABASE_URL, echo=True)

class NewestData(SQLModel, table=True):
    __tablename__ = "newest_data"

    timestamp: int = Field()
    date_time: str = Field()
    device_id: str = Field(primary_key=True)
    datapoint: str = Field(primary_key=True)
    value: str = Field()

def create_db_and_tables():
    try:
        NewestData.__table__.create(engine)
    except:
        pass

def get_session():
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

def store_measurement_supabase(data: dict):
    with Session(engine) as session:
        if "device_id" not in data:
            device_id = ""
        else:
            device_id = str(data["device_id"])

        dt_obj = datetime.datetime.strptime(data["datetime"], '%Y-%m-%d %H:%M:%S.%f')
        timestamp = int(dt_obj.timestamp())
        date_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        
        for key, value in data.items():
            if key not in ["device_id", "datetime"] and value is not None:
                if device_id in ["","power_kw_power_meter_6", "power_kw_power_meter_4", "power_kw_power_meter_5", "power_kw_power_meter_3", "power_kw_power_meter_2", "power_kw_power_meter_1"]:
                    device_id = key
                    temp_datapoint = "power"
                else:
                    temp_datapoint = key

                try:
                    # Try to find existing record with composite key
                    statement = select(NewestData).where(
                        NewestData.device_id == device_id,
                        NewestData.datapoint == temp_datapoint
                    )
                    result = session.exec(statement).first()
                    
                    if result:
                        # Update existing record
                        result.timestamp = timestamp
                        result.date_time = date_time
                        result.value = str(value)
                        session.add(result)
                        logger.info(f"Updated record for device {device_id}, datapoint {temp_datapoint}")
                    else:
                        # Create new record
                        new_data = NewestData(
                            device_id=device_id,
                            datapoint=temp_datapoint,
                            timestamp=timestamp,
                            date_time=date_time,
                            value=str(value)
                        )
                        session.add(new_data)
                        logger.info(f"Created record for device {device_id}, datapoint {temp_datapoint}")
                    
                    # Commit each record individually to handle errors better
                    session.commit()
                    
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error processing datapoint {temp_datapoint} for device {device_id}: {e}")
                    continue           

def on_message_recieved(ch, method, properties, body):
    try:
        parsed_data = json.loads(body)
        store_measurement_supabase(parsed_data)

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

