# -*- coding: utf-8 -*-
from utils import *
from search import *

from sys import argv
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
  
  if len(argv) != 5 and len(argv) != 4:
    print "Usage:"
    print " We engourage to use pypy in order to reduce execution time, it can be found at:"
    print "\t\t http://pypy.org \t https://launchpad.net/~pypy/+archive/ppa"
    print "\t python carmageddon.py M N InitialDistribution Algorism"
    print "\t # Where M N are integer that represents the number of user and drivers"
    print "\t # InitialDistribution can be allOneFirst or fullFirst"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy carmageddon.py 100 100 allOneFirst hillClimbing"
    print ""
    print "or"
    print "\t python carmageddon.py configfile.cfg Algorism"
    print "\t # Where configfile.cfg is a saved state"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy carmageddon.py states.cfg simulatedAnnealing"

    exit()
    
  alg = argv[-1] 
   
  if  len(argv) == 5:
    m = int(argv[1])
    n = int(argv[2])
  
    numDrivers = n
    numPassengers = m-n 
    
    s = State(nPassengers=numPassengers, nMaxDrivers=numDrivers, initialDistribution=argv[3])
  else:
    s = State(cfgfile=argv[2])
    
  c = Carmageddon(s)
  
  if alg == "hillClimbing":
    resul = hill_climbing(c)
  else:
    resul = simulated_annealing(c).state
  
  print resul
    
