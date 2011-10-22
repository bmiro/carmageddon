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


  """ Recives a passenger name """
  def pickupPassenger(self, passenger):
    self.__passengers.append(passenger)
    self.__freespace -= 1
    self.calculatedRouteWeight = None


  """ Recives a passenger name """
  def leavePassenger(self, passenger):
    self.__passengers.remove(passenger)
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
    lchecks = [(self.getOrigin(),"fi")]
    for p in self.__passengers:
      checkpoints[state.getPassengers()[p][0].getOrigin()] = state.getPassengers()[p][0].getDestination()
      lchecks.append((state.getPassengers()[p][0].getOrigin(),state.getPassengers()[p][0].getDestination()))
  
    current = (self.getOrigin(), "DriverOrigin")
    npass = 0
    temp = datetime.now()

    lmarques =  [False]*len(lchecks)
    lmarques[0] = True
    sol = []
    soltmp = []
    soltmp.append(lchecks[0])

    self.permuta(lchecks,0,lmarques,soltmp,sol,len(lchecks),0,MAX_KM,self.getDestination())
    sol = sol[-1]

    #print sol
    sol[0].append((self.getDestination()))
    self.calculatedRouteWeight = sol[1] 
    sol[0][0] = sol[0][0][0]

    return sol[0]


  def permuta(self, lini, npass, lmarques, soltmp, s, npoints, dist, maxim, dest):
    print soltmp
    print dest
    if (dist + distance(soltmp[-1], dest)) > maxim:
      return
      
    if len(lini) == 1:
      soltmp.append(lini[0][0])
      distFinal = dist + distance(soltmp[-1], dest)
      if distFinal < maxim:
        s.append((soltmp[:], distFinal))
        maxim = distFinal
      return

    if len(soltmp) == npoints*2 -1: 
      distFinal = dist + distance(soltmp[-1], dest)
      if distFinal < maxim:
        s.append((soltmp[:], distFinal))
        maxim = distFinal

    longitud = len(lini)
    for x in xrange(longitud):
      if not lmarques[x] :
        lmarques[x] = True
        if lini[x][1] != "fi" and npass < 2:
          soltmp.append(lini[x][0])
          lmarques.append(False)
          lini.append((lini[x][1],"fi"))
          incr = distance(lini[x-1][0],lini[x][0])
          self.permuta(lini,npass+1,lmarques,soltmp,s,npoints,dist +incr,maxim,dest )
          lmarques.pop()
          lini.pop()
          soltmp.pop()   
        else:
          soltmp.append(lini[x][0])
          self.permuta(lini,npass-1,lmarques,soltmp,s,npoints,dist + distance(lini[x-1][0],lini[x][0]),maxim,dest)  
          soltmp.pop()
        lmarques[x] = False


  def getRouteWeight(self,state):
    if self.calculatedRouteWeight != None:
      return self.calculatedRouteWeight

    route = self.getRoute(state)
    return self.calculatedRouteWeight
