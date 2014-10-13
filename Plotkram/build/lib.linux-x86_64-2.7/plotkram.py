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
        
class Simulation():
        def __init__(self, ps, pm, length, number, counter):
            self.params = (ps, pm)
            self.length = length
            self.number = number
            self.times = counter
            #TODO Möglichkeit, andere Verteilungen zu berücksichtigen
            # berechne die most likeli params der inv-gauß-Verteilung
            self.mu, self.loc, self.scale = scipy.stats.invgauss.fit(self.times)
            # berechne Momente
            self.mean, self.variance, self.skewness, self.kurtosis = scipy.stats.invgauss.stats(self.mu, self.loc, self.scale, moments='mvsk')

        def __init__ (self, ps, pm):
	    self.params = (ps, pm)
	    self.length = 1
            self.number = 1
            self.times = 1
            self.mu, self.loc, self.scale, self.mean, self.variance, self.skewness, self.kurtosis = 1,1,1,5000000,10000,3,15
            
        def get_moment(self, moment):
	    if moment == "mean":
		return self.mean
	    if moment == "variance":
		return self.variance
	    if moment == "skewness":
		return self.skewness
	    if moment == "kurtosis":
		return self.kurtosis
	    
	    return None
	
def plot_heatmap_from_file(datei, squareroot_num_sim, moment):
    startzeit = time.clock()
    print "plot heatmap " + datei
    with open(datei, 'rb') as daten:
        sim_array = pickle.load(daten)
    
    plot_heatmap(sim_array, squareroot_num_sim, moment)
      
def plot_heatmap(sim_array, squareroot_num_sim, moment):
    print "plot heatmap"
    #print sim_array,len(sim_array)
   # squareroot_num_sim = int(len(sim_array)/2)
    print squareroot_num_sim
    
    if not squareroot_num_sim:
	print "kein squareroot_num_sim"
	return None
    
    print "Moment", moment
    
    to_plot = np.zeros((squareroot_num_sim, squareroot_num_sim))
    
    for i in range(squareroot_num_sim):
	#print '\n'
        for j in range(squareroot_num_sim):
	    if sim_array[i][j]: 
		#print sim_array[i][j].get_moment(moment), 
		#print type(sim_array[i][j])
	        to_plot[i][j] = math.log(sim_array[i][j].get_moment(moment))
	   
	        if sim_array[i][j].get_moment(moment) == 0:
		    print "params + logmoment ", sim_array[i][j].params, ' ', math.log(sim_array[i][j].get_moment(moment))
	    else:
		to_plot[i][j] = None
		print "none"
	
    #print "toplot ", to_plot
    

    fig, ax = plt.subplots() 
    # extent scheint die achsenbeschriftung zu sein
    cax = ax.imshow(to_plot, origin = 'lower', interpolation = "hamming")  
    
    cbar = fig.colorbar(cax)#, ticks=[np.amin(to_plot), 0, np.amax(to_plot)])*
			
   # cbar.ax.set_yticklabels(['< -1', '0', '> 1'])
    # plot it
    plt.show()
                 
# erwartet datei, in der die sim als liste abgespeichert sind           
def plot_file (datei, histogram_separate, histogram_spec, qq_Plot, fit_qq_Plot, num_bins = 50, vergleich= scipy.stats.invgauss):
    print "plot_file " + datei
    with open(datei, 'rb') as daten:
        sim_liste = pickle.load(daten)
        print sim_liste
        print sim_liste[0].times, sim_liste[0].params
    plot(sim_liste, histogram_separate, histogram_spec, qq_Plot, fit_qq_Plot, num_bins, vergleich)

def plot (sim_liste, histogram_separate, histogram_spec, qq_Plot, fit_qq_Plot, num_bins = 50, vergleich= scipy.stats.invgauss):
    startzeit = time.clock()   
    if histogram_spec:
        print "Erstelle Spektrum"
        fig, ax = plt.subplots()
        fig.suptitle("Laenge: "+str(sim_liste[0].length)+" Anz Teilchen: " +str(sim_liste[1].number)) #TODO, gehe hier davon aus, dass gleiche sim-bedingungen vorliegen
        for sim in sim_liste:
            ax.hist(sim.times, num_bins, alpha=0.5, normed = 1, label = str(sim.params) )
       # plt.show()  
        legend = ax.legend(loc='upper right', shadow=True)

    
    # Je Simulation ein Ausgabefenster mit separatem Histogramm/qq-Plot mit gewählten Params/qq mit automatischem Fit 
    number_stats = sum([histogram_separate, qq_Plot, fit_qq_Plot])
    print number_stats
    if histogram_separate or qq_Plot or fit_qq_Plot:
	print "Erstelle separate Dinge"
	for sim in sim_liste:
	    fig = plt.figure(figsize=(4*number_stats, 4))
            gs1 = gridspec.GridSpec(1, number_stats)
            ax_list = [fig.add_subplot(ss) for ss in gs1]
           
	    akt = 0
	    fig.suptitle("ps, pm"+str(sim.params)+str(round(sim.params[0]-sim.params[1],5)), size = 15)
	    if histogram_separate:
		ax_list[akt].hist(sim.times, num_bins)
		ax_list[akt].set_title("Histogramm")
                akt+=1
                
            #print "hist sep", time.clock()-startzeit
	    if qq_Plot:
                sm.qqplot (np.array(sim.times), scipy.stats.norm,  line = 'r', ax=ax_list[akt])
		ax_list[akt].set_title("qq-Plot; norm!! Params: 0.05")
                akt+=1
            #print 'qq 0.05', time.clock()-startzeit
	    if fit_qq_Plot:
		                
                #mu, loc, scale = scipy.stats.invgauss.fit(sim.times)
                #mean, var = scipy.stats.invgauss.stats(mu, loc, scale, moments='mv')
                #print  "params", sim.params, '(mu, loc, scale), mean, var', round(mu, 5), round(loc, 2), round(scale, 2), '\n',  mean, '\n', var
                
                #sm.qqplot (np.array(sim.times), vergleich, fit = True,  line = 'r', ax=ax_list[akt])
		#ax_list[akt].set_title("qq-Plot mit auto Fit")
                #akt+=1 
                sm.qqplot (np.array(sim.times), vergleich, distargs= (sim.mu, ),  line = 'r', ax=ax_list[akt])
		ax_list[akt].set_title("qq-Plot mit mu:" + str(sim.mu))
                akt+=1
            #print "qq plus rechnen", time.clock()-startzeit                

                #fig.subplots_adjust(top=5.85)
            gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95]) 
            print time.clock()-startzeit
            #plt.tight_layout()
    plt.show()    
       

   
   
    '''x = np.linspace(0, 2*np.pi, 400)
    y = np.sin(x**2)

    pylab.subplots_adjust(hspace=0.000)
    number_of_subplots=len(sim_liste)

    for i,v in enumerate(xrange(number_of_subplots)):
        v = v+1
        ax1 = plt.subplot(number_of_subplots,1,v)
        ax1.plot(x,y)'''

def plot_histogram(datei, histogram_separate, histogram_spec, num_bins=1000):
    with open(datei, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter = ";",quoting=csv.QUOTE_NONE)
        #number,length, params = myreader.next()
        liste = []
        # Erstelle Liste, mit der plt.hist umgehen kann
        for row in myreader:
            unterliste = []
            for r in row:
                r2 = float(r)
                unterliste.append(r2)
            liste.append(unterliste)
        # Erstelle Histogramme     
        if histogram_separate:
	    print "erstelle separate histogramme"
            #meine_range= (length, length+ length*(1/min(params)))
            #meine_range = (length, 4*length)
            meine_range = None
            #print meine_range
            figg = plt.figure()
            ax = figg.add_subplot(221)
            n, bins, patches = plt.hist(liste[0], num_bins, range = meine_range, normed=1, alpha=0.5 )
            ax = figg.add_subplot(222)
            n, bins, patches = plt.hist(liste[1], num_bins, range = meine_range, normed=1, alpha=0.5 )
            ax = figg.add_subplot(223)
            n, bins, patches = plt.hist(liste[2], num_bins, range = meine_range, normed=1, alpha=0.5 )
            ax = figg.add_subplot(224)
            n, bins, patches = plt.hist(liste[3], num_bins, range = meine_range, normed=1, alpha=0.5 )
        

        # ein gemeinsames Histogramm aller Datensätze erstellen; entspricht Spektrum
        if histogram_spec:
            #meine_range= (length, length+ length*(1/min(single_params)))
            meine_range = None
            print "Erstelle Spektrum"
            figg = plt.figure()
            for row in liste:
                n, bins, patches = plt.hist(liste, num_bins, normed=1, alpha=0.5 )
                print "Hist erstellt",#, n, bins, patches#,(time.clock()-startzeit)
        plt.show()    

def plot_qq(datei, qq_Plot, fit_qq_Plot, vergleich = scipy.stats.invgauss):
    with open(datei, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter = ";",quoting=csv.QUOTE_NONE)
        liste = []
        # Erstelle Liste wie oben
        for row in myreader:
            unterliste = []
            for r in row:
                r2 = float(r)
                unterliste.append(r2)
            liste.append(unterliste)

    # Und einen qq-Plot erstellen, evtl Parameter zur vergleichsfunktion müssen
    # per Hand eingestellt werden
    if qq_Plot:
        print "erstelle qq-Plot",
        fig = plt.figure()
        ax = fig.add_subplot(221)
        sm.qqplot (np.array(liste[0]), vergleich, distargs= (0.005,),  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[0]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr2",
        ax = fig.add_subplot(222)
        sm.qqplot (np.array(liste[1]), vergleich, distargs= (0.005,),  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[1]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr3",
        ax = fig.add_subplot(223)
        sm.qqplot (np.array(liste[2]), vergleich, distargs= (0.005,),  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[2]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr4",
        ax = fig.add_subplot(224)
        sm.qqplot (np.array(liste[3]), vergleich, distargs= (0.005,),  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[3]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "qqplot erstellt"

    # qq-Plot mit automatischem fit zur Vergleichsfunktion
    if fit_qq_Plot:
        print "erstelle fit-qq-plot", 
        fig = plt.figure()
        ax = fig.add_subplot(221)
        sm.qqplot (np.array(liste[0]), vergleich, fit = True,  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[0]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr2",
        ax = fig.add_subplot(222)
        sm.qqplot (np.array(liste[1]), vergleich, fit = True,  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[1]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr3",
        ax = fig.add_subplot(223)
        sm.qqplot (np.array(liste[2]), vergleich, fit = True,  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[2]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "nr4",
        ax = fig.add_subplot(224)
        sm.qqplot (np.array(liste[3]), vergleich, fit = True,  line = 'r', ax =ax)
        #txt = ax.text(-1.8, 3500, str(params[3]) ,verticalalignment='top')
        #txt.set_bbox(dict(facecolor='k', alpha=0.1))
        print "qqplot erstellt"

    plt.show()

def get_argument_parser():
    p = argparse.ArgumentParser(
        description = "beschreibung")
    p.add_argument("--langerbefehl", "-l", help='hilfe', action='store_true', dest = 'destination')
    p.add_argument("--maskednan", help = "set masked cells to NaN", action = 'store_true', dest = "masked")   
    p.add_argument("inputfile", help = "input file (pickled) to plot a heatmap, n x n Matrix")
    p.add_argument("--moment", "-m" , help = "which moment to plot as heatmap")
    p.add_argument("--single", "-s", help = "plot a single spectrum")
    p.add_argument("--multiple_files", '-mf', action="store_true", help = "read multiple files, each a single spectrum")
    return p

def main():
    p = get_argument_parser()
    args = p.parse_args()
    if args.moment:
	moment = args.moment
	print "moment", moment
        #print "input:", args.inputfile, type(args.inputfile)
        #plot_heatmap_from_file(args.inputfile, 8, moment)
    
    if args.single:
	filename = args.simarray
	
    if args.multiple_files: #TODO: Krücke!
        print "multiple_files"
	schrittweite = 0.00025    
	p1 = np.arange(0.999, 0.99996, schrittweite)
	p2 = np.arange(0.00004, 0.001, schrittweite)
	pss = np.concatenate((p2, p1), axis = 0)
	pss = np.concatenate((pss, [0]), axis =0)
	pms = np.concatenate((p1, p2), axis = 0)
	pms = np.concatenate((pms, [1]), axis =0)
	#print p1, len(p1), p2, len(p2)
	#print "pss ", pss, len(pss), "\n pms ", pms, len(pms)
    
	mySims = np.array([[None]*len(pss)]*len(pms))
	for i in range(len(pss)):
	    for j in range(len(pms)):
		ps = pss[i]
                pm = pms[j]
                
                #print "öffne jetzt", ps, pm,
                try:
		    print "try"
		    with open("Sim_"+str(ps)+"_"+str(pm)+".p", 'rb') as daten:
			#print daten
			aSim = pickle.load(daten)
			print "aSim", type(aSim), aSim
			mySims[i][j] = aSim
		except IOError:
		    mySims[i][j] = Simulation(ps, pm)
		    print "fehler"
        print "alle offen"
        dim1 = 0
        dim2 = 0
        for x in mySims:
	    dim1+=1
	    for y in x:
		dim2 +=1
		print y.get_moment(moment),
	    print '\n '
	print "dim1 ", dim1, " dim2 ", dim2 
	print len(mySims), len(mySims[1])
        plot_heatmap(mySims, dim1, args.moment)   
        print "fertig"
        


if __name__ == "__main__":
    main()
        