import time
import mpmath
from window import sg, window
from constant import *
from threading import Thread, active_count as active_thread
from multiprocessing import freeze_support


from utils.poolhandler import pool_handler


def main():
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Run":
            if not values[INPUT_N].isdigit() or not values[INPUT_DPS].isdigit():
                continue
            n = int(values[INPUT_N])
            dps = int(values[INPUT_DPS])
            batch_size = 1000000
            mpmath.mp.dps = dps
            
            if active_thread() < 2: 
                # If the program are not currently finding a c 
                finding_c_thread = Thread(target=pool_handler, args=(n, batch_size))
                if not finding_c_thread.is_alive():
                    finding_c_thread.start()

    window.close()


if __name__ == "__main__":
    freeze_support() #Because windows sucks we have to call this stupid boiler plate
    main()

