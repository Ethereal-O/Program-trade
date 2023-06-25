from assists.prepare_data import PrepareData
from assists.printer import Printer
from strategies.strategies import Strategy
from configs.parser import Parser
from configs import configs
from indexes.indexes import Indexes
from ml.env import Env
from ml.td3 import TD3


class Reporter:
    @staticmethod
    def start():
        # parse configs
        report_configs = Parser.parse_report_configs()

        # check data
        if (not PrepareData.check_data(configs.DATA_PATH_SELECT_XLSX)) or report_configs.force_select_data:
            Printer.print_warn(
                "data file not exist or force to regenerate selected data")
            Printer.print_step(0.1, "reading all data...")
            data, header = PrepareData.read_data(
                configs.DATA_PATH_XLSX, header=True)
            Printer.print_step(0.2, "selecting data...")
            selected_indexes = Strategy.select_data(data)
            Printer.print_step(0.3, "writing selected data...")
            data = PrepareData.write_selected_data(
                configs.DATA_PATH_SELECT_XLSX, data, header, selected_indexes)
        else:
            Printer.print_step(0, "reading selected data...")
            data = PrepareData.read_selected_data(
                configs.DATA_PATH_SELECT_XLSX)

        Printer.print_other(
            "read data finished! get data with shape: %s" % (data.shape,))

        # get moneys
        moneys = []
        for i in range(len(data)):
            # first check path
            if not PrepareData.check_data(report_configs.model_path+str(i)+"/"):
                Printer.print_error("please run train first!")
                return
            # create env and make dirs
            Printer.print_step(i+1+0.1, "creating env...")
            eval_env = Env.make(report_configs.env_name,
                                data[i][report_configs.train_test_split:])
            # create policy
            Printer.print_step(i+1+0.2, "creating policy...")
            state_dim = eval_env.get_state_dim()
            action_dim = eval_env.get_action_dim()
            max_action = float(eval_env.get_max_action())
            kwargs = {
                "state_dim": state_dim,
                "action_dim": action_dim,
                "max_action": max_action
            }
            policy = TD3(**kwargs)
            policy.load(report_configs.model_path+str(i) +
                        "/"+report_configs.file_name)
            moneys.append(eval_env.eval_policy(policy)[1])

        # get markowitz
        Printer.print_step(i+2, "getting markowitz...")
        weights = Indexes.get_markowitz(data)

        # get final money
        Printer.print_step(i+3, "getting final money...")
        final_money = Strategy.caculate_money(moneys, weights)

        Printer.print_other("begin money %s, final money %s, earn rate %s" % (
            configs.INIT_MONEY, final_money, final_money/configs.INIT_MONEY))
