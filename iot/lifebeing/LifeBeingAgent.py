
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

def gen_data():
    device_id = str(random.randint(21,40))
    online_status = random.choice(["online","offline"])
    sensitivity = round(random.uniform(300,2000), 1)
    presence_state = random.choice(["occupied","unoccupied"])
    data = {
            "device_id": device_id,
            "datetime": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')),
            "online_status": online_status,
            "sensitivity": sensitivity,
            "presence_state": presence_state
    }
    return json.dumps(data)
    
def main():
    connection, channel = connect_rabbitmq()
    try:
        while True:
            data = gen_data()
            channel.basic_publish(exchange='pubsub', routing_key='', body=data)
            print(f"Publishing LifeBeing data: {data}")
            time.sleep(5)
    finally:
        connection.close()

if __name__ == "__main__":
    main()