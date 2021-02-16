import time
import mpmath
import PySimpleGUI as sg

from utils.poolhandler import pool_handler



def main():
    n = int(input("[Input] enter n (int): "))
    dps = int(input("[Input] enter percision limit (int): "))
    mpmath.mp.dps = dps
    
    b = mpmath.floor(mpmath.sqrt(n))
    print("== n: ", n)
    print("== b':",b)
    print("[*] Limiting decimal percision to: ", mpmath.mp.dps)
    

    start = time.time() # Begin countdown
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
