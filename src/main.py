from strategies.strategies import Strategy
from predict.predict import Predict
from assists.prepare_data import PrepareData
from assists.pic import Pic
from indexes.indexes import Indexes
from configs import configs
import numpy as np

if __name__=="__main__":
    data=PrepareData.read_data(configs.DATA_PATH)
    # get if need buy and sell
    buys,sells,rsis,adxs,atrs=Strategy.get_all_buy_sell_signal(data,data,data)
    # get predict
    predicts=Predict.predict_all(data)
    # get markowitz
    weights=Indexes.get_markowitz(data)
    # get money
    moneys=Strategy.get_all_num(data,predicts,buys,sells,rsis,adxs,atrs,weights)
    # get final money
    final_money=np.sum(moneys,axis=0)
    # Pic.show_all(final_money,data[0])
    # get final money
    print(final_money[-1])