# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import deepcopy,copy
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

  def setPassengers(self,p):
    self.__passengers = p


  """ Recives a passenger object """
  def pickupPassenger(self, passenger):
    if self.__freespace == 0:
      print "The car is full!!" #TODO trow CAR_OVERFLOW exception
    else:
      self.__passengers.append(passenger.getName())
      self.__freespace -= 1


  """ Recives a passenger object """
  def leavePassenger(self, passenger):
    if len(self.__passengers) == 0:
      print "There is no passengers to leave!" #TODO throw CAR_EMPTY exception
    else:
      self.__passengers.remove(passenger.getName())
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
  def getRoute(self,state):
    ## Dictionary of point pointing destinations if exist
    # i.e. { [34, 45] : [22, 56] --> Point is origin
    #        [56, 77] : None }   --> Point is destination
    checkpoints = {}

    ## List of tuples [point, event]
    # i.e. [[34, 45] "PickupPassenger"]
    route = [] 

    # Inserting all origin points
    for p in self.__passengers:
      checkpoints[state.getPassengers()[p][0].getOrigin()] = state.getPassengers()[p][0].getDestination()

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


  def getRouteWeight(self, route):
    w = 0
    current = route[0][0]
    for p in route:
      w += distance(current, p[0])
      current = p[0]
    return w



class State(object):
  def __init__(self, nPassengers=50, nMaxDrivers=26, citySize=10000.0, squareSize=100.0):

    self.__citySize = citySize
    self.__squareSize = squareSize
    
    # Dict of drivers, driver name as key pointing to driver obcjet
    self.__carmageddons = {}
    
    #  Dict of passengeres, passenger name as key pointing to a tupla
    # of passenger object and driver name
    self.__passengers = {}

    for d in range(nMaxDrivers):
      drv = self.genRandomDriver()
      self.__carmageddons[drv.getName()] = drv

    for p in range(nPassengers):
      pss = self.genRandomPassenger()

      alloqued = False
      for c in self.__carmageddons.iterkeys():
        if not self.__carmageddons[c].isFull():
          self.__carmageddons[c].pickupPassenger(pss)
          self.__passengers[pss.getName()] = (pss, c)
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

  def setDrivers(self,d):
    self.__carmageddons = d

  def getPassengers(self):
    return self.__passengers

  def setPassengers(self,p):
    self.__passengers = p



  def getNumPassengers(self):
    return len(self.__passengers)


  def getNumDrivers(self):
    return len(self.__carmageddons)


  """ Recives two key for each driver (degradated and carrier) """
  def degradateDriver(self, degradatedDriver, carrierDriver): #TODO posar un nom mes guais
    if not self.__carmageddons[degradatedDriver].isEmpty():
      print "Trying to degradeta a not empty driver!" #TODO aixecar excepció
      return -1

    if self.__carmageddons[carrierDriver].isFull():
      print "The carrier driver is full" #TODO aixecar excepció
      return -2

    if self.getNumDrivers() == 0:
      print "You can not degradate the last driver!" # TODO aixecar excepció
      return -3

    d = self.__carmageddons.pop(degradatedDriver)
    d = copy(d)
    name = d.getName()
    name = name.replace('D', 'P')
    name = name.replace('-', 'D')
    p = Passenger(name, d.getOrigin()[0], d.getOrigin()[1], \
                        d.getDestination()[0], d.getDestination()[1])


    newdriver_pick = deepcopy(self.__carmageddons[carrierDriver])
    self.__carmageddons[carrierDriver] = newdriver_pick
    self.__carmageddons[carrierDriver].pickupPassenger(p)
    self.__passengers[p.getName()] = (p, self.__carmageddons[carrierDriver].getName())
    
    
  """ Passenger is a passenger name and also newCarrier the new driver name """
  def switchPassenger(self, passenger, newCarrier):
    #TODO gestionar excepcions]
    p = self.__passengers[passenger][0]
    pname = self.__passengers[passenger][1]


    newdriver_leave = deepcopy(self.__carmageddons[pname])
    self.__carmageddons[pname]=newdriver_leave
    self.__carmageddons[pname].leavePassenger(p)

    newdriver_pick = deepcopy(self.__carmageddons[newCarrier])
    self.__carmageddons[newCarrier] = newdriver_pick
    self.__carmageddons[newCarrier].pickupPassenger(p)

    self.__passengers[passenger] = (p, newCarrier)
    


  def whoPickuped(self, passenger):
    return self.__passengers[passenger][1]


  def __repr__(self):
    s = ""
    
    s += "Passenger info:\n"
    for p in self.__passengers:
      s += "\t" + p + " is pickuped by " + self.__passengers[p][1] + "\n"
    
    s += "\nDrivers info:\n"
    for c in self.__carmageddons:
      s += "\t" + c + " pickups: \n"
      if self.__carmageddons[c].isEmpty():
        s += "None\n"
      else:
        for p in self.__carmageddons[c].getPassengers():
          s += "\t\t" + p + "\n"
    return s


  def getKm(self):
    i = 0
    for p in self.__carmageddons.itervalues():
      i += p.getRouteWeight(p.getRoute(self))
    return i
    
    

class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
    self.initial = state
  
  
  def successor(self, state):
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    print state.getKm()
    for p in state.getPassengers():
      currentDrv = state.whoPickuped(p)
      
      for d in state.getDrivers().iteritems():
        if d[0] != currentDrv and not d[1].isFull():
	  #Switch passenger to this driver
	  newState = copy(state)
          newState.setDrivers(copy(state.getDrivers()))
          newState.setPassengers(copy(state.getPassengers()))
	  newState.switchPassenger(p, d[0])
	  yield ("sw",newState)
      
    #Gens all the driver deletions (gens at most (nDrivers-1)*(nDrivers-2) )
    print "Degradating drivres\n"
    for d in state.getDrivers().itervalues():
      if d.isEmpty():
	for carrier in state.getDrivers().iteritems():
	  if carrier[0] != d.getName() and not carrier[1].isFull():
	    newState = copy(state)
            newState.setDrivers(copy(state.getDrivers()))
            newState.setPassengers(copy(state.getPassengers()))
	    newState.degradateDriver(d.getName(), carrier[0])
	    yield ("dgrd",newState)
            break

  def goal_test(self, state):
    pass
    
    
  def value(self, node):
    """Heuristic function"""
    return -node.state.getKm()
    pass


if __name__ == "__main__":
  print "hola"
  #p = Passenger("joan", 1, 1, 9, 9)
  #d = Driver("bernat", 0, 0, 10, 10, 2)


  #d.pickupPassenger(p)
  #r = d.getRoute(s)
  #print r
  #print d.getRouteWeight(r)


  #print s
  s = State()
  c = Carmageddon(s)
  #for suc in c.successor(s):
  #  print(suc)
  f = hill_climbing(c)
  print f.getKm()
  print f
  for d in f.getDrivers().itervalues():
    print d.getRouteWeight(d.getRoute(f))
  
  

