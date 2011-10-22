# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import copy

from passenger import *
from driver import *
from state import *

import gc
import datetime
   
""" Used only to call heuristic value in carmageddon object """
class DummyNode(object):
  def __init__(self, s):
    self.state = s   

class Carmageddon(Problem):
  """ """
  def __init__(self, state, h="km"):
    self.__state = state
    self.initial = state
    self.__h = h
    heuristic_dict = {"km" : self.heuristic_km, "veh" : self.heuristic_veh}
    self.value = heuristic_dict[h]
  
  
  def successor(self, state):
    numberOp1 = 0
    numberOp2 = 0
    numberOp3 = 0
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    for p in state.getPassengers():
      currentDrv = state.whoPickuped(p)
      
      for d in state.getDrivers().iteritems():
        if d[0] != currentDrv :
	  #Switch passenger to this driver
          newState = copy(state)
          newState.setDrivers(copy(state.getDrivers()))
          newState.setPassengers(copy(state.getPassengers()))
          newState.switchPassenger(p, d[0])
          #if newState.getKm() <= MAX_KM:
          numberOp1+= 1
          yield ("sw", newState)
      
     #Gens all the driver deletions inserting it in the first not full driver.
    for d in state.getDrivers().itervalues():
      if d.isEmpty():
        for carrier in state.getDrivers().iteritems():
          if carrier[0] != d.getName() :
            newState = copy(state)
            newState.setDrivers(copy(state.getDrivers()))
            newState.setPassengers(copy(state.getPassengers()))
            newState.degradateDriver(d.getName(), carrier[0])
            yield ("dgrd", newState)
            numberOp2+= 1
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
        numberOp3+= 1
        yield ("swap", newState)
      it+=1
    print "#######################################"
    print datetime.datetime.now()
    print "Nombre d'estats operador 1: ", numberOp1
    print "Nombre d'estats operador 2: ", numberOp2
    print "Nombre d'estats operador 3: ", numberOp3
    print "Nombre d'estats Total     : ", numberOp1 + numberOp2 + numberOp3
    print "Heurístic                 : ", self.printableHeuristic(state)


  def goal_test(self, state):
    pass
    
    
  def value(self, node):
    """Heuristic function"""
    pass
  
  
  def printableHeuristic(self, state):
    dn = DummyNode(state)   
    return -self.value(dn)

      
  def heuristic_km(self, node):
    """Heuristic function"""
    return -node.state.getKm()
    

  def heuristic_veh(self, node):
    """Heuristic function"""
    return -(node.state.getKm() + node.state.getNumDrivers()*PES_VEHICLE)



if __name__ == "__main__":
  #s = State(cfgfile="estat.pr")
  #s.saveToFile("estat.guardat2")
  
  s = State(initialDistribution="allOneFirst")
  print s
  #s.saveToFile("estat.pr")

  c = Carmageddon(s)
#  for suc in c.successor(s):
#    print(suc)
  f = hill_climbing(c)
  #c = Carmageddon(s)
#  for suc in c.successor(s):
#    print(suc)
  #f = simulated_annealing(c)
  #print f.getKm()
  #print f.getNumDrivers()
  #print Driver.t
  print f
  #for d in f.getDrivers().itervalues():
  #  print d.getRouteWeight(d.getRoute(f))
  
  
