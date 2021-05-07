from model import Model
import numpy as np
import pandas as pd
from itertools import cycle
import json
from kafka import KafkaConsumer, KafkaProducer

environ = dict(DB_USER="postgres", DB_PASS="postgres", DB_HOST="localhost", DB_PORT="5432", DB_NAME="postgres",
               KAFKA_TOPIC="mytopic", KAFKA_HOST="localhost:29092")

conf = {"tag": "AVT10:LC475",
"rollwsize" : '72',
"history": '24',
"future": '72'}

m = Model(conf)
m._set_from_pkl('D:\\vkr\\model\\resources\\restore_fuel_v5.pkl')

consumer_params = dict(bootstrap_servers=[environ["KAFKA_HOST"]], auto_offset_reset='latest', api_version=(0, 10),
                      max_partition_fetch_bytes=107374182, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
                      
kafka_consumer = KafkaConsumer(environ["KAFKA_TOPIC"], **consumer_params)

kafka_producer = KafkaProducer(bootstrap_servers=['localhost:29092'], api_version=(0, 10, 2), request_timeout_ms=10)

while True:
    print('here')
    for message in kafka_consumer:
        i_json = message.value
        # print(values_json)
        data = pd.read_json(path_or_buf=i_json, orient='index')
        input_data = data.to_numpy()[1:,0]
        predicted_result = m.run(input_data, "predict")
        json_to_send = {}
        json_to_send['model'] = m.tag
        json_to_send['input_data'] = i_json
        json_to_send['predicted_result'] = predicted_result['result']
        json_to_send = bytes(json.dumps(json_to_send), encoding='utf-8')
        print(json_to_send)
        kafka_producer.send(environ["KAFKA_TOPIC"], json_to_send)