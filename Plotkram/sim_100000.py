#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Ein Versuch, das zwei-Parameter-Modell umzusetzen
# ps ist Wkeit stationär zu bleiben, wenn ich es schon bin
# pm ist Wkeit mobil zu bleiben, wenn ich es schon bin

import random
import numpy as np
import matplotlib.pyplot as plt
import time
#import statsmodels.api as sm
import scipy.stats as stats
import scipy
#import plotkram
#import simulation
import pickle


# Speichert alle interessanten Dinge einer Simulation ab
class Simulation():
        def __init__(self, ps, pm, length=0, number=0, counter=[0,0,1,0,0]):
            self.params = (ps, pm)
            self.length = length
            self.number = number
            self.times = counter
            #TODO Möglichkeit, andere Verteilungen zu berücksichtigen
            # berechne die most likeli params der inv-gauß-Verteilung
            self.mu, self.loc, self.scale = scipy.stats.invgauss.fit(self.times)
            # berechne Momente
            self.mean = np.mean(self.times)
	    self.variance = np.var(self.times)
	    self.skewness = scipy.stats.skew(self.times)
	    self.kurtosis = scipy.stats.kurtosis(self.times)
	    
	   # print self.times
       
	    
	    
#Simuliert einen Schritt für alle Teilchen
def simulatestep(ps, pm, teilchenort, teilchenmobil):
    number = len(teilchenort)
 
   # print teilchen, number
    zzv = np.random.random(number)
    zzv2 = zzv < ps
    zzv3 = zzv < pm
    
    #berechne neuen Zustand für die Teilchen
    mobilneu =  np.bitwise_or(np.bitwise_and(teilchenmobil, zzv3),(np.invert(np.bitwise_or(teilchenmobil, zzv2))))
    # wenn mobil, addiere 1 zum Ort
    teilchenortneu = teilchenort + mobilneu
    
    return teilchenortneu, mobilneu


# simuliert für ps und pm alle teilchen
def simulate(ps, pm, length, teilchenort, teilchenmobil):
    # Hauptschleife, hier wird simuliert
    startzeit = time.clock()
    #print "Teste jetzt: ", round(ps,6), round (pm,6), '  ',
    hilfscounter = []
    zeit = 0
    
    #Teil 1: Sim bis Länge, hier muss noch keine Abbruchbed. getestet werden
    while zeit < length:
        teilchenort, teilchenmobil = simulatestep(ps, pm, teilchenort, teilchenmobil)
        zeit += 1
    
    print "teil1 fertig", time.clock()-startzeit
    
    #Teil 2: Ab jetzt können Teilchen fertig sein
    while True:
	# Damit es schneller geht, nach je x schritten nur testen
        for x in range (10):
            teilchenort, teilchenmobil = simulatestep(ps, pm, teilchenort, teilchenmobil)
            zeit+=1        

        # d ist bitmaske aller aktuell angekommenen Teilchen
        d = teilchenort <= length
        # die beiden aktualisieren (rauswerfen aller fertigen teilchen)
        teilchenort = teilchenort[d]
        teilchenmobil = teilchenmobil[d]   
        #zähle (suminvert...) wie viele schon durch, hänge deren zeiten an
        for j in range (np.sum(np.invert(d))):
            hilfscounter.append(zeit)
        print ".",
        # alle teilchen angekommen :)
        if len(teilchenort)< 10:
            #print "fertig"
            break

    print time.clock()-startzeit
    return hilfscounter

def main():
    startzeit = time.clock()
    
    # Meine ganzen Variablen, TODO: Soll spaeter mal eingelesen werden
    # Laenge der zu simulierenden Strecke
    length = 100000
    # Anzahl der zu simulierenden Teilchen
    number = 1000000
    
    # Die Parameter (ps, pm) Damit man was zu vergleichen hat, mehrere davon    
    #pss = np.array([0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.9987, 0.9988, 0.9989, 0.999, 0.9991, 0.9992, 0.9993, 0.9994, 0.9995])
    #pms = np.array([0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.9987, 0.9988, 0.9989, 0.999, 0.9991, 0.9992, 0.9993, 0.9994, 0.9995])
    
    #pss=np.array([0.0012, 0.0013, 0.959, 0.9592])
    #pms=np.array([0.0012, 0.0013, 0.959, 0.9592])
    
    #schrittweite = 0.000003
    #p1 = np.arange(0.99988, 0.99995, schrittweite)
    #p2 = np.arange(0.00003, 0.00018, schrittweite)
    #pms = np.concatenate((p1, p2), axis = 0)
    #pss = np.concatenate((p1, p2), axis = 0)
    pss = [0.999898]
    pms = [0.999978]
    print pms, pss
    testarray = np.array([[None]*len(pss)]*len(pms))
    
    for i in range(len(pss)):
        print "\n teste", round(pss[i],6), 'zeit', time.clock()-startzeit, ' '  
        for j in range(len(pms)):
            ps = pss[i]
            pm = pms[j]
            print ps, pm, '(', time.strftime("%d%b%Y_%H:%M:%S"), ') ',
            # Simulationen, die schon vorhanden sind, erst mal nicht neu machen
            # Daher vorher alles .p löschen oder verschieben, wenn neue Version
            mySim = None
            
            speichern = False
            # nur die interessanten, nicht zu lange brauchenden Ecken simulieren
            #if ps < 0.5 or pm > 0.5:
	    #Simulation mit gleichen Params, Länge der Strecke und Anzahl der Teilchen schon vorhanden
            # Also diese einfach übernehmen -> testarray   
	    try:
	        filename = 'Sim_'+ str(round(ps,6)) +'_' +  str(round(pm,6))+ ".p"
	        with open (filename, 'rb') as datei:
		    mySim = pickle.load(datei)
		    #soll nicht sein! Rundungsfehler, Genauigkeit?!
		    if not mySim.params==(round(ps,6), round(pm,6)):
			print "Bullshitkram:", mySim.params, (round(ps,6), round(pm,6))
			
		    # Sim mit gleichen Params zwar vorhanden, aber nicht nutzbar, da Länge/Anzahl verschieden
		    if not mySim.length == length or not mySim.number == number:
			print 'neue Sim noetig, da l/n falsch'
			speichern = True
			# neue Sim nötig
		        if ps < 0.5 or pm > 0.5:
			    print "neue Sim, da falsch",
			    mySim = Simulation(round(ps, 6), round(pm,6), length, number, simulate(ps, pm, length, np.zeros(number), np.array([True]*number)))
			else:
			    print "fake, da falsch",
			    mySim = Simulation(round(ps, 6), round(pm,6))

		
		# Simulation mit diesen Params existiert nicht, daher neu machen
	    except (IOError, EOFError):
	        speichern = True
	        if ps < 0.5 or pm > 0.5:
		    print "simuliere, da nicht vorhanden"
		    mySim = Simulation(round(ps, 6), round(pm,6), length, number, simulate(ps, pm, length, np.zeros(number), np.array([True]*number)))
	        else:
		    print "fake, nicht vorhanden",
		    mySim = Simulation(round(ps, 6), round(pm,6))
		   
		    
	    if speichern:
	       # print "speichern"
	        filename = 'Sim_'+ str(round(ps,6)) +'_' +  str(round(pm,6))+ ".p"
	        with open(filename, 'wb') as datei:
		    pickle.dump(mySim, datei)		    
	 
            # ins array kommt jetzt die Sim, entweder eine alte, falls verwertbar oder eine neue
            testarray[i][j]=mySim

                    
            
    # Die Liste mit allen für spätere Verwendung speichern, ist diese vorhanden, sind die ganzen .p im Prinzip hinfällig
    filename = 'Sim_'+ time.strftime("%d%b%Y_%H:%M:%S")+".pickle"
    print filename 
    with open(filename, 'wb') as datei:
        pickle.dump(testarray, datei)

    # Ende :)
    print "Zeit "+str(time.clock()- startzeit)     
    

if __name__ == "__main__":
    main() 
