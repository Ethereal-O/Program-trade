import csv
import pandas as pd
import numpy as np
from configs import configs
from assists.timer import Timer
import os


class PrepareData:
    @staticmethod
    @Timer.clocker
    def read_data(path, type="xlsx", header=False):
        if type == "csv":
            return PrepareData.read_data_csv(path, header)
        else:
            return PrepareData.read_data_xlsx(path, header)

    @staticmethod
    @Timer.clocker
    def read_selected_data(path, type="xlsx", header=False):
        if type == "csv":
            raise NotImplementedError
        else:
            return PrepareData.read_selected_data_xlsx(path, header)

    @staticmethod
    @Timer.clocker
    def write_selected_data(path, data, header, selector, type="xlsx"):
        if type == "csv":
            raise NotImplementedError
        else:
            return PrepareData.write_data_xlsx(path, data, header, selector)

    @staticmethod
    def check_data(path, type="xlsx"):
        if type == "csv":
            raise NotImplementedError
        else:
            return PrepareData.check_data_xlsx(path)

    @staticmethod
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def read_data_csv(path, header):
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
    def read_data_xlsx(path, header):
        # get data
        data = pd.read_excel(path)
        # because the first column is date, so we start from 1
        # and the first two row is the name of the data, the third row is title, so we start from 2
        prices = data.iloc[configs.HEAD_NUM:, configs.INDEX_NUM:]
        if header:
            return np.array(prices.values, dtype=np.float64).T, prices.columns.values
        else:
            return np.array(prices.values, dtype=np.float64).T

    @staticmethod
    def read_selected_data_xlsx(path, header):
        # get data
        data = pd.read_excel(path)
        # as same as read_data_xlsx
        prices = data.iloc[configs.SELECTED_HEAD_NUM:,
                           configs.SELECTED_INDEX_NUM:]
        if header:
            return np.array(prices.values, dtype=np.float64).T, prices.columns.values
        else:
            return np.array(prices.values, dtype=np.float64).T

    @staticmethod
    def check_data_xlsx(path):
        if not os.path.exists(path):
            return False
        else:
            return True

    @staticmethod
    def write_data_xlsx(path, data, header, selector):
        data_selected = np.array(data)[selector].T
        header_selected = np.array(header)[selector]
        write_data = pd.DataFrame(data_selected, columns=header_selected)
        write_data.to_excel(path, index=False)
        return data_selected.T
