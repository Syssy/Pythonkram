#!/usr/bin/env python
# -*- coding: latin-1 -*- 

import scipy.stats
import pickle
import logging
import argparse     
import numpy as np
import time
import matplotlib.pyplot as plt

# Speichert alle interessanten Dinge einer Simulation ab
class Simulation():
    versionsnummer = 5.0
    
    def __init__(self, ps, pm, length, number, counter = [], pd = (), v = versionsnummer):
        self.params = (ps, pm)
        self.length = length
        self.number = number
        if counter:
            self.times = counter
            #TODO Möglichkeit, andere Verteilungen zu berücksichtigen
            # berechne die most likeli params der inv-gauß-Verteilung
            #self.mu, self.loc, self.scale = scipy.stats.invgauss.fit(self.times)
            # berechne Momente unter der Annahme, dass Invgauß vorliegt und per fit gut berechnet wurde
            #self.mean, self.variance, self.skewness, self.kurtosis = scipy.stats.invgauss.stats(self.mu, self.loc, self.scale, moments='mvsk')
            #print "erstelle Sim mit ppmvsk: ", self.params, self.mean, self.variance, self.skewness, self.kurtosis
            self.mean = np.mean(self.times)
            self.variance = np.var(self.times)
            #print "..", self.times
            self.skewness = scipy.stats.skew(self.times)
            #print "sk"
            self.kurtosis = scipy.stats.kurtosis(self.times)
        # peakdata of form: ((loc,scale),width,height)
        if pd:
            self.pd = pd
        self.version = v


    def simulate_step(self, location, mobile_state, number):
        """Simuliere einen Schritt für alle Teilchen.
        
        ps, pm -- Wahrscheinlichkeit stationaer/mobil zu bleiben
        (new_)location -- np-array aller Orte vor bzw. nach diesem Aufruf
        (new_)mobile_state -- np-array aller Teilchenzustaende vor bzw. nach diesem Aufruf
        number -- Anzahl der zu simulierenden Teilchen, ungleich self.number, da es am Ende weniger werden
        """
        zzv = np.random.random(number)
        zzv2 = zzv < self.params[0]
        zzv3 = zzv < self.params[1]
        logging.log(10, zzv[0:10])
        logging.log(10, zzv2[0:10])
        logging.log(10, zzv3[0:10])
        #berechne neuen Zustand für die Teilchen    
        # entweder: vorher mobil und bleibe es (zzv3, pm)
        # oder: war nicht mobil und bleibe nicht (invertiert zu oder)
        new_mobile_state =  np.bitwise_or(np.bitwise_and(mobile_state, zzv3), (np.invert(np.bitwise_or(mobile_state, zzv2))))
        # wenn mobil, addiere 200 zum Ort; Festlegung auf 0.2mm mitte November 2014
        new_location = location + (200 * new_mobile_state)
        logging.log(10, location[0:10])
        logging.log(10, new_location[0:10])
        logging.log(10, mobile_state[0:10])
        logging.log(10, new_mobile_state[0:10])
        return new_location, new_mobile_state

        # simuliert für ps und pm alle teilchen
    def simulate(self):
        """Hauptschleife, Simuliere und teste, ob fertig."""
        startzeit = time.clock()
        arrival_counter = []
        time_needed = 0
        number = self.number
        
        location = np.zeros(number)
        mobile_state = np.array([True]*number)
    
        #Teil 1: Sim bis Länge, hier muss noch keine Abbruchbed. getestet werden
        while time_needed < self.length/20000000:
            location, mobile_state = self.simulate_step(location, mobile_state, number)
            time_needed += 0.00001
            logging.log(10, time_needed)
        #time.sleep(2)
        # Zeit soll hier 1/10s sein
        logging.log(24, "Teil1 vorbei, zeit:%s, simdauer:%s", time_needed, time.clock()-startzeit)
        logging.log(19, location[0:10])
        #Teil 2: Ab jetzt können Teilchen fertig sein, teste erst, dann x neue Runden
        while True:
            # d ist bitmaske aller aktuell angekommenen Teilchen
            d = location < self.length
            logging.log(10, location)
            logging.log(15, d[0])
            logging.log(15, "in der trueschleife, zeit: %s", time_needed)
            # die beiden aktualisieren (rauswerfen aller fertigen teilchen)
            location = location[d]
            mobile_state = mobile_state[d]   
            #zähle (suminvert...) wie viele schon durch, hänge deren zeitenen an
            for j in range(np.sum(np.invert(d))):
                arrival_counter.append(time_needed)

            # alle teilchen angekommen :) oder Simulation dauert schon zu lange :(
            number = len(location)
            if number < 1:
                logging.log(25, "fertig, simzeit: %s, realtime: %s", time_needed, (time.clock()-startzeit))
                break
            if time_needed > 240:
                logging.log(25, "dat bringt nix, %s", (time.clock()-startzeit))
                for j in range(len(location)):
                    arrival_counter.append(time_needed+100)
                break    
            
            # Damit es schneller geht, nach je x schritten nur testen
            for x in range (1000):
                location, mobile_state = self.simulate_step(location, mobile_state, number)
                time_needed+=0.00001
        
        #print time.clock()-startzeit
        self.times = arrival_counter


    def set_pd(self, pd, v = versionsnummer):
            self.pd = pd
            self.version = v

    def __repr__(self):
            return str(self.params)
        
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
    neueSim = Simulation(0.99, 0.1, 200000, 1000, [])
    neueSim.simulate()
    #print (neueSim, neueSim.times)
    n, bins, patches = plt.hist(neueSim.times, 50, normed=1, alpha=0.5)
    plt.show()
       
    '''if args.recalc == args.moment:
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
            aSim = pickle.dump(aSim, datei)'''
    
    

if __name__ == "__main__":
    logging.basicConfig(level=20)
    main()
