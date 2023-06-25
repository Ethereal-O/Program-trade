from configs import configs
import argparse


class Train_configs:
    def __init__(self):
        self.force_select_data = configs.FORCE_SELECT_DATA
        self.data_path = configs.DATA_PATH_SELECT_XLSX
        self.env_name = configs.DEFAULT_ENV_NAME
        self.seed = configs.SEED
        self.start_timesteps = configs.START_TIMESTEPS
        self.eval_freq = configs.EVAL_FREQ
        self.max_timesteps = configs.MAX_TIMESTEPS
        self.expl_noise = configs.EXPL_NOISE
        self.batch_size = configs.BATCH_SIZE
        self.discount = configs.DISCOUNT
        self.tau = configs.TAU
        self.policy_noise = configs.POLICY_NOISE
        self.noise_clip = configs.NOISE_CLIP
        self.policy_freq = configs.POLICY_FREQ
        self.save_model = configs.SAVE_MODEL
        self.load_model = configs.LOAD_MODEL
        self.model_path = configs.MODEL_PATH
        self.result_path = configs.RESULT_PATH
        self.file_name = configs.FILE_NAME
        self.train_test_split = configs.TRAIN_TEST_SPLIT


class Report_configs:
    def __init__(self):
        self.force_select_data = configs.FORCE_SELECT_DATA
        self.env_name = configs.DEFAULT_ENV_NAME
        self.train_test_split = configs.TRAIN_TEST_SPLIT
        self.model_path = configs.MODEL_PATH
        self.file_name = configs.FILE_NAME


class Parser:
    @staticmethod
    def parse_default_train_configs():
        return Train_configs()

    @staticmethod
    def parse_train_configs():
        train_configs = Parser.parse_default_train_configs()
        parser = argparse.ArgumentParser()
        parser.add_argument("--force_select_data",
                            default=train_configs.force_select_data)
        parser.add_argument("--data_path", default=train_configs.data_path)
        parser.add_argument("--env_name", default=train_configs.env_name)
        parser.add_argument("--seed", default=train_configs.seed, type=int)
        parser.add_argument("--start_timesteps",
                            default=train_configs.start_timesteps, type=int)
        parser.add_argument(
            "--eval_freq", default=train_configs.eval_freq, type=int)
        parser.add_argument("--max_timesteps",
                            default=train_configs.max_timesteps, type=int)
        parser.add_argument("--expl_noise", default=train_configs.expl_noise)
        parser.add_argument(
            "--batch_size", default=train_configs.batch_size, type=int)
        parser.add_argument("--discount", default=train_configs.discount)
        parser.add_argument("--tau", default=train_configs.tau)
        parser.add_argument(
            "--policy_noise", default=train_configs.policy_noise)
        parser.add_argument("--noise_clip", default=train_configs.noise_clip)
        parser.add_argument(
            "--policy_freq", default=train_configs.policy_freq, type=int)
        parser.add_argument("--save_model", default=train_configs.save_model)
        parser.add_argument("--load_model", default=train_configs.load_model)
        parser.add_argument("--model_path", default=train_configs.model_path)
        parser.add_argument("--result_path", default=train_configs.result_path)
        parser.add_argument("--file_name", default=train_configs.file_name)
        parser.add_argument("--train_test_split",
                            default=train_configs.train_test_split)
        args = parser.parse_args()
        train_configs.force_select_data = args.force_select_data
        train_configs.data_path = args.data_path
        train_configs.env_name = args.env_name
        train_configs.seed = args.seed
        train_configs.start_timesteps = args.start_timesteps
        train_configs.eval_freq = args.eval_freq
        train_configs.max_timesteps = args.max_timesteps
        train_configs.expl_noise = args.expl_noise
        train_configs.batch_size = args.batch_size
        train_configs.discount = args.discount
        train_configs.tau = args.tau
        train_configs.policy_noise = args.policy_noise
        train_configs.noise_clip = args.noise_clip
        train_configs.policy_freq = args.policy_freq
        train_configs.save_model = args.save_model
        train_configs.load_model = args.load_model
        train_configs.model_path = args.model_path
        train_configs.result_path = args.result_path
        train_configs.file_name = args.file_name
        train_configs.train_test_split = args.train_test_split
        return train_configs

    @staticmethod
    def parse_default_report_configs():
        return Report_configs()

    @staticmethod
    def parse_report_configs():
        report_configs = Parser.parse_default_report_configs()
        parser = argparse.ArgumentParser()
        parser.add_argument("--force_select_data",
                            default=report_configs.force_select_data)
        parser.add_argument("--env_name", default=report_configs.env_name)
        parser.add_argument("--train_test_split",
                            default=report_configs.train_test_split)
        parser.add_argument("--model_path", default=report_configs.model_path)
        parser.add_argument("--file_name", default=report_configs.file_name)
        args = parser.parse_args()
        report_configs.force_select_data = args.force_select_data
        report_configs.env_name = args.env_name
        report_configs.train_test_split = args.train_test_split
        report_configs.model_path = args.model_path
        report_configs.file_name = args.file_name
        return report_configs
