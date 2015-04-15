#!/usr/bin/env python
# -*- coding: latin-1 -*- 
# Hoffentlich finale Version für die 2-Param Simulation

import scipy.stats
import pickle
import logging
import argparse     
import numpy as np
import time
import matplotlib.pyplot as plt

# Speichert alle interessanten Dinge einer Simulation ab
class Simulation():
    """Simuliert und speichert Daten einer Simulation
    """
    versionsnummer = 6.0
    
    def __init__(self, ps, pm, length, number, mode, times = [], pd = (), version = versionsnummer):
        """__init__
        
        ps, pm - Parameter; Wahrscheinlichkeit, stationaer/mobil zu bleiben, wenn ein Teilchen schon in diesem Zustand ist
        length - Laenge der Saule
        number - Anzahl simulierter Teilchen
        mode - Wie wird simuliert, each_timestep (T) oder by_event (E)
        times - Ankunftszeiten
        pd - aus den times errechnete Peakdaten: ((loc, scale), width, height)
        v - Versionsnummer eben ;)
        """
        self.params = (ps, pm)
        self.length = length
        self.number = number
        self.mode = mode
        if times:
            self.times = times
            self.mean = np.mean(self.times)
            self.variance = np.var(self.times)
            self.skewness = scipy.stats.skew(self.times)
            self.kurtosis = scipy.stats.kurtosis(self.times)
        # peakdaten der form: ((loc,scale),width,height)
        if pd:
            self.pd = pd
        self.version = version

    def simulate_step(self, locations, mobile_states, number):
        """Simuliere einen Schritt für alle Teilchen.
        
        ps, pm -- Wahrscheinlichkeit stationaer/mobil zu bleiben
        (new_)locations -- np-array aller Orte vor bzw. nach diesem Aufruf
        (new_)mobile_states -- np-array aller Teilchenzustaende vor bzw. nach diesem Aufruf
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
        new_mobile_states =  np.bitwise_or(np.bitwise_and(mobile_states, zzv3), (np.invert(np.bitwise_or(mobile_states, zzv2))))
        # wenn mobil, addiere 200 zum Ort; Festlegung auf 0.2mm mitte November 2014
        new_locations = locations + (200 * new_mobile_states)
        logging.log(10, locations[0:10])
        logging.log(10, new_locations[0:10])
        logging.log(10, mobile_states[0:10])
        logging.log(10, new_mobile_states[0:10])
        return new_locations, new_mobile_states

    def simulate_each_timestep(self):
        """ Simuliere und teste auf fertig.
        simulate_each_timestep vs simulate_by_event
        """
        # startzeit für Laufzeitmessungen
        startzeit = time.clock()
        # Wird Liste aller Ankunftszeiten
        arrival_counter = []
        # Simulationszeit in Sekunden
        time_needed = 0
        # Anzahl zu simulierender Teilchen
        number = self.number
        
        # aktuelle Orte der Teilchen
        locations = np.zeros(number)
        # akutelle Zustaende der Teilchen 
        mobile_states = np.array([True]*number)
    
        #Teil 1: Sim bis frueheste Teilchen ankommen koennen, hier muss noch keine Abbruchbed. getestet werden
        while time_needed < self.length/10000:
            locations, mobile_states = self.simulate_step(locations, mobile_states, number)
            time_needed += 0.00001
            logging.log(10, time_needed)
        # Zeit soll hier 1/10s sein
        logging.log(20, "Teil1 vorbei, zeit:%s, simdauer:%s", time_needed, time.clock()-startzeit)
        logging.log(13, locations[0:10])
        #Teil 2: Ab jetzt koennen Teilchen fertig sein, teste erst, dann x neue Runden
        while True:
            # d ist bitmaske aller aktuell angekommenen Teilchen
            d = locations < self.length
            logging.log(10, locations)
            logging.log(13, d[0])
            logging.log(15, "in der trueschleife, zeit: %s", time_needed)
            # die beiden Arrays aktualisieren (rauswerfen aller fertigen Teilchen)
            locations = locations[d]
            mobile_states = mobile_states[d]   
            #zähle (suminvert...) wie viele schon durch, haenge deren Zeiten ans Ergebnis an
            for j in range(np.sum(np.invert(d))):
                arrival_counter.append(time_needed)

            # Abbruchbedingung: alle teilchen angekommen :) oder Simulation dauert schon zu lange :(
            number = len(locations)
            if number < 1:
                logging.log(25, "fertig, simzeit: %s, realtime: %s", time_needed, (time.clock()-startzeit))
                break
            if time_needed > 240:
                logging.log(25, "dat bringt nix, %s", (time.clock()-startzeit))
                # alle noch nicht fertigen Teilchen bekommen 100 Sek Strafe, damit man sieht, dass Simulation nicht zu Ende durchgefuehrt wurde
                for j in range(len(locations)):
                    arrival_counter.append(time_needed+100)
                break    
            
            # Damit es schneller geht, nach je x schritten nur testen
            for x in range (1000):
                locations, mobile_states = self.simulate_step(locations, mobile_states, number)
                time_needed+=0.00001
        
        #print time.clock()-startzeit
        self.times = arrival_counter
        self.recalculate_moments()

    def test_finished(self, teilchenliste):
        """Teste, ob die Teilchen schon durch sind"""
        #finished = np.array([False if o<=self.length else o-self.length for z, o in teilchenliste])
        
        teile = [(z, o) for z, o in teilchenliste if o < self.length]
        
        zeiten = [o-self.length for z, o in teilchenliste if o>=self.length]
        #zustaende, orte = zip(*teilchenliste)
        if len(zeiten) > 0:
            logging.log(13, "teile und zeiten %s %s", teile, zeiten)
#        fertig = orte > self.length
        #logging.log(10, "fertig? %s", finished)
        
        return teile, zeiten
        
    def simulate_event(self, teilchenliste):
        """Simuliere ein zeitliches Event"""
        
#        [(!zustand, ort) for (zustand, ort) in teilchenliste]
        
        zustaende, orte = zip(*teilchenliste)
        logging.log(10, "zustaende %s", zustaende[0:10])
        logging.log(10, "orte %s", orte[0:10])
#        zustaende = [!zustand for (zustand, ort) in teilchenliste]
#        orte = [ort for (zustand, ort) in teilchenliste]
        
        
        # Geometrisch verteilt: Zeit bis zum naechsten Erfolg
        zeitspannen_ps = scipy.stats.geom.rvs(1-self.params[0], size = len(teilchenliste))
        zeitspannen_pm = scipy.stats.geom.rvs(1-self.params[1], size = len(teilchenliste))
        
        
        logging.log(10, "zeitspannen_ps %s", zeitspannen_ps[0:10])
        logging.log(10, "zeitspannen_pm %s", zeitspannen_pm[0:10])
        zeitspannen_pm *= zustaende
        zustaende = [not x for x in zustaende]
        zeitspannen_ps *= zustaende        
        zeitspannen = zeitspannen_pm + zeitspannen_ps
        
        logging.log(10, "zeitspannen_ps %s", zeitspannen_ps[0:10])
        logging.log(10, "zeitspannen_pm %s", zeitspannen_pm[0:10])
        
        logging.log(10, "zeitspannen %s", zeitspannen[0:10])   
                    
        orte += (zeitspannen_pm * 200)
        
#        logging.log(10, "orte_pm %s", orte_pm[0:10]    
        logging.log(10, "orte %s", orte[0:10])
        
        new_events = list(zip(zeitspannen, zustaende, orte))
        
        #time.sleep(0.1)
        return new_events
        
    def simulate_by_event(self):
        """Simuliert mit Hilfe einer Liste von Events
        """
        startzeit = time.clock()
        logging.log(25, "simuliere %s", self.params)
        length = self.length
        number = self.number
        act_time = 0
    
        # Ereignisse als dict. Jeweils als key einen Zeitpunkt (enthaelt nur diejenigen, wo auch was passiert, Vergangenheit wird geloescht) und eine Liste aller Teilchen, mit denen dann was passieren soll
        events = {}
        hl = list()
        # Init: Zu Zeitpunkt 0 passiert mit allen Teilchen was
        # Teilchen als Tupel von Zustand (0=stat, 1=mob) und Ort
        for i in range(number):
            hl.append((True, 0))
        events[act_time]=hl
        
        # Hier kommen die Ankunftszeiten rein
        arrival_counter = []
        
        # solange noch Ereignisse ausstehen, wird simuliert
        teil1 = int(length)
        for act_time in range(teil1):
            if act_time in events:
                teilchenliste = np.array(events[act_time])
                new_events = self.simulate_event(teilchenliste)
                for zeitdiff, zustand, ort in new_events:
                    try:
                        events[act_time + zeitdiff].append((zustand, ort))
                    except KeyError as err:
                        #print "KeyError", err
                        events.update({act_time + zeitdiff:[(zustand, ort)]})
                del events[act_time]
            # Kein Ereignis zu aktuellem Zeitpunkt act_time
        act_time = teil1
        print("teil1vorbei")
        logging.log(20, "teil1 %s, realtime: %s sec, events: %s", act_time, time.clock()-startzeit, len(events))    
        while len(events) > 1:
            if act_time in events:
                #if (act_time % 10000) == 0:
                #    logging.log(15, "tu noch was %s, events: %s", act_time/100000, len(events))
                logging.log(11, "bei time: %s events: %s", act_time/100000, events[act_time])
                logging.log(11, "betrachte zeitpunkt %s", act_time)
                # Liste aller Teilchen, mit denen zu diesem Zeitpunkt was passiert
                teilchenliste = np.array(events[act_time])
                teilchenliste, zeiten = self.test_finished(teilchenliste)
                arrival_counter.extend([(act_time+(zeitpunkt/200)) for zeitpunkt in zeiten])
                
                #logging.log(25, "noch da2")
                # Falls die Teilchen dieses Zeitpunktes alle durch sind, wird nicht mehr simuliert
                if len(teilchenliste) > 0:
                    new_events = self.simulate_event(teilchenliste)
                    for zeitdiff, zustand, ort in new_events:
                        try:
                            events[act_time + zeitdiff].append((zustand, ort))
                        except KeyError as err:
                            #print "KeyError", err
                            events.update({act_time + zeitdiff:[(zustand, ort)]})
                         
                del events[act_time]
                ##Zeitpunkt abgearbeitet, Vergangenheit loeschen
            #naechste Zeit betrachen    
            act_time += 1  
            #print ("events", len(events), 'act_time:', act_time)
        self.times = [zeit/100000 for zeit in arrival_counter]
        logging.log(25, "fertig, simzeit: %s, realtime: %s", act_time/100000, (time.clock()-startzeit))
        
    def set_pd(self, pd, v = versionsnummer):
        """setzt peakdaten und versionsnummer neu, falls veraltet oder nicht vorhanden zu gebrauchen"""
        self.pd = pd
        self.version = v

    def __repr__(self):
            return (str(self.params) + self.mode)
        
    def get_moment(self, moment):
        """Gibt den Wert des "moment" zurück"""
        if moment == "mean":
            return self.mean
        if moment == "variance":
            return self.variance
        if moment == "skewness":
            return self.skewness
        if moment == "kurtosis":
            return self.kurtosis
        return None
        
    def recalculate_moments(self): 
        """sollte nicht mehr gebraucht werden, berechnet die Momente neu"""
        self.mean = np.mean(self.times) 
        self.variance = np.var(self.times)
        self.skewness = scipy.stats.skew(self.times)
        self.kurtosis = scipy.stats.kurtosis(self.times)
        
# für Kommandozeilentests      
def get_argument_parser():
    p = argparse.ArgumentParser(
    description = "beschreibung")  
    p.add_argument("--inputfile", "-i", type = str,  help = "input file (pickled)")
    p.add_argument("--moment", "-m" , help = "which moment is of interest")
    p.add_argument("--recalc", "-rc", type=str, help = "recalculate moments")
    p.add_argument("--number", "-n", help = "how many files to recalculate")
    
    return p

#aktuell nur genutzt, um die Momente neu zu berechnen, war noetig dank alter scipy-version
# ansonsten fuer testzwecke
def main():
    number = 10000
    length = 200000
    print ("n", number, "l", length, time.strftime("%d%b%Y_%H:%M:%S"))
    p = get_argument_parser()
    args = p.parse_args()
    neueSim = Simulation(0.9992, 0.999, length, number, [])
    neueSim.simulate_by_event()
    #print (neueSim, neueSim.times)
    n, bins, patches = plt.hist(neueSim.times, 50, normed=1, alpha=0.5)
    
    #neueSim.simulate_each_timestep()
    #n, bins, patches = plt.hist(neueSim.times, 50, normed=1, alpha=0.5)
    
    plt.show()
       
if __name__ == "__main__":
    logging.basicConfig(level=20)
    main()
