# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import copy

from passenger import *
from driver import *
from state import *
        
class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
    self.initial = state
  
  
  def successor(self, state):
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    for p in state.getPassengers():
      currentDrv = state.whoPickuped(p)
      
      for d in state.getDrivers().iteritems():
        if d[0] != currentDrv and not d[1].isFull():
	  #Switch passenger to this driver
	  newState = copy(state)
          newState.setDrivers(copy(state.getDrivers()))
          newState.setPassengers(copy(state.getPassengers()))
	  newState.switchPassenger(p, d[0])
	  if newState.getKm() <= MAX_KM:
	    yield ("sw", newState)
      
     #Gens all the driver deletions inserting it in the first not full driver.
    print "Degradating drivres\n"
    for d in state.getDrivers().itervalues():
      if d.isEmpty():
	for carrier in state.getDrivers().iteritems():
	  if carrier[0] != d.getName() and not carrier[1].isFull():
	    newState = copy(state)
            newState.setDrivers(copy(state.getDrivers()))
            newState.setPassengers(copy(state.getPassengers()))
	    newState.degradateDriver(d.getName(), carrier[0])
	    yield ("dgrd", newState)
            break

  def goal_test(self, state):
    pass
    
    
  def value(self, node):
    """Heuristic function"""
    return -node.state.getKm()
    pass


if __name__ == "__main__":
  s = State()
  print s
  s.saveToFile("estat.guardat")


