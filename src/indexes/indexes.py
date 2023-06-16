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
    def ADX(high, low, close, timeperiod=configs.ADX_PERIOD):
        return talib.ADX(high, low, close, timeperiod=timeperiod)
    
    # 停损指标
    @staticmethod
    def SAR(high, low, acceleration=0, maximum=0):
        return talib.SAR(high, low, acceleration=acceleration, maximum=maximum)
    
    # 威廉指标
    @staticmethod
    def WILLR(high, low, close, timeperiod=configs.WILLR_PERIOD):
        return talib.WILLR(high, low, close, timeperiod=timeperiod)
    
    # 随机指标
    @staticmethod
    def KDJ(high, low, close, fastk_period=configs.KDJ_FASTK_PERIOD, slowk_period=configs.KDJ_SLOWK_PERIOD, slowd_period=configs.KDJ_SLOWD_PERIOD):
        slowk, slowd = talib.STOCH(
            high, low, close, fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
        return slowk, slowd
    
    @staticmethod
    def ATR(high, low, close, timeperiod=configs.ATR_PERIOD):
        return talib.ATR(high, low, close, timeperiod=timeperiod)
    
    # 中间意愿指标
    @staticmethod
    def CR(high, low, close, timeperiod=configs.CR_PERIOD, type=0):
        M_0=high+low+2*close/4
        M_1=high+low+close/3
        M_2=high+low/2
        M=[M_0,M_1,M_2]
        M=M[type]
        P_1=[0 if i<timeperiod else sum([max(high[i-j]-M[i-j-1],0) for j in range(timeperiod)]) for i in range(len(M))]
        P_2=[0 if i<timeperiod else sum([max(M[i-j-1]-low[i-j],0) for j in range(timeperiod)]) for i in range(len(M))]
        CR= [np.nan if i<timeperiod else 100*P_1[i]/(P_1[i]+P_2[i]) for i in range(len(M))]
        return CR
        
    @staticmethod
    def get_markowitz(closes):
        # we need assert all closes has same length
        # caculate annualized returns
        annualized_returns = np.array([((close[-1] - close[0]) / close[0]) for close in closes])
        # calculate covariance matrix
        cov_matrix = np.cov(closes)
        # caculate sharpe ratio
        sharpe_ratio = annualized_returns / np.sqrt(np.diag(cov_matrix))
        # calculate optimal weights
        optimal_weights = sharpe_ratio / np.sum(sharpe_ratio)
        return optimal_weights
        
