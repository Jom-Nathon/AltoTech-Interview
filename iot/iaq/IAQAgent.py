
import random, time, json
from datetime import datetime
import pika
from pika.exchange_type import ExchangeType
import os

# Use environment variables for configuration
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)

credentials = pika.PlainCredentials('guest', 'guest')
connection_parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials
)

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

def gen_data(device_id: str):
    temperature = round(random.uniform(10,50), 1)
    humidity = round(random.uniform(1,100), 1)
    co2 = round(random.uniform(300,2000), 1)

    data = {
            "device_id": device_id,
            "datetime": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')),
            "temperature": temperature,
            "humidity": humidity,
            "co2": co2
    }
    return json.dumps(data)

def main():
    connection, channel = connect_rabbitmq()
    try:
        while True:
            for device_id in range(1,20):
                data = gen_data(device_id)
                channel.basic_publish(exchange='pubsub', routing_key='', body=data)
                print(f"Publishing IAQ data: {data}")
                time.sleep(2)

    finally:
        connection.close()

if __name__ == "__main__":
    main()