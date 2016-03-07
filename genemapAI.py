import googlemaps
import random
from bitstring import BitArray, BitString

#Google Maps API key
gmaps = googlemaps.Client(key = 'AIzaSyCMDZHOxRUdinR1iawcBMV-bGTY34wREXI')

genepool = []
children = []

class Alien(object):
    sexpriority = 0

    def __init__(self, x, y, height, weight, rocky):
        self.x = BitArray('0b'+bin(x).lstrip('0b').zfill(8))
        self.y = BitArray('0b'+bin(y).lstrip('0b').zfill(8))
        self.height = BitArray('0b'+bin(height).lstrip('0b').zfill(4))
        self.weight = BitArray('0b'+bin(weight).lstrip('0b').zfill(4))
        self.rocky  = BitArray('0b'+bin(rocky).lstrip('0b').zfill(4))


#function for mapping Alien.x and Alien.y to coordinates
#edits Alien.sexpriority based on elevation
def map(Alien):
    #map 128,128 to Mount Maclure, every increase of 1 = 0.0001 decimal degree
    maclurex = 37.743541
    maclurey = -119.281537
    dunit = 0.0001
    elevation = gmaps.elevation((maclurex+dunit*(int(Alien.x.bin, 2)-128), maclurey+dunit*(int(Alien.y.bin, 2)-128)))[0]['elevation']
    print int(round(elevation))

#Function for removing dead aliens from gene pool
def casualties(alien, height, weight, rocky, intensity):
    #Test to see if alien lives
    print "Testing alien: ", alien, " at index: ", genepool.index(alien)
    lifescore = intensity*height*int(alien.height.bin, 2) + intensity*weight*int(alien.weight.bin, 2) + intensity*rocky*int(alien.rocky.bin, 2)
    print "    lifescore: ", lifescore
    #If alien dies, remove from gene pool
    if lifescore < 0.0:
        print genepool.index(alien), "is now dead. :("
    else:
        print genepool.index(alien), "LIVES! :D"



#Funciton for running disasters
def storm():
    #Roll for disaster type
    disaster = random.choice(("Wind","Flood","Earthquake","None"))
    print "Disaster type: ", disaster
    #Roll for disaster intensity
    intensity = random.randint(1,4)
    print "Disaster intensity: ", intensity
    #Evaluate disaster casualties
    for elem in genepool:
        if disaster == "Wind":
            height = -1
            weight = 1
            rocky = 0.5
            casualties(elem,-1,1,0.5, intensity)
        elif disaster == "Flood":
            height = 1
            weight = 0.5
            rocky = -1
            casualties(elem,1,0.5,-1, intensity)
        elif disaster == "Earthquake":
            height = 0.5
            weight = -1
            rocky = 1
            casualties(elem,0.5,-1,1, intensity)
        elif disaster == "None":
            pass


def breed():
    global genepool
    #re-order genepool for all members
    for x in range(len(genepool)):
        print x, "cycle"
        for elem in genepool:
            print elem
            print elem.sexpriority, "sex priority"
            #find priority
            if elem.sexpriority == len(genepool)-x:
                #find where in genepool the priority is
                index = genepool.index(elem)
                #add to END of list
                genepool=genepool+[genepool.pop(index)]





"""
#Run disaster - get casualties
storm()

map()
"""
