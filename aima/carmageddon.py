# -*- coding: utf-8 -*-
from utils import *;
from search import *;

# Macros for easy indexation of coor tuples.
# i.e. a[X] -> xcoor
X = 0
Y = 1

def distance(src, dst):
  return abs(src[X] - dst[X]) + abs(src[Y] - dst[Y])

class Passenger(object):
  def __init__(self, name, xo, yo, xd, yd):
    self.__name = name
    self.__xo = xo
    self.__yo = yo
    self.__xd = xd
    self.__yd = yd

  def getDestination():
    return (self.__xd, self.__yd)

  def getOrigin():
    return (self.__xo, self.__yo)

class Driver(Passenger):
  def __init__(self, name, xo, yo, xd, yd, freespace):
    self.__name = name
    self.__xo = xo
    self.__yo = yo
    self.__xd = xd
    self.__yd = yd
    self.__freespace = freespace
    self.__passengers = []

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
      checkpoints.[self.__passengers.getOrigin] = self.__passengers.getDestination

    current = [self.getOrigin(), "DriverOrigin"]
    while not empty(checkpoints):
      # Searching nearst point
      d = MAX_DIST
      nearest = []
      for c in checkpoints.keys():
        if distance(current, c) < d:
          d = distance(current, c)
          nearest = c
          
      route.append(current)
      dest = checkpoints.pop(c)
      if dest != None:
        checkpoints[dest] = None
        event = "PickupPassenger"
      else:
        event = "LeavePassenger"
      current = [c, event]   

    route.append([self.getDestination, "DriverDestination"])
    return route

  def getRouteWeight(route):
    w = 0
    current = route[0][0]
    for p in route:
      w += distance(current, p[0])
      current = p[0]
    return w



class State(object):
  def __init__(self, nPassenger=16, nMaxDrivers=8, citySize=10000.0, squareSize=100.0):
    
  
  
  def genRandom():
    pass
  


class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    pass
  
  def successor(self, state):
    pass

  def goal_test(self, state):
    pass
    
  def value(self, node):
    """Heuristic function"""
    pass
