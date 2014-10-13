import numpy as np
import random
import time
import timeit

mobil = True
x = 1000*10000

def test_1(x):
    starttime = time.clock()
    for i in range(x):
        zz = random.random()
        if zz>0.5:
            mobil = False
        else:
            mobil = True

def test_2(x):
    starttime = time.clock()
    r = random.random
    for i in range(x):
        zz = r()
        if zz>0.5:
            mobil = False
        else:
            mobil = True

def test_3(x):
    starttime = time.clock()
    y2 = np.random.random(x)
    for i in range(x):
        if y2[i]>0.5:
            mobil = False
        else:
            mobil = True

def test_4(x):
    starttime = time.clock()
    y2 = np.random.random(x)
    for i in range(x):
        if y2.item(i)>0.5:
            mobil = False
        else:
            mobil = True

def test_5(x):
    starttime = time.clock()
    y2 = np.random.random(x)
    for y in y2:
        if y > 0.5:
            mobil = False
        else:
            mobil = True
    
def test_6(x):
    starttime = time.clock()
    y2 = np.random.random(x)
    mobil = y2>0.5


print min((timeit.repeat("test_1(zahl)", setup= "from __main__ import test_1; zahl = 100000", number=1000)))
print min((timeit.repeat("test_2(zahl)", setup= "from __main__ import test_2; zahl = 100000", number=1000)))
print min((timeit.repeat("test_3(zahl)", setup= "from __main__ import test_3; zahl = 100000", number=1000)))
print min((timeit.repeat("test_4(zahl)", setup= "from __main__ import test_4; zahl = 100000", number=1000)))
print min((timeit.repeat("test_5(zahl)", setup= "from __main__ import test_5; zahl = 100000", number=1000)))
print min((timeit.repeat("test_6(zahl)", setup= "from __main__ import test_6; zahl = 100000", number=1000)))
