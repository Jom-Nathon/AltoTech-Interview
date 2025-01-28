# datetime,                online_status,  sensitivity,  presence_state
# 2024-12-03 00:00:00.00,  online,         100.0,        unoccupied

import datetime, random, time, json
import pika

class LifeBeing:
    def __init__(self):
        now = datetime.datetime.now()
        self.time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        self.online_status = "Online"
        self.sensitivity = None
        self.presence_state = None

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
        self.presence_state = random.choice(["unoccupied", "occupied"])
        self.sensitivity = round(random.uniform(99,100), 1)
        print(self.time, self.online_status, self.sensitivity, self.presence_state)
        return self
    
    def main(self):
        while True:
            data = self.gen_data()
            print(f"Publishing IAQ data: {data}")
            time.sleep(5)  
    
test = LifeBeing()
test.gen_data()