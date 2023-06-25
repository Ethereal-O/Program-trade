from dispatcher.td3_trainer import TD3Trainer
from dispatcher.reporter import Reporter
from configs import configs


def main():
    if configs.MODE == configs.MODE_TRAIN:
        TD3Trainer.start()
    if configs.MODE == configs.MODE_REPORT:
        Reporter.start()


if __name__ == "__main__":
    main()
