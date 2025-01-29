# datetime,power_kw_power_meter_1,power_kw_power_meter_2,power_kw_power_meter_3,power_kw_power_meter_4,power_kw_power_meter_5,power_kw_power_meter_6
# 2024-11-07 00:00:00.00,4.83,4.77,4.52,4.48,4.3,4.24

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
    power_kw_power_meter_1 = round(random.uniform(0,20), 1)
    power_kw_power_meter_2 = round(random.uniform(0,20), 1)
    power_kw_power_meter_3 = round(random.uniform(0,20), 1)
    power_kw_power_meter_4 = round(random.uniform(0,20), 1)
    power_kw_power_meter_5 = round(random.uniform(0,20), 1)
    power_kw_power_meter_6 = round(random.uniform(0,20), 1)

    data = {
            "datetime": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')),
            "power_kw_power_meter_1": power_kw_power_meter_1,
            "power_kw_power_meter_2": power_kw_power_meter_2,
            "power_kw_power_meter_3": power_kw_power_meter_3,
            "power_kw_power_meter_4": power_kw_power_meter_4,
            "power_kw_power_meter_5": power_kw_power_meter_5,
            "power_kw_power_meter_6": power_kw_power_meter_6,
    }
    return json.dumps(data)
    
def main():
    connection, channel = connect_rabbitmq()
    try:
        while True:
            data = gen_data()
            channel.basic_publish(exchange='pubsub', routing_key='', body=data)
            print(f"Publishing PowerMeter data: {data}")
            time.sleep(5)
    finally:
        connection.close()

if __name__ == "__main__":
    main()