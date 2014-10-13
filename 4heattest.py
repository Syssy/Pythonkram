# -*- coding: utf-8 -*-
import scipy.stats
import csv
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pickle
import pylab
import matplotlib.gridspec as gridspec
import time
import simulation
import math
from matplotlib import cm
import argparse        
from matplotlib.pyplot import figure, show, axes, sci
from matplotlib import cm, colors
from matplotlib.font_manager import FontProperties
from numpy import amin, amax, ravel
from numpy.random import rand

    # Set the first image as the master, with all the others
    # observing it for changes in cmap or norm.
class ImageFollower:
    'update image in response to changes in clim or cmap on another image'
    def __init__(self, follower):
        self.follower = follower
    def __call__(self, leader):
        self.follower.set_cmap(leader.get_cmap())
        self.follower.set_clim(leader.get_clim())
        
        
def plot_4_heatmaps(sim_array, num_sim):
    
    print sim_array, num_sim, math.sqrt(num_sim)/2
    scale = int(math.sqrt(num_sim)/2)
    #erstelle to_plots
    sim_array = np.reshape(sim_array, (scale*2, scale*2))
    print sim_array
    plotlist = []
    hilfsliste1 = []
    hilfsliste2 = []
    hilfsliste3 = []
    for i in range (scale):
	hilfsliste1 = []
	for j in range (scale):
	    hilfsliste1.append(sim_array[i][j])
	    #print sim_array[i][j]
	hilfsliste2.append(hilfsliste1)
	#print "hl2", hilfsliste2
    plotlist.append(hilfsliste2)
   
    hilfsliste2 = []
    for i in range (scale):
	hilfsliste1 = []
	for j in range (scale):
	    hilfsliste1.append(sim_array[i+scale][j])
	    #print sim_array[i][j]
	hilfsliste2.append(hilfsliste1)
    plotlist.append(hilfsliste2)
   
    hilfsliste2 = []
    for i in range (scale):
	hilfsliste1 = []
	for j in range (scale):
	    hilfsliste1.append(sim_array[i][j+scale])
	    #print sim_array[i][j]
	hilfsliste2.append(hilfsliste1)
    plotlist.append(hilfsliste2)
   
    hilfsliste2 = []
    for i in range (scale):
	hilfsliste1 = []
	for j in range (scale):
	    hilfsliste1.append(sim_array[i+scale][j+scale])
	    #print sim_array[i][j]
	hilfsliste2.append(hilfsliste1)
    plotlist.append(hilfsliste2)
    print "plotlist ",plotlist
    
    Nr = 2
    Nc = 2

    fig = figure()
    #cmap = cm.cool

    figtitle = 'Multiple images'
   # t = fig.text(0.5, 0.95, figtitle,
#		horizontalalignment='center',
#		fontproperties=FontProperties(size=16))

    cax = fig.add_axes([0.2, 0.08, 0.6, 0.04])

    w = 0.4
    h = 0.32
    ax = []
    images = []
    vmin = 1e40
    vmax = -1e40
    for i in range(Nr):
	for j in range(Nc):
	    print "ij ", i, j
	    pos = [0.075 + j*1.1*w, 0.18 + i*1.2*h, w, h]
	    a = fig.add_axes(pos)
	    if i > 0:
		a.set_xticklabels([])
	    
            data = plotlist[i+j*Nc]

	    print data
	    dd = ravel(data)
	    # Manually find the min and max of all colors for
	    # use in setting the color scale.
	    vmin = min(vmin, amin(dd))
	    vmax = max(vmax, amax(dd))
	    images.append(a.imshow(data, origin = "lower"))
	    ax.append(a)

    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    for i, im in enumerate(images):
	im.set_norm(norm)
	if i > 0:
	    images[0].callbacksSM.connect('changed', ImageFollower(im))

    # The colorbar is also based on this master image.
    fig.colorbar(images[0], cax, orientation='horizontal')

    # We need the following only if we want to run this interactively and
    # modify the colormap:
    axes(ax[0])     # Return the current axes to the first one,
    sci(images[0])  # because the current image must be in current axes.

    show()

def main():
    testarray = np.array([[2,2,2,3,3,3], [2,5,5,5,5,3], [2,5,4,4,5,3], [0,5,4,4,5,1], [0,5,5,5,5,1],[0,0,0,1,1,1]])
    
    testarray = np.reshape (testarray, 36)
    plot_4_heatmaps(testarray, 36)
    
    #fig, ax = plt.subplots()
    #ax.imshow(testarray)
    #plt.show()
    

if __name__ == "__main__":
    main()