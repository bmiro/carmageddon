# -*- coding: utf-8 -*-
from copy import deepcopy, copy

from passenger import *

# Macros for easy indexation of coor tuples.
# i.e. a[X] -> xcoor
X = 0
Y = 1
MAX_KM = 30

def distance(src, dst):
  return abs(src[X] - dst[X]) + abs(src[Y] - dst[Y])

class Driver(Passenger):
  def __init__(self, name, xo, yo, xd, yd, maxSpace):
    Passenger.__init__(self, name, xo, yo, xd, yd)
    self.__freespace = maxSpace
    self.__maxSpace = maxSpace
    self.__passengers = []

  def __copy__(self):
    newone = Driver(self.getName(),self.getOrigin()[0],self.getOrigin()[1],self.getDestination()[0],self.getDestination()[1],self.__maxSpace)
    newone.__dict__.update(self.__dict__)
    newone.setPassengers(copy(self.__passengers))
    return newone



  def isEmpty(self):
    return self.__freespace == self.__maxSpace


  def isFull(self):
    return self.__freespace == 0


  def getPassengers(self):
    return self.__passengers

  def setPassengers(self, p):
    self.__passengers = p

  def getMaxSpace(self):
    return self.__maxSpace

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
      d = MAX_KM
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
