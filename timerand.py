from time import clock
import numpy as np
from numpy.random import random as nprand
from random import random as stdrand


def test_std_global(n):
    low = high = 0
    for i in range(n):
        x = stdrand()
        if x < 0.5:
            low += 1
        else:
            high +=1
    return (low, high)


def test_np_global(n):
    low = high = 0
    for i in range(n):
        x = nprand()
        if x < 0.5:
            low += 1
        else:
            high +=1
    return (low, high)


def _test_loop(n, r):
    low = high = 0
    for i in range(n):
        x = r()
        if x < 0.5:
            low += 1
        else:
            high +=1
    return (low, high)
    

def test_std_local(n):
    return _test_loop(n, stdrand)


def test_np_local(n):
    return _test_loop(n, nprand)


def test_all_np(n):
    r = nprand(n)
    low = np.sum(r<0.5)
    high = n - low
    return (low, high)

def test_np_prefetch_rand_1(n):
    r = nprand(n)
    low = high = 0
    for x in r:
        if x < 0.5:
            low += 1
        else:
            high += 1
    return (low, high)

def test_np_prefetch_rand_2(n):
    r = nprand(n)
    low = high = 0
    q = 0.5
    for i in range(n):
        if r[i] < q:
            low += 1
        else:
            high += 1
    return (low, high)
    

def test_np_prefetch_bool(n):
    low = high = 0
    bools = nprand(n) < 0.5
    for b in bools:
        if b:
            low += 1
        else:
            high += 1
    return (low, high)


def test_np_prefetch_rand_list_direct(n):
    r = nprand(n).tolist()
    low = high = 0
    for x in r:
        if x < 0.5:
            low += 1
        else:
            high += 1
    return (low, high)


def test_np_prefetch_rand_list_range(n):
    r = nprand(n).tolist()
    low = high = 0
    for i in range(n):
        if r[i] < 0.5:
            low += 1
        else:
            high += 1
    return (low, high) 

def main():
    n = 20*1000*1000  # number of random values to draw
    tests = [test_std_global, test_np_global, test_std_local, test_np_local,
             test_np_prefetch_rand_1, test_np_prefetch_rand_2,
             test_np_prefetch_bool, test_all_np,
             test_np_prefetch_rand_list_direct, test_np_prefetch_rand_list_range]
    print("Times are for {} random numbers".format(n))
    for t in tests:
        start = clock()
        result = t(n)
        time = clock() - start
        print("{}: {:.2f} seconds".format(t.__name__, time))


if __name__ == "__main__":
    main()


    
