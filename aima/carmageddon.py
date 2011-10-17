# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import deepcopy

from passenger import *
from driver import *
from state import *
        
class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
  
  
  def successor(self, state):
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    for p in state.getPassengers():
      currentDrv = state.whoPickuped(p)
      
      for d in state.getDrivers().iteritems():
	if d[0] != currentDrv and not d[1].isFull():
	  #Switch passenger to this driver
	  newState = deepcopy(state)
	  newState.switchPassenger(p, d[0])
	  yield newState
      
    #Gens all the driver deletions (gens at most (nDrivers-1)*(nDrivers-2) )
    print "Degradating drivres\n"
    for d in state.getDrivers().itervalues():
      if d.isEmpty():
	for carrier in state.getDrivers().iteritems():
	  if carrier[0] != d.getName() and not carrier[1].isFull():
	    newState = deepcopy(state)
	    newState.degradateDriver(d.getName(), carrier[0])
	    yield newState

  def goal_test(self, state):
    return False
    
    
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
  
  c = Carmageddon(s)
  for suc in c.successor(s):
    print(suc)
  
  

