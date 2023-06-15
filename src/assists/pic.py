import pandas as pd
import matplotlib.pyplot as plt
from configs import configs


class Pic:
    def show(close,buy,sell, show_period=configs.PIC_SHOW_PERIOD):
        index=range(len(buy))
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.scatter(index[-show_period:], buy[-show_period:], label="buy", color='green', marker='^',alpha=1, linewidths=5)
        plt.scatter(index[-show_period:], sell[-show_period:], label="sell", color='red', marker='v',alpha=1, linewidths=5)
        plt.plot(close[-show_period:], label='Close Price', alpha=0.35)
        plt.title('Close Prcie buy & sell Signals')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()