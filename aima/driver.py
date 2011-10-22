# -*- coding: utf-8 -*-
from copy import deepcopy, copy

from passenger import *

from datetime import datetime

# Macros for easy indexation of coor tuples.
# i.e. a[X] -> xcoor
X = 0
Y = 1
MAX_KM = 3000000000

def distance(src, dst):
  return abs(src[X] - dst[X]) + abs(src[Y] - dst[Y])

class Driver(Passenger):
  t = 0
  def __init__(self, name, xo, yo, xd, yd, maxSpace):
    Passenger.__init__(self, name, xo, yo, xd, yd)
    self.__freespace = maxSpace
    self.__maxSpace = maxSpace
    self.__passengers = []
    self.calculatedRouteWeight = None

  def __copy__(self):
    newone = Driver(self.getName(),self.getOrigin()[0],self.getOrigin()[1],self.getDestination()[0],self.getDestination()[1],self.__maxSpace)
    newone.__dict__.update(self.__dict__)
    newone.setPassengers(copy(self.__passengers))
    return newone



  def isEmpty(self):
    return self.__freespace == self.__maxSpace


  def getPassengers(self):
    return self.__passengers

  def setPassengers(self, p):
    self.__passengers = p

  def getMaxSpace(self):
    return self.__maxSpace

  """ Recives a passenger object """
  def pickupPassenger(self, passenger):
    self.__passengers.append(passenger.getName())
    self.__freespace -= 1
    self.calculatedRouteWeight = None


  """ Recives a passenger object """
  def leavePassenger(self, passenger):
    self.__passengers.remove(passenger.getName())
    self.__freespace += 1
    self.calculatedRouteWeight = None


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
    checkpointsDest = {}

    ## List of tuples [point, event]
    # i.e. [[34, 45] "PickupPassenger"]
    route = [] 

    # Inserting all origin points
    lchecks = []
    for p in self.__passengers:
      checkpoints[state.getPassengers()[p][0].getOrigin()] = state.getPassengers()[p][0].getDestination()
      lchecks.append((state.getPassengers()[p][0].getOrigin(),state.getPassengers()[p][0].getDestination()))
  


    current = (self.getOrigin(), "DriverOrigin")
    npass = 0
    temp = datetime.now()


    lmarques = [False]*len(lchecks)
    sol = []
    soltmp = []
    self.permuta(lchecks,0,lmarques,soltmp,sol,len(lchecks))
    print len(lchecks)
    #print sol

    while checkpoints or checkpointsDest:
      # Searching nearst point
      d = MAX_KM
      nearest = []

      for c in checkpointsDest.keys():
        if distance(current[0], c) < d:
          d = distance(current[0], c)
          nearest = c

      if npass < 2:
        for c in checkpoints.keys():
          if distance(current[0], c) < d:
            d = distance(current[0], c)
            nearest = c


          

      if nearest in checkpoints:
        checkpointsDest[nearest] = True 
        checkpoints.pop(nearest)
        event = "PickupPassenger"
        npass += 1
      else:
        event = "LeavePassenger"
        checkpointsDest.pop(nearest)
        npass -= 1

      current = (nearest, event)  
      route.append(current) 
    temp =  datetime.now() -temp
    Driver.t+=temp.microseconds


    route.append((self.getDestination(), "DriverDestination"))

    return route


  def permuta(self,lini,npass,lmarques,soltmp,s,npoints):
    if len(soltmp) == npoints*2: 
      s.append(soltmp[:])



    longitud = len (lini)
    for x in xrange(longitud):
      if not lmarques[x] :
        lmarques[x] = True
        if lini[x][1]!= "fi" and npass<2:
          soltmp.append(lini[x][0])
          lmarques.append(False)
          lini.append((lini[x][1],"fi"))
          self.permuta(lini,npass+1,lmarques,soltmp,s,npoints)
          lmarques.pop()
          lini.pop()
          soltmp.pop()   
        else:
          soltmp.append(lini[x][0])
          self.permuta(lini,npass-1,lmarques,soltmp,s,npoints)  
          soltmp.pop()
        lmarques[x] = False


  def getRouteWeight(self,state):
    if self.calculatedRouteWeight != None:
      return self.calculatedRouteWeight

    route = self.getRoute(state)
    w = 0
    current = route[0][0]
    for p in route:
      w += distance(current, p[0])
      current = p[0]
    self.calculatedRouteWeight = w
    return w
