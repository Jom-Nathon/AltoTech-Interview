# datetime,                temperature, humidity,  co2
# 2024-12-27 00:00:00.00,  24.5,        55.0,      488.8

import datetime, random, time, json
import pika

class IAQ:
    def __init__(self):
        now = datetime.datetime.now()
        self.time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        self.temperature = None
        self.humidity = None
        self.co2 = None

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        # Declare exchange
        self.channel.exchange_declare(
            exchange='sensor_data',
            exchange_type='fanout'
        )

    def gen_data(self):
        self.temperature = round(random.uniform(10,50), 1)
        self.humidity = round(random.uniform(1,100), 1)
        self.co2 = round(random.uniform(300,2000), 1)
        print(self.time, self.temperature, self.humidity, self.co2)
        return self
    
    def main(self):
        while True:
            data = self.gen_data()
            print(f"Publishing IAQ data: {data}")
            time.sleep(5)  
    
test = IAQ()
test.gen_data()