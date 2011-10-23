# -*- coding: utf-8 -*-

from search import *
from sys import argv

from types import FunctionType

from carmageddon import Carmageddon
from state import State

from re import compile
from datetime import datetime

import prog

ITERATIONS = 2

""" Returns the best operator """
def test1_Operators():
  stats = {}
  stats['exec_time'] = 0
  stats['heuristic'] = 0
  stats['drivers'] = 0
  
  ############################################################################
  ############################## Test executions #############################
  ############################################################################
  
  ################################### Set 1 ##################################
  i = 0
  op1Time = []
  op1Drivers = []
  op1Heuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " of Set 1"
    s = State(nPassengers=100, nMaxDrivers=100, initialDistribution="allOneFirst")
    c = Carmageddon(s, "km", "1")
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()    
    op1Time.append(tf - to)
    
    op1Drivers.append(finalState.getNumDrivers())
    op1Heuristic.append(c.printableHeuristic(finalState))
    i += 1
   
  ################################### Set 2 ###################################
  i = 0
  op2Time = []
  op2Drivers = []
  op2Heuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " of Set 2"
    s = State(nPassengers=100, nMaxDrivers=100, initialDistribution="allOneFirst")
    c = Carmageddon(s, "km", "2")
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()    
    op2Time.append(tf - to)
    
    op2Drivers.append(finalState.getNumDrivers())
    op2Heuristic.append(c.printableHeuristic(finalState))
    i += 1
    
  
  ## Stats
  op1AvrTime = reduce(lambda x, y: x + y, op1Time)/len(op1Time)
  op1AvrDrivers = reduce(lambda x, y: x + y, op1Drivers)/len(op1Drivers)
  op1AvrHeuristic = reduce(lambda x, y: x + y, op1Heuristic)/len(op1Heuristic)
  
  op2AvrTime = reduce(lambda x, y: x + y, op2Time)/len(op2Time)
  op2AvrDrivers = reduce(lambda x, y: x + y, op2Drivers)/len(op2Drivers)
  op2AvrHeuristic = reduce(lambda x, y: x + y, op2Heuristic)/len(op2Heuristic)
  
  print "\t\t Average results of set1 of operators"
  print "\t Average time: \t\t ", op1AvrTime
  print "\t Average drivers:\t\t ", op1AvrDrivers
  print "\t Average heuristic:\t\t ", op1AvrHeuristic
  print "\n\n"
  print "\t\t Average results of set2 of operators"
  print "\t Average time: \t\t ", op2AvrTime
  print "\t Average drivers:\t\t ", op2AvrDrivers
  print "\t Average heuristic:\t\t ", op2AvrHeuristic
  
  if op1AvrHeuristic == op2AvrHeuristic:
    print "Both operators has the same heurístic resuluts!!!"
    return
  
  if op1AvrHeuristic < op2AvrHeuristic:
    best = "1"
    worst = "2"
  else:
    best = "2"
    worst = "1"
  print "The operator set %s is better than operator set %s" % (best, worst)
  return best

  
def test2_Inits():
  print "Test 2"

def test3_SimulatedAnnealingParams():
  print "Test 3"

def test4_TemporalEvolution():
  print "Test 4"

def test5_SecondHeuristicPonderation():
  print "Test 5"

def test6_HCvsSA():
  print "Test 6"

def test7_MNproportion():
  print "Test 7"


if __name__ == "__main__":
  print "\n\n\nUsage:"
  print "If one parameter is given it executes the corresponding test, the parameter is an \
  integer form 1 to 7."
  print ""
  print "If more parameters are given it will execute single"

  if len(argv) == 2:
    funcs = []
    testRegex = compile(r"test")
    for funcName in dir(prog):
      if isinstance(prog.__dict__.get(funcName), FunctionType):
	if testRegex.match(funcName):
	  funcs.append(prog.__dict__[funcName])
    
    funcs[int(argv[1])-1]()
    exit()
	

  if len(argv) != 7 and len(argv) != 6:
    print "Usage:"
    print " We engourage to use pypy in order to reduce execution time, it can be found at:"
    print "\t\t http://pypy.org \t https://launchpad.net/~pypy/+archive/ppa\n\b"
    print "\t python carmageddon.py N M InitialDistribution Optimizer OperatorSet Algorism\n"
    print "\t # Where N M are integer that represents the number of users and the non-drivers"
    print "\t # InitialDistribution can be allOneFirst or fullFirst"
    print "\t # Optimizer can be km or drv"
    print "\t # OperatorSet can be 1 or 2"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy carmageddon.py 200 100 allOneFirst km 1 hillClimbing"
    print ""
    print "or"
    print "\t python carmageddon.py configfile.cfg Optimizer OperatorSet Algorism"
    print "\t # Where configfile.cfg is a saved state"
    print "\t # Optimizer can be km or drv"
    print "\t # OperatorSet can be 1 or 2"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy carmageddon.py states.cfg drv 2 simulatedAnnealing"

    exit()
    
  alg = argv[-1]
  operatorSet = argv[-2]
  optimizer = argv[-3]
   
  if  len(argv) == 7:
    m = int(argv[2])
    n = int(argv[1])
  
    numDrivers = n-m
    numPassengers = m 
    
    print "There are " + str(numPassengers) + " passengers and " + str(numDrivers) + " drivers." 
    s = State(nPassengers=numPassengers, nMaxDrivers=numDrivers, initialDistribution=argv[3])
  else:
    s = State(cfgfile=argv[2])
    
  c = Carmageddon(s, optimizer, operatorSet)
  print c.run(alg)
