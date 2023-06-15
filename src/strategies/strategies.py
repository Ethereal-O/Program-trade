import numpy as np
import matplotlib.pyplot as plt
from indexes.indexes import Indexes
import configs.configs
plt.style.use('fivethirtyeight')


class Strategy:
    @staticmethod
    def get_buy_sell_signal(high,low,close):
        # get macd signal
        macd, signal, hist=Indexes.MACD(close)
        rsi = Indexes.RSI(close)
        

        buy = []
        sell = []
        flag = -1
        itmp=-100
        for i in range(0, len(signal)):
            if macd[i] > signal[i] and rsi[i]>=60:
                if i-itmp>=30:
                    sell.append(np.nan)
                    # 买入信号
                    buy.append(close[i])
                    itmp=i
                    flag=0
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
            elif macd[i] < signal[i] and rsi[i]<=40:
                if flag==0:
                    buy.append(np.nan)
                # 卖出信号
                    sell.append(close[i])
                    itmp=-100
                    flag=-1
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
                
        return buy, sell