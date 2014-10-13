import numpy as np
import random
import time

mobil = True
x = 1000*10000


starttime = time.clock()
for i in range(x):
    zz = random.random()
    if zz>0.5:
        mobil = False
    else:
        mobil = True
print ("zeit: ", time.clock()-starttime, " einzelne random.random - Aufrufe ")

starttime = time.clock()
r = random.random
for i in range(x):
    zz = r()
    if zz>0.5:
        mobil = False
    else:
        mobil = True
print ("zeit: ", time.clock()-starttime, " einzelne random.random - Aufrufe plus alias")

starttime = time.clock()
y2 = np.random.random(x)
for i in range(x):
    if y2[i]>0.5:
        mobil = False
    else:
        mobil = True
print ("zeit: ", time.clock()-starttime, " NP-Array, Schleife und Zugriff mit [i]")

starttime = time.clock()
y2 = np.random.random(x)
for i in range(x):
    if y2.item(i)>0.5:
        mobil = False
    else:
        mobil = True
print ("zeit: ", time.clock()-starttime, " NP-Array, Schleife und Zugriff mit .item")

starttime = time.clock()
y2 = np.random.random(x)
for y in y2:
    if y > 0.5:
        mobil = False
    else:
        mobil = True
print ("zeit: ", time.clock()-starttime, " Durchlaufen des NP-Array")


starttime = time.clock()
y2 = np.random.random(x)
mobil = y2>0.5
print ("zeit: ", time.clock()-starttime, " Vektor")
