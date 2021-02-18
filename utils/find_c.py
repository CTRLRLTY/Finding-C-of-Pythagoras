import mpmath
import multiprocessing as mp
from window import sg
from typing import Union

IPC_DATA = list[tuple]

def get_i(b: int,target: tuple) -> None:
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


def __guess_a(i: int,n: int) -> mpmath.mpf:
    b = mpmath.floor(mpmath.sqrt(n))
    c = b + i
    c_squared = mpmath.power(c,2)
    a_squared = c_squared - (n)
    a = mpmath.sqrt(a_squared)
    return (b,c,c_squared,a_squared,a)

def get_a(data: IPC_DATA) -> Union[tuple,None]:
    i_list,n,test_range = data
    for test in range(test_range[0],test_range[1],10):
        temp_list = [test+y for y in i_list]
        for y in temp_list:
            result = __guess_a(y,n)

            if mpmath.isint(result[-1]): #check if a is int
                deb = (*result,result[1]-result[-1],result[1]+result[-1])
                print(deb)
                print(deb[-3])
                return (y,*result,result[1]-result[-1],result[1]+result[-1]) #return i,b,c,c^2,a^2,a,p,q
                #return (y, *result)
