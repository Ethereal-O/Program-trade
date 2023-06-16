from strategies.strategies import Strategy
from predict.predict import Predict
from assists.prepare_data import PrepareData
from assists.pic import Pic
from indexes.indexes import Indexes
from configs import configs

if __name__=="__main__":
    data=PrepareData.read_data(configs.DATA_PATH)
    # get if need buy and sell
    buy,sell,rsi,adx,atr=Strategy.get_buy_sell_signal(data,data,data)
    # Pic.show_signal(data,buy,sell)
    predict=Predict.predict(data)
    # Pic.show_predict(data,predict)
    money=Strategy.get_all_num(data,predict,buy,sell,rsi,adx,atr)
    # Pic.show_money(res)
    Pic.show_all(money,data,predict)
    # get final money
    print(money[-1])