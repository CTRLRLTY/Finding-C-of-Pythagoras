import mpmath
import multiprocessing as mp

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
