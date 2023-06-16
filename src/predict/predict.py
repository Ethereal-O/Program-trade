import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib.pyplot as plt
import numpy as np
from configs import configs

class Predict:
    @staticmethod
    def predict(close):
        return Predict.arima_predict(close)
    
    @staticmethod
    def arima_predict(close):
        # here to diff the close, you should first check if the close is stationary
        diff_times=configs.DIFF_TIMES
        # diff = np.diff(close,n=diff_times)
        # print('diff result:\n', acorr_ljungbox(diff, lags=1))
        # plot_acf(diff)
        # plot_pacf(diff)
        # plt.show()
        model = sm.tsa.arima.ARIMA(close, order=(diff_times,1,1)).fit()
        predict=model.predict(configs.START_PREDICT_INDEX)
        return [0 if i<len(close)-len(predict) else predict[i-len(close)+len(predict)] for i in range(len(close))]

    @staticmethod
    def predict_all(closes):
        return [Predict.predict(close) for close in closes]
