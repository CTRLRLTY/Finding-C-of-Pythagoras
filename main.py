import multiprocessing as mp
import time
import os
import sys
import mpmath

def get_i(b,target):
    for x in range(10):
        if str(target) in str(b+x)[-1]: return x

def get_table(n):
    identic_table = {
            "1": (1,6,4,9,0,5),
            "3": (2,7,3,8),
            "7": (4,9,1,6),
            "9": (5,0,2,7,3,8)
            }
    b = mpmath.floor(mpmath.sqrt(n))
    _b_ = str(b)[-3] # Getting b' last digit
    _n_ = str(n)[-1] # Getting n last digit

    _n_int = int(_n_)
    _b_int = int(_b_)
    i_candidate = [ get_i(_b_int,target) for target in identic_table[_n_] ]
    
    return i_candidate


def __guess_a(i,n):
    try:
        b = mpmath.floor(mpmath.sqrt(n))
        c = b + i
        c_squared = mpmath.power(c,2)
        a_squared = c_squared - (n)
        a = mpmath.sqrt(a_squared)
        """
        if(i == 3): 
            print("b: ",b)
            print("c: ",c)
            print("c^2: ",c_squared)
            print("a^2: ",a_squared)
            print("a: ",a)
        """
        return a
    except ValueError: #if a value error is determined, return a float
        print("{} ValueError Found. Skipping i: {}".format(mp.current_process().name,i))
        return 1.1 

def get_a(data):
    i_list,n,test_range = data
    for test in range(test_range[0],test_range[1],10):
        temp_list = [test+y for y in i_list]
        for y in temp_list:
            a = __guess_a(y,n)
            if mpmath.isint(a):
                print("+++ {} Found a: {} using i: {}.".format(mp.current_process().name, a,y))
                return (y,a)
    return None

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

        #first check
        a = __guess_a(1,n)
        while not mpmath.isint(a):
            test_ranges = [(total + y * batch_size, total + (y+1) * batch_size) for y in range(n_cores)]
            params = [(i_candidate, n, test_range) for test_range in test_ranges]
            print("=====Testing from {} to {}=====".format(test_ranges[0][0], test_ranges[-1][1]-1))
            for result in pool.imap_unordered(get_a, params):
                if isinstance(result,tuple): 
                    pool.terminate()
                    return [result]
            total += n_cores * batch_size
        return [(1,a)]

def main():
    n = int(input("[Input] enter n (int): "))
    dps = int(input("[Input] enter percision limit (int): "))
    mpmath.mp.dps = dps
    
    start = time.time()
    b = mpmath.floor(mpmath.sqrt(n))
    print("== n: ", n)
    print("== b':",b)
    print("[*] Limiting decimal percision to: ", mpmath.mp.dps)
    

    i,a = pool_handler(n)[0]
    c = b + i
    print("###### FOUND a ######")
    print("** Found a on i: {} **".format(i))
    print("== a value: ", a)
    print("== c + a: {}".format(c + a))
    print("== c - a: {}".format(c - a))
    print("Result found in %d seconds" % (time.time() - start))

if __name__ == "__main__":
    main() 
