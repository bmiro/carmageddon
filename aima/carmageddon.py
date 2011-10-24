# -*- coding: utf-8 -*-
from utils import *
from search import *

from sys import argv
import sys
from copy import copy

from passenger import *
from driver import *
from state import *

#import cProfile

""" Used only to call heuristic value in carmageddon object """
class DummyNode(object):
  def __init__(self, s):
    self.state = s   

class Carmageddon(Problem):
  """ """
  def __init__(self, state, h="km", operatorSet="1"):
    self.__state = state
    self.initial = state
    self.__operatorSet = operatorSet
    self.__h = h
    heuristic_dict = {"km" : self.heuristic_km, "veh" : self.heuristic_veh}
    self.value = heuristic_dict[h]
  
  def run(self, alg="hillClimbing", k=None, lam=None, lim=None):
    if alg == "hillClimbing":
      return hill_climbing(self)
    else:
      if k != None and lam != None and lim != None:
	params = exp_schedule(k, lam, lim)
	return simulated_annealing(self, params).state
      else:
	return simulated_annealing(self).state


  def successor(self, state):
    numberOp1 = 0
    numberOp2 = 0

    if self.__operatorSet == "1":
      for s in self.genPassengerSwitches(state):
        numberOp1 += 1
        yield s
      for s in self.genSoftDriverDegradations(state):
        numberOp2 += 1
        yield s

	
    elif self.__operatorSet == "2": 
      for s in self.genPassengerSwaps(state):
	numberOp1 += 1
	yield s
      for s in self.genHardDriverDegradations(state):
	numberOp2 += 1
	yield s
         
    print "#######################################"
    print "Nombre d'estats operador 1: ", numberOp1
    print "Nombre d'estats operador 2: ", numberOp2
    print "Nombre d'estats Total     : ", numberOp1 + numberOp2
    print "Heurístic                 : ", self.printableHeuristic(state)


  # Operator
  def genPassengerSwaps(self, state):    
    ltemp = list(state.getPassengers())
    for p1 in ltemp:
      for p2 in xrange(it,len(ltemp)):
        newState = copy(state)
        newState.setDrivers(copy(state.getDrivers()))
        newState.setPassengers(copy(state.getPassengers()))
        newState.swapPassengers(p1,ltemp[p2])
        yield ("swap", newState)
    
  # Operator
  def genPassengerSwitches(self, state):
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
          yield ("sw", newState)
          
  # Operator
  def genSoftDriverDegradations(self, state):
    #Gens all the empty driver deletions
    for d in state.getDrivers().itervalues():
      if d.isEmpty():
        for carrier in state.getDrivers().iteritems():
          if carrier[0] != d.getName():
            newState = copy(state)
            newState.setDrivers(copy(state.getDrivers()))
            newState.setPassengers(copy(state.getPassengers()))
            newState.degradateDriver(d.getName(), carrier[0])
            yield ("dgrd", newState)
            break
            
  # Operator
  def genHardDriverDegradations(self, state):
    #Gens all the driver deletions inserting it in the first not full driver.
    for d in state.getDrivers().itervalues():
      for carrier in state.getDrivers():
        if carrier != d.getName():
          newState = copy(state)
          newState.setDrivers(copy(state.getDrivers()))
          newState.setPassengers(copy(state.getPassengers()))
          # Distribution of passengers in other drivers
          for p in d.getPassengers():
            for anotherDriver in newState.getDrivers():
              if anotherDriver != d.getName():
          newState.switchPassenger(p, anotherDriver)
          # Puts the old driver as a passenger with the carrier driver.
          newState.degradateDriver(d.getName(), carrier)
          yield ("dgrd", newState)
          break
    
    
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

  def path_cost(self, c, state1, action, state2):
    return sys.maxint - self.printableHeuristic(state2)


