import csv
import numpy as np

class PrepareData:
    @staticmethod
    def read_data(path):
        price=[]
        with open(path, 'r', encoding="utf-8") as f:
            # get csv parser for annotations file
            gtReader = csv.reader(f, delimiter=',')
            for row in gtReader:
                if ','.join(row).split(',')[0]=="":
                    continue
                else:
                    price.append(float(','.join(row).split(',')[0]))
        return np.array(price)