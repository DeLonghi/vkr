import json

from db_handlers import DB_Saver, Database
from kafka import KafkaConsumer

environ = dict(DB_USER="postgres", DB_PASS="postgres", DB_HOST="localhost", DB_PORT="5432", DB_NAME="postgres",
               KAFKA_TOPIC="mytopic_consumer", KAFKA_HOST="localhost:29092")

class Receiver:
    """Метакласс, описывающий общее поведение и структуру всех Broadcast методов"""

    def __init__(self, models):
        self.models = models
        self.database = Database()
        params = dict(bootstrap_servers=[environ["KAFKA_HOST"]], auto_offset_reset='latest', api_version=(0, 10),
                      max_partition_fetch_bytes=107374182, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.kafka_topic = environ["KAFKA_TOPIC"]
        self.kafka_consumer = KafkaConsumer(self.kafka_topic, **params)

    def run(self):
        while True:
            for message in self.kafka_consumer:
                values = message.value
                print(values)
                DB_Saver(message=values, database=self.database).run()