# Standard library imports
# from flask import Flask, jsonify, request
import warnings
import json
import sys
import os

import pickle

# Local application imports
from model import Model


class AbsIO:

    def __init__(self, conf):
        self._configure()
        self.task_jsn = None
        self.model = Model(conf= conf)

    def _configure(self):
        """ Конфигурирование сервиса """
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
        warnings.filterwarnings("ignore")

    def set_from_pkl(self, path):
        self.model._set_from_pkl(path)

    def _run_as_task(self, model_mode, model_data):
        # HINT: Здесь может быть обертка с асинхронностью
        return self.model.run(model_data, model_mode)

    def run(self):
        print('!!!!!!!!!')
        model_mode, model_data = self.task_jsn["mode"], self.task_jsn.get("data")
        self.task_jsn["data"] = self._run_as_task(model_mode, model_data)
        jsn = json.dumps(self.task_jsn)
        sys.stdout.write(jsn+'\n')
        return jsn


class StdIO(AbsIO):

    def _configure(self):
        super()._configure()

    def run(self):
        while True:
            try:
                self.task_jsn = json.loads(sys.stdin.readline())
                super().run()
            except json.decoder.JSONDecodeError:
                pass
            except KeyboardInterrupt:
                exit()


class FileIO(AbsIO):

    def __init__(self, file_name,conf):
        super().__init__(conf)
        self.file_name = file_name

    def run(self):
        for task_jsn in open(self.file_name, 'r'):
            self.task_jsn = json.loads(task_jsn)
            super().run()

