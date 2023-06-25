from configs import configs
from assists.prepare_data import PrepareData
from assists.printer import Printer
import numpy as np


class Env:
    @staticmethod
    def make(env_name, data=None, seed=configs.SEED):
        env = Env(env_name, data, seed)
        return env

    def __init__(self, env_name, data=None, seed=configs.SEED, file_path=configs.DATA_PATH_XLSX, start_index=configs.STATE_PERIOD-1):
        self.env_name = env_name
        self.file_path = file_path
        self.index = start_index
        if data is None:
            # as default, we use the first data
            self.data = self.read_data()[0]
        else:
            self.data = data
        self.seed = seed
        self.money = configs.INIT_MONEY
        self.stock = 0
        self.buy_num = 0
        self.sell_num = 0
        self.done = False

    def reset(self):
        self.index = configs.STATE_PERIOD-1
        self.money = configs.INIT_MONEY
        self.stock = 0
        self.buy_num = 0
        self.sell_num = 0
        self.done = False
        return self.get_state()

    def step(self, action):
        # action is a single number, which is less than 1, and greater than -1
        # the action is the percentage of the money to buy the stock or sell the stock
        # if action is positive, then buy the stock
        assert action <= configs.MAX_ACTION and action >= configs.MIN_ACTION

        if self.index == len(self.data)-2:
            self.done = True
        else:
            self.index += 1

        if action > 0 and self.data[self.index] > 0:
            # buy the stock
            transfer_money = min(self.money, self.money*action)
            self.money = float(self.money-transfer_money)
            self.stock = float(self.stock+transfer_money/self.data[self.index])
            self.buy_num += 1
        elif action < 0:
            # sell the stock
            transfer_stock = min(self.stock, self.stock*(-action))
            self.money = float(self.money+transfer_stock*self.data[self.index])
            self.stock = float(self.stock-transfer_stock)
            self.sell_num += 1

        return self.get_state(), self.get_reward(), self.done

    def sample_action(self):
        return np.random.uniform(configs.MIN_ACTION, configs.MAX_ACTION)

    def get_action_dim(self):
        return 1

    def get_state_dim(self):
        return configs.STATE_PERIOD+2

    def get_max_action(self):
        return configs.MAX_ACTION

    def set_seed(self, seed):
        self.seed = seed
        np.random.seed(seed)

    def get_state(self):
        state_money = np.array(
            [self.money/configs.INIT_MONEY, self.stock/configs.STOCK_SCALE])
        state_period = self.data[self.index -
                                 configs.STATE_PERIOD+1:self.index+1]/configs.DATA_SCALE
        return np.concatenate((state_period, state_money))

    def get_reward(self):
        # for avoiding the agent not buy any but always sell to keep the money and achieve a high reward, we add a penalty for selling
        return (self.money+self.stock*self.data[self.index]-configs.INIT_MONEY)/configs.INIT_MONEY-configs.SELL_NUM_SCALE*self.sell_num
        # this is to make the num of buying and the num of selling a balance
        return (self.money+self.stock*self.data[self.index]-configs.INIT_MONEY)/configs.INIT_MONEY+1/((self.buy_num+1)/(self.sell_num+1)+(self.sell_num+1)/(self.buy_num+1))-0.5

    def get_money(self):
        return self.money+self.stock*self.data[self.index]

    def eval_policy(self, policy, eval_episodes=configs.EVAL_EPISODES):
        eval_env = Env.make(self.env_name+"_eval", self.data)
        avg_reward = 0
        for _ in range(eval_episodes):
            state, done = eval_env.reset(), False
            while not done:
                action = policy.select_action(np.array(state))
                state, reward, done = eval_env.step(action)
                avg_reward += reward

        avg_reward /= eval_episodes
        money = eval_env.get_money()

        Printer.print_eval(
            f"evaluation over {eval_episodes} episodes: {avg_reward:.3f} money: {money:.3f}")
        return avg_reward, money

    def read_data(self):
        data = PrepareData.read_data(self.file_path)
        return data
