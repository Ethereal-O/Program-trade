import numpy as np
import matplotlib.pyplot as plt
from indexes.indexes import Indexes
from configs import configs
plt.style.use('fivethirtyeight')


class Strategy:
    # method to judge if need buy
    @staticmethod
    def need_buy(macd,signal,rsi):
        return macd > signal and rsi>=configs.RSI_UPPER
    
    # method to judge if need sell
    @staticmethod
    def need_sell(macd,signal,rsi):
        return macd < signal and rsi<=configs.RSI_LOWER
    
    # method to get all signals
    @staticmethod
    def get_buy_sell_signal(high,low,close):
        # get macd signal
        macd, signal, hist=Indexes.MACD(close)
        # get rsi signal
        rsi = Indexes.RSI(close)
        # get adx signal
        adx = Indexes.ADX(high,low,close)
        # get atr signal
        atr = Indexes.ATR(high,low,close)
        # prepare buy and sell signal
        buy = []
        sell = []
        # to avoid not buy anything but to sell, in this case, when we sell, we sell all the stock we have
        if_has_buy = False
        # to avoid buy and sell in a short time
        last_buy_index=configs.BUY_INIT_INDEX
        for i in range(len(close)):
            if Strategy.need_buy(macd[i],signal[i],rsi[i]) and i-last_buy_index>=configs.BUY_SELL_PERIOD:
                # buy here!
                sell.append(np.nan)
                buy.append(close[i])
                last_buy_index=i
                if_has_buy=True
            elif Strategy.need_sell(macd[i],signal[i],rsi[i]) and if_has_buy:
                # sell here!
                buy.append(np.nan)
                sell.append(close[i])
                last_buy_index=configs.BUY_INIT_INDEX
                if_has_buy=False
            else:
                # do nothing
                buy.append(np.nan)
                sell.append(np.nan)
        return buy, sell, rsi, adx, atr
    
    @staticmethod
    def get_all_num(close,predict,buy,sell,rsi,adx,atr,init_money=configs.INIT_MONEY):
        res=[]
        money=init_money
        stock=0
        for i in range(len(close)):
            if not (np.isnan(buy[i]) or np.isnan(rsi[i]) or np.isnan(adx[i])) and money>0:
                # num is selected by rsi and adx
                transfer_money=min(money,money*rsi[i]/adx[i])
                # num is selected by atr
                # transfer_money=money*configs.ATR_RATIO/atr[i]
                money=money-transfer_money
                stock=stock+transfer_money/close[i]
            elif not (np.isnan(sell[i]) or np.isnan(rsi[i]) or np.isnan(adx[i])):
                transfer_money=stock*close[i]
                money=money+transfer_money
                stock=0
                
            res.append(money+stock*close[i])
            
        return res