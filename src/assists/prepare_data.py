import csv
import pandas as pd
import numpy as np
from configs import configs
from assists.timer import Timer


class PrepareData:
    @staticmethod
    @Timer.clocker
    def read_data(path):
        return PrepareData.read_data_xlsx(path)

    @staticmethod
    def read_data_csv(path):
        with open(path, 'r', encoding="utf-8") as f:
            # get csv parser for annotations file
            gtReader = csv.reader(f, delimiter=',')
            length = len(next(gtReader))
            prices = []
            for i in range(length):
                price = []
                f.seek(0)
                for row in gtReader:
                    if row[i] == "":
                        continue
                    else:
                        price.append(float(row[i]))
                prices.append(price.copy())
        return np.array(prices)

    @staticmethod
    def read_data_xlsx(path):
        # get data
        data = pd.read_excel(path)
        # because the first column is date, so we start from 1
        # and the first two row is the name of the data, the third row is title, so we start from 2
        prices = data.iloc[configs.HEAD_NUM:, configs.INDEX_NUM:].values
        return np.array(prices, dtype=np.float64).T
