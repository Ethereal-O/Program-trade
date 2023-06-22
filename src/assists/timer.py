import time
from assists.printer import Printer


class Timer:
    @staticmethod
    def clocker(func):
        def new_func(*arg, **kwargs):
            clock_start = time.time()
            val = func(*arg, **kwargs)
            clock_end = time.time()
            Printer.print_clock("clock start at %ss, end at %ss, interval %ss" %
                                (clock_start, clock_end, clock_end-clock_start))
            return val
        return new_func
