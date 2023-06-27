import pandas as pd
import matplotlib.pyplot as plt
from configs import configs
import seaborn as sns


class Pic:
    @staticmethod
    def show_signal(close, buy, sell, show_period=configs.PIC_SHOW_PERIOD):
        index = range(len(buy))
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.scatter(index[-show_period:], buy[-show_period:],
                    label="buy", color='green', marker='^', alpha=1, linewidths=5)
        plt.scatter(index[-show_period:], sell[-show_period:],
                    label="sell", color='red', marker='v', alpha=1, linewidths=5)
        plt.plot(close[-show_period:], label='Close Price', alpha=0.35)
        plt.title('Close Prcie buy & sell Signals')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()

    @staticmethod
    def show_predict(close, predict, show_period=configs.PIC_SHOW_PERIOD):
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.plot(close[-show_period:], label='Close Price', alpha=0.35)
        plt.plot(predict[-show_period:], label='Predict Price', alpha=0.35)
        plt.title('Close Prcie & Predict Price')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()

    @staticmethod
    def show_money(money, show_period=configs.PIC_SHOW_PERIOD):
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.plot(money[-show_period:], label='Money', alpha=0.35)
        plt.title('Money')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()

    @staticmethod
    def show_all(money, close, show_period=configs.PIC_SHOW_PERIOD):
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.plot(close[-show_period:], label='Close Price', alpha=0.35)
        plt.plot(money[-show_period:], label='Money', alpha=0.35)
        plt.title('Close Prcie & Money')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()

    @staticmethod
    def show_correlation_matrix(correlation_matrix):
        sns.heatmap(correlation_matrix, annot=True, cmap='rainbow',
                    linewidths=1.0, annot_kws={'size': 8})
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.show()
        
    @staticmethod
    def show_reward(reward):
        plt.figure(figsize=configs.PIC_FIGURE_SIZE)
        plt.plot(reward, label='Reward', alpha=0.35)
        plt.title('Reward')
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Reward', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()
