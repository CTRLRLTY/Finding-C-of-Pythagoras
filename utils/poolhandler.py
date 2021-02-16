import os
import mpmath
import multiprocessing as mp

from utils.find_c import __guess_a, get_a,get_table

def pool_handler(n):
    n_cores = os.cpu_count()
    print("[*] Available Cores: ",n_cores)
    try: # Setting batch_size 
        b_index = sys.argv.index("-b") 
        batch_size = int(sys.argv[b_index+1])
    except: batch_size = 1000000
    total = 0
    with mp.Pool() as pool:
        i_candidate = get_table(n)
        print("[*] using batch size: ", batch_size)
        print("[*] using i candidate: ", i_candidate)

        a = __guess_a(1,n) #first check
        while not mpmath.isint(a): #if i=1 is not the answer
            test_ranges = [(total + y * batch_size, total + (y+1) * batch_size) for y in range(n_cores)]
            params = [(i_candidate, n, test_range) for test_range in test_ranges]
            print("=====Testing from {} to {}=====".format(test_ranges[0][0], test_ranges[-1][1]-1))
            for result in pool.imap_unordered(get_a, params):
                if isinstance(result,tuple): 
                    pool.terminate()
                    return [result]
            total += n_cores * batch_size
        return [(1,a)] #this returns only if i=1 is the answer of C

