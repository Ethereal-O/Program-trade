from strategies.strategies import Strategy
from predict.predict import Predict
from assists.prepare_data import PrepareData
from assists.pic import Pic
from indexes.indexes import Indexes
from configs import configs
from assists.process_data import ProcessData
from assists.printer import Printer
from configs import configs

if __name__ == "__main__":
    # read data
    Printer.print_step(1, "reading data...")
    data = PrepareData.read_data(configs.DATA_PATH)
    Printer.print_other(
        "Read data finished! Get data with shape: %s" % (data.shape,))
    # get if need buy and sell
    Printer.print_step(2, "getting if need buy and sell...")
    buys, sells, rsis, adxs, atrs = Strategy.get_all_buy_sell_signal(
        data, data, data)
    # get predict
    Printer.print_step(3, "getting predict...")
    predicts = Predict.predict_all(data)
    # get markowitz
    Printer.print_step(4, "getting markowitz...")
    weights = Indexes.get_markowitz(data)
    # get money
    Printer.print_step(5, "getting moneys...")
    moneys = Strategy.get_all_num(
        data, predicts, buys, sells, rsis, adxs, atrs, weights)
    # collect them all
    final_money, data_sum = ProcessData.collect_data(moneys, data)
    # Pic.show_all(final_money, data_sum)
    # get final money
    Printer.print_other("begin money %s, final money %s, earn rate %s" % (
        configs.INIT_MONEY, final_money[-1], final_money[-1]/configs.INIT_MONEY))
