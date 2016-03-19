import sys
import csv
import googlemaps
import random
import copy
from bitstring import BitArray, BitString


#print sys.argv[1]
#print sys.argv[2]


population = int(sys.argv[1])
mutationrate = float(sys.argv[2])

maxelevation = 3979

##print population
##print mutationrate

#Google Maps API key
gmaps = googlemaps.Client(key = #yourkeyhere)

stop = False
genepool = []
children = []
closecalls = []
generation = 0

class Alien(object):
    sexpriority = 0
    elevation = 0

    def __init__(self, x, y, height, weight, rocky):
        self.x = BitArray('0b'+bin(x).lstrip('0b').zfill(8))
        self.y = BitArray('0b'+bin(y).lstrip('0b').zfill(8))
        self.height = BitArray('0b'+bin(height).lstrip('0b').zfill(4))
        self.weight = BitArray('0b'+bin(weight).lstrip('0b').zfill(4))
        self.rocky  = BitArray('0b'+bin(rocky).lstrip('0b').zfill(4))


#random 1st generation
def spawn():
    print "Spawning first generation of Aliens......"
    global genepool
    global population
    for z in range(population):
        x = random.randint(0, 255)
        y = random.randint(0, 255)
        height = random.randint(0, 15)
        weight = random.randint(0, 15)
        rocky = random.randint(0, 15)
        genepool.append(Alien(x,y, height, weight, rocky))

#function for mapping Alien.x and Alien.y to coordinates
#edits Alien.sexpriority based on elevation
def map():
    print "Now mapping Aliens......"
    global genepool
    counter = 0
    for elem in genepool:
        #map 128,128 to Mount Maclure, every increase of 1 = 0.0001 decimal degree
        maclurex = 37.743541
        maclurey = -119.281537
        dunit = 0.0001


        #ensure that process retries until request is succesful
        while True:
            try:
                elevation = gmaps.elevation((maclurex+dunit*(int(elem.x.bin, 2)-128), maclurey+dunit*(int(elem.y.bin, 2)-128)))[0]['elevation']
                break
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print "Google Maps connection error, trying again..."




        #print int(round(elevation))
        #store elevation in Alien.elevation
        elem.elevation = int(round(elevation))

        #Write to File
        global generation
        b = open('data.csv', 'a')
        a = csv.writer(b)
        data = [elem, generation, int(elem.x.bin, 2), int(elem.y.bin, 2), elem.elevation, int(elem.height.bin, 2), int(elem.weight.bin, 2), int(elem.rocky.bin, 2)]
        a.writerow(data)
        b.close()
        counter += 1

        print counter, "/", population
    #make new array
    sortinghat = copy.copy(genepool)
    #for every member in array
    for p in range(len(sortinghat)):
        maximum = 0
        #find maximum
        for elem in sortinghat:
            if elem.elevation > maximum:
                maximum = elem.elevation
                index = sortinghat.index(elem)

        #assign sex priority and remove from sortinghat
        sortinghat[index].sexpriority = len(genepool)-p
        sortinghat.pop(index)


    #Find top member again
    #find maximum
    topperformer = 0
    for elem in genepool:
        if elem.elevation > topperformer:
            topperformer = elem.elevation
            ID = elem
    global stop
    if topperformer == maxelevation:
        stop = True


    """
    #print " "
    #print " "
    #print "Map Complete!"
    #print "-----------------"
    #print "Top performer is: "
    #print ID, "elevation: ", topperformer
    #print " "
    #print " "
    #print "Top Sex Priority = ", len(genepool)
    for elem in genepool:
       #print "Sex Priority: ", elem.sexpriority, " Elevation: ", elem.elevation
    """

#Function for removing dead aliens from gene pool
def casualties(alien, height, weight, rocky, intensity):
    global closecalls
    #Test to see if alien lives
    #print "Testing alien: ", alien, " at index: ", genepool.index(alien)
    lifescore = intensity*height*int(alien.height.bin, 2) + intensity*weight*int(alien.weight.bin, 2) + intensity*rocky*int(alien.rocky.bin, 2)
    #print "    lifescore: ", lifescore
    #If alien dies, remove from gene pool
    if lifescore < 0.0:
        #print genepool.index(alien), "is now dead. :("
        genepool.pop(genepool.index(alien))
    elif lifescore == 0.0:
        #print genepool.index(alien), "is just hanging on......"
        closecalls.append(alien)
    else:
        #print genepool.index(alien), "LIVES! :D"
        pass


#Funciton for running disasters
def storm():
    print "Runing Storm"
    #Roll for disaster type
    disaster = random.choice(("Wind","Flood","Earthquake","None"))
    #print "Disaster type: ", disaster
    #Roll for disaster intensity
    intensity = random.randint(1,4)
    #print "Disaster intensity: ", intensity
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

    #print "Before enforce even casulaties, genepool size: ", len(genepool)
    #print "Before enforce even casulaties, closecalls size: ", len(closecalls)

    #ensure casulaties always is even number
    if len(genepool)%2 == 1:
        #print "genepool size is odd: ", len(genepool)
        if closecalls == []:
            freakaccident = random.choice(genepool)
            genepool.pop(genepool.index(freakaccident))
            #print freakaccident, " died of a freak accident!"
        else:
             unlucky = random.choice(genepool)
             genepool.pop(genepool.index(unlucky))
             #print unlucky, " was unlucky and died."
    #print " "
    #print " "
    #print "-----------------"
    #print "Total casualties: ", population - len(genepool)







def breed():
    print "Now breeding Aliens......"
    global genepool
    global children
    #raw_input("presskeytoadvance")
    #re-order genepool for all members
    genepool.sort(key=lambda genepool: genepool.sexpriority, reverse=False)
    #clean the children array
    children=[]

    #print "Before breed genepool size: ", len(genepool)
    #print "Before breed children size: ", len(children)

    #find next parents to breed
    for x in range(len(genepool)/2):
        parentA = genepool[len(genepool)-(2*x)-1]
        parentB = genepool[len(genepool)-(2*x+1)-1]
        #print "parentA: ", parentA
        #print "parentB: ", parentB
        #print "............."
        #print "Mating: ",parentA.sexpriority, parentB.sexpriority
        #print " "

        childA = copy.deepcopy(parentA)
        childB = copy.deepcopy(parentB)


#        swap 4 middle bits of x

        childA.x[2]=parentB.x[2]
        childB.x[2]=parentA.x[2]

        childA.x[3]=parentB.x[3]
        childB.x[3]=parentA.x[3]

        childA.x[4]=parentB.x[4]
        childB.x[4]=parentA.x[4]

        childA.x[5]=parentB.x[5]
        childB.x[5]=parentA.x[5]

#       swap 4 middle bits of y

        childA.y[2]=parentB.y[2]
        childB.y[2]=parentA.y[2]

        childA.y[3]=parentB.y[3]
        childB.y[3]=parentA.y[3]

        childA.y[4]=parentB.y[4]
        childB.y[4]=parentA.y[4]

        childA.y[5]=parentB.y[5]
        childB.y[5]=parentA.y[5]


#       swap two last bits of height

        childA.height[2]=parentB.height[2]
        childB.height[2]=parentA.height[2]

        childA.height[3]=parentB.height[3]
        childB.height[3]=parentA.height[3]

#       swap two last bits of weight

        childA.weight[2]=parentB.weight[2]
        childB.weight[2]=parentA.weight[2]

        childA.weight[3]=parentB.weight[3]
        childB.weight[3]=parentA.weight[3]

#       swap two last bits of rocky

        childA.rocky[2]=parentB.rocky[2]
        childB.rocky[2]=parentA.rocky[2]

        childA.rocky[3]=parentB.rocky[3]
        childB.rocky[3]=parentA.rocky[3]

        maybemutate(childA)
        maybemutate(childB)

        children.append(childA)
        children.append(childB)

    #print "Before replenish genepool size: ", len(genepool)
    #print "Before replenish children size: ", len(children)

#replenish population for those who have fallen

    replenish = population - len(genepool)
    if replenish > 0:
        for x in range(replenish):
            #find top sex priority
            for elem in genepool:
                if elem.sexpriority == len(genepool)-x:
                    #add it to children
                    children.append(elem)
                    #print "Revived and added to children: ", elem, " elevation: ", elem.elevation


    #print "Before copy genepool size: ", len(genepool)
    #print "Before copy children size: ", len(children)

    genepool = copy.deepcopy(children)

    #print "After copy genepool size: ", len(genepool)
    #print "After copy children size: ", len(children)
    #raw_input("presskeytoadvance")


def maybemutate(alien):

    for i in range(8):
        if (100-mutationrate)>random.randint(0, 100):
            alien.x[i]= not alien.x[i]

    for i in range(8):
        if (100-mutationrate)>random.randint(0, 100):
            alien.y[i]= not alien.y[i]

    for i in range(4):
        if (100-mutationrate)>random.randint(0, 100):
            alien.height[i]= not alien.height[i]

    for i in range(4):
        if (100-mutationrate)>random.randint(0, 100):
            alien.weight[i]= not alien.weight[i]

    for i in range(4):
        if (100-mutationrate)>random.randint(0, 100):
            alien.rocky[i]= not alien.rocky[i]






#do this thing
def run():
    #1st generation
    spawn()

    while not stop:
        global generation
        generation += 1
        print " "
        print " "
        print "-----------------"
        print " "
        print "Now running generation ", generation
        print " "
        print "-----------------"
        print " "

        #Run disaster - get casualties
        storm()

        #Assign sex priority based on elevation
        map()

        #breed
        breed()
    print "*****************"
    print "-----------------"
    print " "
    print "Test complete!"
    for elem in genepool:
        if elem.elevation == maxelevation:
            print "Top performer is: "
            print elem, elem.x, elem.y, elem.elevation
    print " "
    print "-----------------"
    print "*****************"


run()
