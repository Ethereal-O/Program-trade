import numpy as np
import matplotlib.pyplot as plt
import math
from indexes.indexes import Indexes
from configs import configs
from assists.timer import Timer
from deprecated import deprecated
plt.style.use('fivethirtyeight')


class Strategy:
    # method to judge if need buy
    @staticmethod
    def need_buy(macd, signal, rsi):
        return macd > signal and rsi >= configs.RSI_UPPER

    # method to judge if need sell
    @staticmethod
    def need_sell(macd, signal, rsi):
        return macd < signal and rsi <= configs.RSI_LOWER

    # method to get all signals
    @staticmethod
    def get_buy_sell_signal(high, low, close):
        # get macd signal
        macd, signal, hist = Indexes.MACD(close)
        # get rsi signal
        rsi = Indexes.RSI(close)
        # get adx signal
        adx = Indexes.ADX(high, low, close)
        # get atr signal
        atr = Indexes.ATR(high, low, close)
        # prepare buy and sell signal
        buy = []
        sell = []
        # to avoid not buy anything but to sell, in this case, when we sell, we sell all the stock we have
        if_has_buy = False
        # to avoid buy and sell in a short time
        last_buy_index = configs.BUY_INIT_INDEX
        for i in range(len(close)):
            if Strategy.need_buy(macd[i], signal[i], rsi[i]) and i-last_buy_index >= configs.BUY_SELL_PERIOD:
                # buy here!
                sell.append(np.nan)
                buy.append(close[i])
                last_buy_index = i
                if_has_buy = True
            elif Strategy.need_sell(macd[i], signal[i], rsi[i]) and if_has_buy:
                # sell here!
                buy.append(np.nan)
                sell.append(close[i])
                last_buy_index = configs.BUY_INIT_INDEX
                if_has_buy = False
            else:
                # do nothing
                buy.append(np.nan)
                sell.append(np.nan)
        return buy, sell, rsi, adx, atr

    @staticmethod
    @Timer.clocker
    def get_all_buy_sell_signal(highs, lows, closes):
        buys = []
        sells = []
        rsis = []
        adxs = []
        atrs = []
        for i in range(len(closes)):
            buy, sell, rsi, adx, atr = Strategy.get_buy_sell_signal(
                highs[i], lows[i], closes[i])
            buys.append(buy)
            sells.append(sell)
            rsis.append(rsi)
            adxs.append(adx)
            atrs.append(atr)
        return buys, sells, rsis, adxs, atrs

    @staticmethod
    def get_single_num(close, predict, buy, sell, rsi, adx, atr, weight, init_money=configs.INIT_MONEY):
        res = []
        money = init_money
        stock = 0
        for i in range(len(close)):
            if not (np.isnan(buy[i]) or np.isnan(rsi[i]) or np.isnan(adx[i])) and money > 0 and close[i] > 0:
                # num is selected by rsi and adx
                transfer_money = min(money, money*rsi[i]/adx[i])
                # num is selected by atr
                # transfer_money=min(money,money*configs.ATR_RATIO/atr[i])
                money = money-transfer_money
                stock = stock+transfer_money/close[i]
            elif not (np.isnan(sell[i]) or np.isnan(rsi[i]) or np.isnan(adx[i])):
                transfer_money = stock*close[i]
                money = money+transfer_money
                stock = 0

            res.append(money+stock*close[i])

        return res

    @staticmethod
    @deprecated(reason="we will use rl to get num")
    @Timer.clocker
    def get_all_num(closes, predict, buys, sells, rsis, adxs, atrs, weights, init_money=configs.INIT_MONEY):
        res = []
        for i in range(len(closes)):
            res.append(Strategy.get_single_num(
                closes[i], predict[i], buys[i], sells[i], rsis[i], adxs[i], atrs[i], weights[i], init_money*weights[i]))
        return res

    @staticmethod
    def get_reserve_first_zero_index(data):
        for i in range(len(data)-1, -1, -1):
            if data[i] == 0:
                return i
        return -1

    @staticmethod
    def get_all_reserve_first_zero_index(data):
        return [Strategy.get_reserve_first_zero_index(single_data) for single_data in data]

    @staticmethod
    def select_data(data):
        # get all indexes
        buys, sells, rsis, adxs, atrs = Strategy.get_all_buy_sell_signal(
            data, data, data)
        reserve_first_zero_indexs = Strategy.get_all_reserve_first_zero_index(
            data)
        # we just use rsis and adxs to select data
        rsis = [rsi[reserve_first_zero_index+1:] for rsi,
                reserve_first_zero_index in zip(rsis, reserve_first_zero_indexs)]
        adxs = [adx[reserve_first_zero_index+1:] for adx,
                reserve_first_zero_index in zip(adxs, reserve_first_zero_indexs)]
        rsis_devide_adxs = [sum(rsi[np.isfinite(
            rsi)])*sum(adx[np.isfinite(adx)]) for rsi, adx in zip(rsis, adxs)]
        # delete the data which is not good
        rsis_devide_adxs = [index if sum(
            single_data > 0) > configs.MIN_DATA_ACCECPT_NUM else -math.inf for index, single_data in zip(rsis_devide_adxs, data)]
        rsis_devide_adxs = [index if reserve_first_zero_index < configs.MIN_DATA_ACCECPT_SHOP_NUM else -
                            math.inf for index, reserve_first_zero_index in zip(rsis_devide_adxs, reserve_first_zero_indexs)]
        # find first selected_num indexes
        selected_indexes = np.argsort(
            rsis_devide_adxs)[-configs.SELECTED_DATA_NUM:]
        return selected_indexes

    @staticmethod
    def caculate_money(moneys, weights):
        earn = [(money-configs.INIT_MONEY)*weight for money,
                weight in zip(moneys, weights)]
        return sum(earn)+configs.INIT_MONEY
