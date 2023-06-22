
class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[106m'
    OKGREEN = '\033[102m'
    WARNING = '\033[105m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Printer:
    @staticmethod
    def print_step(step, message):
        print(f"{Bcolors.OKGREEN}[Step %s]{Bcolors.ENDC} {Bcolors.OKBLUE}%s{Bcolors.ENDC}" % (
            step, message))

    @staticmethod
    def print_clock(message):
        print(f"{Bcolors.WARNING}[Clock]{Bcolors.ENDC} {Bcolors.OKBLUE}%s{Bcolors.ENDC}" % (
            message))

    @staticmethod
    def print_other(message):
        print(f"{Bcolors.OKCYAN}[Other]{Bcolors.ENDC} {Bcolors.OKBLUE}%s{Bcolors.ENDC}" % (
            message))
