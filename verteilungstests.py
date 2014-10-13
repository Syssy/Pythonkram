import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.stats as stats
import plotkram
import simulation
import pickle
import statsmodels.api as sm
import random
import time

spannen = []

anzahl = 100000

zeit = time.clock()

for i in range(anzahl):
    zz = 0
    zeitspanne = 0
    while zz <= 0.999:
	    zz = random.random()
	    zeitspanne += 1
    spannen.append(zeitspanne)
       
#print spannen 
n, bins, patches = plt.hist(spannen, 70, normed=1, alpha=0.5 )

print time.clock()-zeit
zeit = time.clock()

spannen = scipy.stats.geom.rvs(0.001, size = anzahl)
#print list(spannen)

n, bins, patches = plt.hist(spannen, 70, normed=1, alpha=0.5 )

print time.clock()-zeit

#sm.qqplot(np.array(spannen), scipy.stats.geom, fit = True,  line = 'r')

plt.show()