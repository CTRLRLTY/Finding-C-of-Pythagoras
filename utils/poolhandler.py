import os
import mpmath
from window import RUN_OUTPUT_WIN
import multiprocessing as mp

from utils.find_c import __guess_a, get_a,get_table

PROGRESS_WIN = RUN_OUTPUT_WIN.pop("Progress")
RESULT_WINS = RUN_OUTPUT_WIN.items()

def pool_handler(n: int, batch_size: int) -> None:
    total = 0
    n_cores = os.cpu_count()

    with mp.Pool(n_cores) as pool:
        i_candidate = get_table(n)

        *guess_result,a = __guess_a(1,n) #first check
        while not mpmath.isint(a): #if i=1 is not the answer
            test_ranges = [(total + y * batch_size, total + (y+1) * batch_size) for y in range(n_cores)]
            params = [(i_candidate, n, test_range) for test_range in test_ranges]
            PROGRESS_WIN.update("Finding from {} to {}".format(test_ranges[0][0], test_ranges[-1][1]-1))
            for result in pool.imap_unordered(get_a, params):
                if isinstance(result,tuple):
                    a = result[-1] # Setting the a first so the parent while loop breaks as well
                    ctr = 0
                    for key,WIN in RESULT_WINS:
                        WIN.update(f"{key}: " + str(result[ctr]))
                        ctr += 1
                    pool.terminate()
                    break

            total += n_cores * batch_size
        PROGRESS_WIN.update("Finished!")
        pool.join()
