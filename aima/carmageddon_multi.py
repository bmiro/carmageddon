# -*- coding: utf-8 -*-
from utils import *
from search import *


from copy import copy

from passenger import *
from driver import *
from state import *

import threading
import os

import multiprocessing
import Queue 

myLock = threading.Lock()

def successorSwitch(qstate,qexit):
  print "successor"
  state = qstate.get()
  for p in state.getPassengers():
    currentDrv = state.whoPickuped(p)
      
    for d in state.getDrivers().iteritems():
      if d[0] != currentDrv and not d[1].isFull():
        newState = copy(state)
        newState.setDrivers(copy(state.getDrivers()))
        newState.setPassengers(copy(state.getPassengers()))
        newState.switchPassenger(p, d[0])
        qexit.put(("swi",newState))

def successorSwap(qstate,qexit):
  state = qstate.get()
  for p1 in state.getPassengers():
    for p2 in state.getPassengers():
      newState = copy(state)
      newState.setDrivers(copy(state.getDrivers()))
      newState.setPassengers(copy(state.getPassengers()))
      newState.swapPassengers(p1,p2)
      qexit.put(("swa",newState))


def successorDegradate(qstate,qexit):
  state = qstate.get()
  for d in state.getDrivers().itervalues():
    if d.isEmpty():
      for carrier in state.getDrivers().iteritems():
        if carrier[0] != d.getName() and not carrier[1].isFull():
          newState = copy(state)
          newState.setDrivers(copy(state.getDrivers()))
          newState.setPassengers(copy(state.getPassengers()))
          newState.degradateDriver(d.getName(), carrier[0])
          qexit.put(("dgr",newState))
          break



        
class Carmageddon(Problem):
  """ """
  def __init__(self, state):
    self.__state = state
    self.initial = state
    self.tr = None
  
  
  def successor(self, state):
    print state.getKm()
    qstate = multiprocessing.Queue()
    qexit = multiprocessing.Queue()
    qstate.put(state)
    qstate.put(state)
    qstate.put(state)
    p = multiprocessing.Process(target=successorSwitch, args=(qstate,qexit))
    p2 = multiprocessing.Process(target=successorSwap, args=(qstate,qexit))
    p3 = multiprocessing.Process(target=successorDegradate, args=(qstate,qexit))
    p.start()
    p2.start()
    p3.start()
    while p.is_alive() or p2.is_alive() or p3.is_alive():
      try:
        rt = qexit.get(False)
        yield rt
      except Queue.Empty:
        continue
    p.join()
    p2.join()
    p3.join()

  def goal_test(self, state):
    pass


    
  def value(self, node):
    return -node.state.getKm()
    """Heuristic function"""
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
  
  

