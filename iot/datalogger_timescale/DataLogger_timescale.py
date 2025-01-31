from iot.datalogger_timescale.config import settings
import time, json, os, datetime
import pika
from pika.exchange_type import ExchangeType
import logging, psycopg2

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


with psycopg2.connect(settings.TIMESCALE_URL) as conn:
    cursor = conn.cursor()
    # use the cursor to interact with your database
    # cursor.execute("SELECT * FROM table")

def create_db_and_tables():
    try:
        query_create_sensordata_table = """CREATE TABLE raw_data (
                                            timestamp INTEGER,
                                            date_time TIMESTAMPTZ NOT NULL,
                                            device_id TEXT,
                                            datapoint TEXT,
                                            value TEXT
                                            );
                                    """
        query_create_sensordata_hypertable = "SELECT create_hypertable('raw_data', by_range('timestamp'));"

        cursor = conn.cursor()
        cursor.execute(query_create_sensordata_table)
        cursor.execute(query_create_sensordata_hypertable)
        # commit changes to the database to make changes persistent
        conn.commit()
        cursor.close()
        logger.info("Successfully created tables")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")

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

def store_measurement_timescale(data: dict):
    try:
        if "device_id" not in data:
            device_id=""
        else:
            device_id = str(data["device_id"])
        dt_obj = datetime.datetime.strptime(data["datetime"], '%Y-%m-%d %H:%M:%S.%f')
        timestamp = int(dt_obj.timestamp())
        date_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        
        for key, value in data.items():
            if key not in ["device_id", "datetime"] and value is not None:
                if device_id == "":
                    query = """INSERT INTO raw_data (timestamp, date_time, device_id, datapoint, value)
                            VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(query, (timestamp, date_time, key, "power", str(value)))
                
                else:
                    query = """INSERT INTO raw_data (timestamp, date_time, device_id, datapoint, value)
                            VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(query, (timestamp, date_time, device_id, key, str(value)))
        conn.commit()
        logger.info(f"Successfully stored/updated data for device {device_id}")
            
    except Exception as e:
        logger.error(f"Error storing data: {e}")
        conn.rollback()


def on_message_recieved(ch, method, properties, body):
    try:
        parsed_data = json.loads(body)
        store_measurement_timescale(parsed_data)
                
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

