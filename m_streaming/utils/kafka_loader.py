import random
from time import sleep
from json import dumps
from kafka import KafkaProducer

code_list = [200, 202, 204, 300, 301, 302, 400, 401, 403, 404, 500, 502]
host_list = ['127.0.0.1', '10.0.0.2', '10.0.0.3']
user_list = ['peter', 'bob']
method_list = ['GET', 'POST']

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

while True:
    for e in range(50):
        data = {
            "host": random.choice(host_list),
            "user": random.choice(user_list),
            "method": random.choice(method_list),
            "path": "/sample-image.png",
            "code": random.choice(code_list),
            "size": random.choice(range(1, 10000))
        }
        producer.send('test', value=data)
    sleep(2)
