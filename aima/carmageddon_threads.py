# -*- coding: utf-8 -*-
from utils import *
from search import *

from copy import copy

from passenger import *
from driver import *
from state import *

import threading

myLock = threading.Lock()

class successorSwitch(threading.Thread):
  def __init__(self,state,l):
    threading.Thread.__init__(self)
    self.state = state
    self.l = l
    
  def run(self):
    for p in self.state.getPassengers():
      currentDrv = self.state.whoPickuped(p)
        
      for d in self.state.getDrivers().iteritems():
        if d[0] != currentDrv and not d[1].isFull():
	    #Switch passenger to this driver
          newState = copy(self.state)
          newState.setDrivers(copy(self.state.getDrivers()))
          newState.setPassengers(copy(self.state.getPassengers()))
          newState.switchPassenger(p, d[0])
          with myLock:
            self.l.append( newState)


class successorSwap(threading.Thread):
  def __init__(self,state,l):
    threading.Thread.__init__(self)
    self.state = state
    self.l = l

  def run(self):
    for p1 in self.state.getPassengers():
      for p2 in self.state.getPassengers():
        newState = copy(self.state)
        newState.setDrivers(copy(self.state.getDrivers()))
        newState.setPassengers(copy(self.state.getPassengers()))
        newState.swapPassengers(p1,p2)
        with myLock:
          self.l.append(newState)


class successorDegradate(threading.Thread):
  def __init__(self,state,l):
    threading.Thread.__init__(self)
    self.state = state
    self.l = l
  def run(self):
    for d in self.state.getDrivers().itervalues():
      if d.isEmpty():
        for carrier in self.state.getDrivers().iteritems():
          if carrier[0] != d.getName() and not carrier[1].isFull():
            newState = copy(self.state)
            newState.setDrivers(copy(self.state.getDrivers()))
            newState.setPassengers(copy(self.state.getPassengers()))
            newState.degradateDriver(d.getName(), carrier[0])
            with myLock:
              self.l.append ( newState)
            break

        
class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
    self.initial = state
  
  
  def successor(self, state):
    print state.getKm()
    #Gens all the passenger changes (gens at most nPassengers*nDrivers states)
    l = list()
    myPr = successorSwitch(state,l)
    myPr2 = successorSwap(state,l)
    myPr3 = successorDegradate(state,l)
    myPr.start()
    myPr2.start()
    myPr3.start()
    myPr.join()
    myPr2.join()
    myPr3.join()
    for rt in l:
      yield ("sw",rt)


    print "joined"


 
     #Gens all the driver deletions inserting it in the first not full driver.



  def goal_test(self, state):
    pass
    
    
  def value(self, node):
    """Heuristic function"""
    return -node.state.getKm()
    pass


if __name__ == "__main__":
  print "hola"
  #p = Passenger("joan", 1, 1, 9, 9)
  #d = Driver("bernat", 0, 0, 10, 10, 2)


  #d.pickupPassenger(p)
  #r = d.getRoute(s)
  #print r
  #print d.getRouteWeight(r)


  #print s
  s = State()
  print s
  c = Carmageddon(s)
#  for suc in c.successor(s):
#    print(suc)
#  f = simulated_annealing(c)
  f = hill_climbing(c)
 # print f.getKm()
  print f
  #for d in f.getDrivers().itervalues():
  #  print d.getRouteWeight(d.getRoute(f))
  
  


