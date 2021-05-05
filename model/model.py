# Third party import
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
import logging

logging.basicConfig(filename='model.log', level=logging.DEBUG)


class Model:

    def __init__(self, conf):
        self.tag = conf["tag"]
        self.rollwsize = conf["rollwsize"]
        self.history = conf["history"]
        self.future = conf["future"]
        self.model = LinearRegression()

    def _set_from_pkl(self, path):
        self.model = pickle.load(open(path, 'rb'))

    def _w_shift(self, df):
        w_x, w_y = self.history, self.future
        w = w_x + w_y
        D = df.copy(deep=True).to_numpy()
        newlen = D.shape[0] - w
        X = np.zeros((newlen, w, D.shape[1]))
        for i in range(newlen):
            X[i] = D[i:i + w, :]
        X = X.reshape(X.shape[0], -1)
        return X[:, :w_x], X[:, -w_y:]

    def _create_shifted_sets(self, tag, data):
        df = data[[tag]].copy(deep=True).dropna()
        df = df.interpolate()

        w = self.rollwsize
        ma = df.rolling(window=w).mean()
        ma, df = ma.iloc[w:], df.iloc[w:]

        hist, fut = self.history, self.future
        X, Y = self._w_shift(pd.DataFrame(df[tag]))
        X = np.column_stack((X, ma.to_numpy()[:-(hist + fut), 0].reshape(-1, 1)))
        # TODO: Встроить сюда cross-validation чтобы оценивать качество построенной модели
        return X, Y

    def run(self, data, mode):
        if mode == 'fit':
            logging.info(f"tag {self.tag} FIT")
            # Считываем данные для обучения из excel файла
            data = pd.read_excel("fitdata.xlsx", skiprows=0).sort_values('date').reset_index(drop=True)
            data = data.drop('date', axis=1).apply(pd.to_numeric, errors='coerce')

            # Подготоваливаем массивы из временных рядов
            x, y = self._create_shifted_sets(self.tag, data)

            # Фитим и сохраняем модель
            self.model.fit(x, y)
            pickle.dump(self.model, open(f"pkl/{self.tag}.pkl", 'wb'))
            ret = {"score": self.model.score(x, y)}
            logging.info(f"tag {self.tag} FITTED score {self.model.score(x, y)}")
            return ret
        elif mode == 'predict':
            logging.info(f"tag {self.tag} PREDICT: {data}")
            # Подготоваливаем массива,  работает только для одномерных.
            # w = self.rollwsize
            # x = [sum(data[:w])/w]
            # x.extend(data[w:])
            # x = np.array([x])
            # predicted = [i for i in self.model.predict(x)[0]]
            predicted = self.model.predict(data)
            logging.info(f"tag {self.tag} PREDICTED: {predicted}")
            ret = {"result": predicted}
        return ret
