import time
import mpmath
from window import sg, window
from constant import *
from threading import Thread, active_count as active_thread
from multiprocessing import freeze_support


from utils.poolhandler import pool_handler


def main():
    finding_c_thread = None
    while True:
        event, values = window.read(timeout=1)
        print("Active Thread:", active_thread(),end="")
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Run":
            i = 0
            if not values[INPUT_N].isdigit() or not values[INPUT_DPS].isdigit():
                continue
            if values[INPUT_I].isdigit():
                i = int(values[INPUT_I])
            n = int(values[INPUT_N])
            dps = int(values[INPUT_DPS])
            mpmath.mp.dps = dps
            
            if not finding_c_thread or not finding_c_thread.is_alive():
                # If the program are not currently finding a c 
                finding_c_thread = Thread(target=pool_handler, args=(n, i), daemon=True) #Making it a daemon thread so when we close the program, it will terminate child process
                if not finding_c_thread.is_alive():
                    finding_c_thread.start()
        if event == "Stop" and not finding_c_thread: #If stop button is clicked and there's an active finding_c_thread
            pass

        print("")


    window.close()


if __name__ == "__main__":
    freeze_support() #Because windows sucks we have to call this stupid boiler plate
    main()

