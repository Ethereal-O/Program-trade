import numpy as np


class ProcessData:
    @staticmethod
    def collect_data(data1, data2):
        data1_collected = np.sum(data1, axis=0)
        data2_collected = np.sum(data2, axis=0)
        return data1_collected, data2_collected
