#读入csv文件到列表
import csv
import os

class PrepareData:
    @staticmethod
    def readData(path):
        price=[]
        with open(path, 'r', encoding="utf-8") as f:
            gtReader = csv.reader(f, delimiter=',')  # csv parser for annotations file
            for row in gtReader:
                print(row)
                # if ','.join(row).split(',')[1]=="":
                #     continue
                # else:
                #     price.append(float(','.join(row).split(',')[1]))

        return price