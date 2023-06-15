import talib
from configs import configs
import numpy as np


class Indexes:
    # 相对强弱指标
    @staticmethod
    def RSI(close_k, periods=configs.RSI_PERIOD):
        return talib.RSI(close_k, periods)
    
    # 异同移动平均线指标
    @staticmethod
    def MACD(close_k, fastperiod=configs.MACD_FASTPEROID, slowperiod=configs.MACD_SLOWPEROID, signalperiod=configs.MACD_SIGNALPEROID):
        macd, signal, hist = talib.MACD(
            close_k, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        return macd, signal, hist
    
    # 平均方向性运动指标
    @staticmethod
    def ADX(high, low, close, timeperiod=14):
        return talib.ADX(high, low, close, timeperiod=timeperiod)
    
    # 停损指标
    @staticmethod
    def SAR(high, low, acceleration=0, maximum=0):
        return talib.SAR(high, low, acceleration=acceleration, maximum=maximum)
    
    # 威廉指标
    @staticmethod
    def WILLR(high, low, close, timeperiod=14):
        return talib.WILLR(high, low, close, timeperiod=timeperiod)
    
    # 随机指标
    @staticmethod
    def KDJ(high, low, close, fastk_period=9, slowk_period=3, slowd_period=3):
        slowk, slowd = talib.STOCH(
            high, low, close, fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
        return slowk, slowd
    
    # 中间意愿指标
    @staticmethod
    def CR(high, low, close, timeperiod=26, type=0):
        M_0=high+low+2*close/4
        M_1=high+low+close/3
        M_2=high+low/2
        M=[M_0,M_1,M_2]
        M=M[type]
        P_1=[0 if i<timeperiod else sum([max(high[i-j]-M[i-j-1],0) for j in range(timeperiod)]) for i in range(len(M))]
        P_2=[0 if i<timeperiod else sum([max(M[i-j-1]-low[i-j],0) for j in range(timeperiod)]) for i in range(len(M))]
        CR= [np.nan if i<timeperiod else 100*P_1[i]/(P_1[i]+P_2[i]) for i in range(len(M))]
        return CR
        
        
