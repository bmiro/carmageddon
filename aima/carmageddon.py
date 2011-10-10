# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import deepcopy
from random import random, randint

# Macros for easy indexation of coor tuples.
# i.e. a[X] -> xcoor
X = 0
Y = 1
MAX_DIST = 200

def distance(src, dst):
  return abs(src[X] - dst[X]) + abs(src[Y] - dst[Y])

class Passenger(object):
  def __init__(self, name, xo, yo, xd, yd):
    self.__name = name
    self.__xo = xo
    self.__yo = yo
    self.__xd = xd
    self.__yd = yd

  def getDestination(self):
    return (self.__xd, self.__yd)

  def getOrigin(self):
    return (self.__xo, self.__yo)

  def getName(self):
    return self.__name

class Driver(Passenger):
  def __init__(self, name, xo, yo, xd, yd, maxspace):
    Passenger.__init__(self,name,xo,yo,xd,yd)
    self.__freespace = maxspace
    self.__maxspace = maxspace
    self.__passengers = []

  def isEmpty(self):
    return self.__freespace == self.__maxspace

  def isFull(self):
    return self.__freespace == 0

  def getPassengers(self):
    return self.__passengers

  def pickupPassenger(self, passenger):
    if self.__freespace == 0:
      print "The car is full!!" #TODO trow CAR_OVERFLOW exception
    else:
      self.__passengers.append(passenger)
      self.__freespace -= 1

  def leavePassenger(self, passenger):
    if empty(self.__passengers):
      print "There is no passengers to leave!" #TODO throw CAR_EMPTY exception
    else:
      self.__passengers.remove(passenger)
      self.__freespace += 1

  def getDestinations(self):
    d = []
    for p in self.__passsengers:
      d.append(p.getDestination())
    return d


  """ Returns the min route that involves all the passengers
  "   i.e. 
  "   [[[33, 44], "DriverOrigin"],
  "    [[34, 45], "PickupPassenger"],
  "    [[55, 65], "LeavePassenger"],
  "    [[57, 70], "DriverDestination"]]
  """
  def getRoute(self):
    ## Dictionary of point pointing destinations if exist
    # i.e. { [34, 45] : [22, 56] --> Point is origin
    #        [56, 77] : None }   --> Point is destination
    checkpoints = {}

    ## List of tuples [point, event]
    # i.e. [[34, 45] "PickupPassenger"]
    route = [] 

    # Inserting all origin points
    for p in self.__passengers:
      checkpoints[p.getOrigin()] = p.getDestination()

    current = [self.getOrigin(), "DriverOrigin"]
    while checkpoints:
      # Searching nearst point
      d = MAX_DIST
      nearest = []
      for c in checkpoints.keys():
        if distance(current[0], c) < d:
          d = distance(current[0], c)
          nearest = c
          
      route.append(current)
      dest = checkpoints.pop(c)
      if dest != None:
        checkpoints[dest] = None
        event = "PickupPassenger"
      else:
        event = "LeavePassenger"
      current = [c, event]   

    route.append(current)
    route.append([self.getDestination(), "DriverDestination"])
    return route

  def getRouteWeight(self,route):
    w = 0
    current = route[0][0]
    for p in route:
      w += distance(current, p[0])
      current = p[0]
    return w



class State(object):
  def __init__(self, nPassengers=12, nMaxDrivers=8, citySize=10000.0, squareSize=100.0):

    self.__citySize = citySize
    self.__squareSize = squareSize
    self.__carmageddons = {}
    self.__passengers = {}
    self.__nPassengers = 0
    self.__nDrivers = 0

    for d in range(nMaxDrivers):
      drv = self.genRandomDriver()
      self.__carmageddons[drv.getName()] = drv
      self.__nDrivers += 1

    for p in range(nPassengers):
      pss = self.genRandomPassenger()

      alloqued = False
      for c in self.__carmageddons.iterkeys():
        if not self.__carmageddons[c].isFull():
          self.__carmageddons[c].pickupPassenger(pss)
          self.__passengeres[pss] = c
          self.__nPassengeres += 1
          alloqued = True
          break

      if not alloqued:
        print "There are more passengers than free space!!!" #TODO raise exception
  
  def genRandomDriver(self):
    d = Driver('D-' + str(random())[2:8], randint(0, self.__citySize), \
                                          randint(0, self.__citySize), \
                                          randint(0, self.__citySize), \
                                          randint(0, self.__citySize), 2)
    return d

  def genRandomPassenger(self):
    p = Passenger('P-' + str(random())[2:8], randint(0, self.__citySize), \
                                             randint(0, self.__citySize), \
                                             randint(0, self.__citySize), \
                                             randint(0, self.__citySize))
    return p

  def getDrivers(self):
    return self.__carmageddons

  def getPassengers(self):
    return self.__passengers

  def getNumPassengers(self):
    return self.__nPassengers

  def getNumDrivers(self):
    return self.__nDrivers

  def degradateDriver(self, degradatedDriver, carrierDriver): #TODO posar un nom mes guais
    if not self.__carmageddons[degradatedDriver].isEmpty():
      print "Trying to degradeta a not empty driver!" #TODO aixecar excepció
      return -1

    if self.__carmagaddons[carrierDriver].isFull():
      print "The carrier driver is full" #TODO aixecar excepció
      return -2

    if self.__nDrivers == 0:
      print "You can not degradate the last driver!" # TODO aixecar excepció
      return -3

    d = self.__carmageddons.pop(degradatedDriver)
    name = d.getName()
    name[0] = 'P'
    p = Passenger(name, d.getOrigin()[0], d.getOrigin()[1], \
                        d.getDestination()[0], d.getDestintion()[1])

    self.__carmageddons[carrierDriver].pickupPassenger(p)
    self.__nDrivers -= 1
    self.__nPassengers += 1


  def switchPassenger(self, passenger, newCarrier):
    #TODO gestionar excepcions
    self.__carmageddons[self.whoPickuped(passenger)].leavePassenger(passenger)
    self.__carmageddons[newCarrier.getName()].pickupPassenger(passenger)
    self.__passengeres[passenger] = newCarrier.getName()

  def whoPickuped(self, passenger):
    return self.__passengres[passenger]

  def __repr__(self):
    s = ""
    for c in self.__carmageddons:
      s += "Driver " + c.getName() + " pickups: \n"
      if c.isEmpty():
        s += "None\n"
      else:
        for p in c.getPassengers():
          s += "   " + p.getName() + "\n"
    return s

class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
  
  def successor(self, state):
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    for p in passengers:
      
      

    #Gens all the driver deletions (gens at most (nDrivers-1)*(nDrivers-2) )
    for d in state.getDrivers():
      pass

  def goal_test(self, state):
    pass
    
  def value(self, node):
    """Heuristic function"""
    pass

if __name__ == "__main__":
  print "hola"
  p = Passenger("joan", 1, 1, 9, 9)
  d = Driver("bernat", 0, 0, 10, 10, 2)

  d.pickupPassenger(p)
  r = d.getRoute()
  print r
  print d.getRouteWeight(r)

  s = State()
  print s

