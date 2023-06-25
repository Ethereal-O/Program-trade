from dispatcher.td3_trainer import TD3Trainer
from dispatcher.reporter import Reporter
from configs import configs


if __name__ == "__main__":
    if configs.MODE == configs.MODE_TRAIN:
        TD3Trainer.start()
    if configs.MODE == configs.MODE_REPORT:
        Reporter.start()
