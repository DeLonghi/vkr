# Standard library imports
# from kafka import KafkaProducer
# from kafka.errors import KafkaError

from abc import abstractmethod
from threading import Thread
from itertools import cycle
import pandas as pd
import time
import json
import sys
import json

class Broadcast(Thread):
    """Метакласс, описывающий общее поведение и структуру всех Broadcast методов"""

    buffer: pd.DataFrame  # Буфер входных значений из csv
    json: dict  # json строка для отправки в топик

    def __init__(self):
        Thread.__init__(self)
        self.json = {}
        # self.producer = KafkaProducer(bootstrap_servers=['localhost:29092'], api_version=(0, 10, 2), request_timeout_ms=10)


    @abstractmethod
    def _preprocess_data(self):
        pass

    @abstractmethod
    def run(self):
        pass


class ModelBroadcast(Broadcast):

    def __init__(self, delay, data_file):
        self.buffer = pd.read_csv(data_file)
        Broadcast.__init__(self)
        self.delay = delay

        # На первое время хардкодим и предполагаем что поток один. Также предполагаем что данне в csv для одного потока.
        # Итератор по буферу
        self._iterator = cycle(self.buffer.index)

    def _preprocess_data(self):
        ti = self._iterator.__next__()
        res = self.buffer.loc[ti]
        res = res.dropna().to_json()
        return bytes(json.dumps(res), encoding='utf-8')

    def run(self):
        while True:
            start = time.time()
            json_to_send = self._preprocess_data()
            # self.producer.send("mytopic", json_to_send)
            sys.stdout.buffer.write(json_to_send)
            sys.stdout.write("\n")
            sys.stdout.flush()
            time.sleep(self.delay - ((time.time() - start) % self.delay))
