# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import copy

from passenger import *
from driver import *
from state import *


        
class Carmageddon(Problem):
  """ """
  def __init__(self, state, h = "km"):
    self.__state = state
    self.initial = state
    heuristic_dict = {"km":self.heuristic_km,"veh":self.heuristic_veh}
    self.value = heuristic_dict[h]
  
  
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
          #if newState.getKm() <= MAX_KM:
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

    it = 0
    print "iyy"
    ltemp = list(state.getPassengers())
    for p1 in ltemp:
      for p2 in xrange(it,len(ltemp)):
        newState = copy(state)
        newState.setDrivers(copy(state.getDrivers()))
        newState.setPassengers(copy(state.getPassengers()))
        newState.swapPassengers(p1,ltemp[p2])
        #if newState.getKm() <= MAX_KM:
        yield ("swap", newState)
      it+=1


  def goal_test(self, state):
    pass
    
    
  def value(self, node):
    """Heuristic function"""
    pass

  def heuristic_km(self, node):
    """Heuristic function"""
    return -node.state.getKm()

  def heuristic_veh(self, node):
    """Heuristic function"""
    return -(node.state.getKm()+node.state.getNumDrivers()*PES_VEHICLE)



if __name__ == "__main__":
  #s = State(cfgfile="estat.guardat")
  #s.saveToFile("estat.guardat2")
  
  #s.saveToFile("estat.guardat")
  s = State()
  c = Carmageddon(s)
#  for suc in c.successor(s):
#    print(suc)
  f = hill_climbing(c)
  #c = Carmageddon(s)
#  for suc in c.successor(s):
#    print(suc)
  #f = simulated_annealing(c)
  print f.getKm()
  print f.getNumDrivers()
  #print f
  #for d in f.getDrivers().itervalues():
  #  print d.getRouteWeight(d.getRoute(f))
  
  
