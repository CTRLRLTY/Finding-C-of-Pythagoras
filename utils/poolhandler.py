import os
import mpmath
from window import RUN_OUTPUT_WIN
import multiprocessing as mp
from threading import Thread, Event

from utils.find_c import __guess_a, get_a,get_table

PROGRESS_WIN = RUN_OUTPUT_WIN.pop("Progress")
RESULT_WINS = RUN_OUTPUT_WIN.items()
N_CORES = os.cpu_count()
BATCH_SIZE = 0
N = 0

def RUN_OUTPUT_CLEAR():
    for key, WIN in RESULT_WINS:
        WIN.update("")

def RUN_OUTPUT_UPDATE(element_value):
    ctr = 0
    for key, WIN in RESULT_WINS:
        WIN.update(f"{key}: " + str(element_value[ctr]))
        ctr += 1

def get_pool_result(result_pipes, terminate_event):
    for result in result_pipes:
        if isinstance(result, tuple):
            terminate_event.set()
            RUN_OUTPUT_UPDATE(result)
            break
    print(f"RUN_BACKGROUND_RESULT: {result}")

def divide_work(start):
    i_candidate = get_table(N)
    test_ranges = [(start + y * BATCH_SIZE, start + (y + 1) * BATCH_SIZE) for y in range(N_CORES)]
    work_batch = [(i_candidate, N, test_range) for test_range in test_ranges]
    min = test_ranges[0][0]
    max = test_ranges[-1][1] - 1
    return (work_batch,min, max)

def create_thread(pool,start,terminate_event):
    work_batch, min_range, max_range = divide_work(start)

    PROGRESS_WIN.update("Finding from {} to {}".format(min_range, max_range))
    result_pipes = pool.imap_unordered(get_a, work_batch)

    get_pool_result_thread = Thread(target=get_pool_result, args=(result_pipes, terminate_event))
    get_pool_result_thread.start()

    active_thread = get_pool_result_thread
    next_start_range = start + N_CORES * BATCH_SIZE
    return (active_thread,next_start_range)

def pool_handler(n,min_range = 0,batch_size = 1000000, terminate_event = None):
    global BATCH_SIZE
    global N
    N = n
    BATCH_SIZE = batch_size
    RUN_OUTPUT_CLEAR()
    result = (1, *(__guess_a(1, n)))  # first check
    if mpmath.isint(result[-1]): RUN_OUTPUT_UPDATE(result)
    else:
        min_range = min_range - min_range % 10  # set last digit to 0

        get_pool_result_thread = None
        with mp.Pool(N_CORES) as pool:
            print(f"POOL CREATED: {pool}")
            while not terminate_event.is_set():
                terminate_event.wait(1.0)
                there_is_no_thread = not get_pool_result_thread

                if there_is_no_thread:
                   get_pool_result_thread, min_range = create_thread(pool,min_range,terminate_event)
                else:
                    thread_is_inactive = not get_pool_result_thread.is_alive()
                    if thread_is_inactive:
                        get_pool_result_thread, min_range = create_thread(pool,min_range,terminate_event)

            PROGRESS_WIN.update("Finished!")
            pool.terminate()
            print(f"POOL DESTROYED: {pool}")
