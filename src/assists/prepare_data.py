import csv
import numpy as np

class PrepareData:
    @staticmethod
    def read_data(path):
        with open(path, 'r', encoding="utf-8") as f:
            # get csv parser for annotations file
            gtReader = csv.reader(f, delimiter=',')
            length=len(next(gtReader))
            prices=[]
            for i in range(length):
                price=[]
                f.seek(0)
                for row in gtReader:
                    if row[i]=="":
                        continue
                    else:
                        price.append(float(row[i]))
                prices.append(price.copy())
        return np.array(prices)