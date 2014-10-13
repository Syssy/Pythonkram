#!/usr/bin/env python
# -*- coding: latin-1 -*- 

import scipy.stats
import pickle
import argparse        

# Speichert alle interessanten Dinge einer Simulation ab
class Simulation():
        def __init__(self, ps, pm, length, number, counter):
            self.params = (ps, pm)
            self.length = length
            self.number = number
            self.times = counter
            #TODO Möglichkeit, andere Verteilungen zu berücksichtigen
            # berechne die most likeli params der inv-gauß-Verteilung
            self.mu, self.loc, self.scale = scipy.stats.invgauss.fit(self.times)
            # berechne Momente unter der Annahme, dass Invgauß vorliegt und per fit gut berechnet wurde
            self.mean, self.variance, self.skewness, self.kurtosis = scipy.stats.invgauss.stats(self.mu, self.loc, self.scale, moments='mvsk')
            print "erstelle Sim mit ppmvsk: ", self.params, self.mean, self.variance, self.skewness, self.kurtosis

        # Gibt den Wert des moment zurück
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
	
	#berechnet die Momente / Parameter Neu
        # Momente werden hier aber direkt, ohne Umweg über Verteilung berechnet
	def recalculate_params(self):
	    self.mu, self.loc, self.scale = scipy.stats.invgauss.fit(self.times)
	    
	def recalculate_moments(self):   
	    #print "mean", self.mean, ' ', 
	    self.mean = np.mean(self.times)
	    #print self.mean
	    #print "var", self.variance, ' ', 
	    self.variance = np.var(self.times)
	    #print self.variance, ' '
	    #print "skew", self.skew, ' ',
	    self.skewness = scipy.stats.skew(self.times)
	    #print self.skewness, ' '
	    #print "kurtosis", self.kurtosis, ' ',
	    self.kurtosis = scipy.stats.kurtosis(self.times)
	    #print self.kurtosis, ' '
	    
# für Kommandozeilentests	    
def get_argument_parser():
    p = argparse.ArgumentParser(
        description = "beschreibung")  
    p.add_argument("--inputfile", "-i", type = str,  help = "input file (pickled)")
    p.add_argument("--moment", "-m" , help = "which moment is of interest")
    p.add_argument("--recalc", "-rc", type=str, help = "recalculate moments")
    p.add_argument("--number", "-n", help = "how many files to recalculate")
    
    return p

# bla, aktuell nur genutzt, um die Momente neu zu berechnen
def main():
    p = get_argument_parser()
    args = p.parse_args()
    if args.recalc == moments:
	for num in range(1,args.number):
	        with open("Sim_"+str(num)+".p") as daten:
	        #print daten
	            aSim = pickle.load(daten)
	            aSim.recalculate_moments()
	           # pickle.dump(daten, aSim)
	            with open("SimNeu_"+str(num)+".p", "wb") as datei:
		        aSim = pickle.dump(aSim, datei)
    
    if args.recalc == params:
	for num in range(1,args.number):
	        with open("Sim_"+str(num)+".p") as daten:
	        #print daten
	            aSim = pickle.load(daten)
	            aSim.recalculate_params()
	           # pickle.dump(daten, aSim)
	            with open("SimNeu_"+str(num)+".p", "wb") as datei:
		        aSim = pickle.dump(aSim, datei)
    
    

if __name__ == "__main__":
    main()