# this is the config file for the project
# below are some initial configs for the project
# such as the peroids of the indicators

# For indicators
MACD_FASTPEROID = 12
MACD_SLOWPEROID = 26
MACD_SIGNALPEROID = 9
RSI_PERIOD = 14
ADX_PERIOD = 14
WILLR_PERIOD = 14
KDJ_FASTK_PERIOD = 9
KDJ_SLOWK_PERIOD = 3
KDJ_SLOWD_PERIOD = 3
ATR_PERIOD = 14
CR_PERIOD = 26

# For pic
PIC_SHOW_PERIOD = 2000
PIC_FIGURE_SIZE = (16, 8)

# For data
DATA_PATH_CSV = "./data/data.csv"
DATA_PATH_XLSX = "./data/data.xlsx"
DATA_PATH_SELECT_XLSX = "./data/data_select.xlsx"
SELECTED_DATA_NUM = 20
FORCE_SELECT_DATA = False
HEAD_NUM = 2
SELECTED_HEAD_NUM = 0
INDEX_NUM = 1
SELECTED_INDEX_NUM = 0

# For strategy
RSI_UPPER = 60
RSI_LOWER = 40
BUY_SELL_PERIOD = 30
BUY_INIT_INDEX = -100
INIT_MONEY = 10000
ATR_RATIO = 100
MIN_DATA_ACCECPT_NUM = 30

# For predict
DIFF_TIMES = 2
START_PREDICT_INDEX = 50

# For env
DEFAULT_ENV_NAME = "ENV_DEFAULT"
STATE_PERIOD = 5
EVAL_EPISODES = 10
MIN_ACTION = -1
MAX_ACTION = 1
DATA_SCALE = 10000
STOCK_SCALE = 10
SELL_NUM_SCALE = 0.1

# For train
SEED = 0                    # Sets Gym, PyTorch and Numpy seeds
START_TIMESTEPS = 100       # Time steps initial random policy is used
EVAL_FREQ = 300             # How often (time steps) we evaluate
MAX_TIMESTEPS = 10000       # Max time steps to run environment
EXPL_NOISE = 0.01           # Std of Gaussian exploration noise
BATCH_SIZE = 5              # Batch size for both actor and critic
DISCOUNT = 0.99             # Discount factor
TAU = 0.005                 # Target network update rate
POLICY_NOISE = 0.01         # Noise added to target policy during critic update
NOISE_CLIP = 0.01           # Range to clip target policy noise
POLICY_FREQ = 2             # Frequency of delayed policy updates
SAVE_MODEL = True           # Save model and optimizer parameters
LOAD_MODEL = False          # Load model and optimizer parameters
MODEL_PATH = "./results/ml/models/"
RESULT_PATH = "./results/ml/results/"
FILE_NAME = "TD3_"+DEFAULT_ENV_NAME
TRAIN_TEST_SPLIT = 1000

# For mode
MODE_TRAIN = "train"
MODE_REPORT = "report"
# MODE = MODE_TRAIN
MODE = MODE_REPORT
