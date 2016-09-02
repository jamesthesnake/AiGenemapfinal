from geneticmap import *

#test subjects

julie = Alien(86, 227, 4, 16, 0)
julie.sexpriority = 49
genepool.append(julie)
boss = Alien(87, 228, 3, 15, 16)
boss.sexpriority = 48
genepool.append(boss)
hi = Alien(86, 228, 4, 16, 0)
hi.sexpriority = 47
genepool.append(hi)
frank = Alien(87, 228, 3, 1, 13)
frank.sexpriority = 46
genepool.append(frank)
winner = Alien(87, 227, 3, 1, 13)
winner.sexpriority = 50
genepool.append(winner)


for elem in matinglist:
   elem.sexpriority, elem.elevation


#random map tests
gmaps.elevation((maclurex+dunit*(87-128), maclurey+dunit*(227-128)))


git fetch origin && git reset --hard origin/master && git clean -f -d

gmaps.elevation((maclurex+dunit*(89-128), maclurey+dunit*(223-128)))




(maclurex+dunit*(int(hi.x.bin, 2)-128), maclurey+dunit*(int(hi.y.bin, 2)-128))
(maclurex+dunit*(int(frank.x.bin, 2)-128), maclurey+dunit*(int(frank.y.bin, 2)-128))
(maclurex+dunit*(int(winner.x.bin, 2)-128), maclurey+dunit*(int(winner.y.bin, 2)-128))

gmaps.elevation((maclurex+dunit*(int(boss.x.bin, 2)-128), maclurey+dunit*(int(boss.y.bin, 2)-128)))[0]['elevation']

gmaps.elevation((37.739424, -119.271569))[0]['elevation']



#POI
#central point - Mount Maclure
37.743541, -119.281537
#elevation in meters
3872

#highest point - Mount Lyell
37.739424, -119.271569
#elevation in meters
3931

#highest point
winner = Alien(89, 223, 3, 1, 13)
winner.sexpriority = 50
#elevation in meteres
3979



#test for maximum
maparray = []

for x in range (10):
  for y in range(10):
    value = gmaps.elevation((maclurex+dunit*(x-128+80), maclurey+dunit*(y+220-128)))[0]['elevation']
    maparray.append(value)
    winner = max(maparray)
    print x+80, y+220, value, winner
    if value == winner:
      print "NEW MAX"
