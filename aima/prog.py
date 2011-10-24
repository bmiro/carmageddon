# -*- coding: utf-8 -*-

from search import *
from sys import argv

from types import FunctionType

from carmageddon import Carmageddon
from state import State

from re import compile
from datetime import datetime

import prog

ITERATIONS = 10

""" Returns the best operator """
def test1_Operators():
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

  
def test2_Inits(operatorSet="1"):
  ############################################################################
  ############################## Test executions #############################
  ############################################################################
  
  ################################ allOneFirst ###############################
  i = 0
  op1Time = []
  op1Drivers = []
  op1Heuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " of all one first inicialization"
    s = State(nPassengers=100, nMaxDrivers=100, initialDistribution="allOneFirst")
    c = Carmageddon(s, "km", operatorSet)
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()    
    op1Time.append(tf - to)
    
    op1Drivers.append(finalState.getNumDrivers())
    op1Heuristic.append(c.printableHeuristic(finalState))
    i += 1
   
  ################################# fullfirst ################################
  i = 0
  op2Time = []
  op2Drivers = []
  op2Heuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " of all one first inicialization"
    s = State(nPassengers=100, nMaxDrivers=100, initialDistribution="fullFirst")
    c = Carmageddon(s, "km", operatorSet)
    
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
  
  print "\t\t Average results of \"all one first\" of operators"
  print "\t Average time: \t\t ", op1AvrTime
  print "\t Average drivers:\t\t ", op1AvrDrivers
  print "\t Average heuristic:\t\t ", op1AvrHeuristic
  print "\n\n"
  print "\t\t Average results of \"full first\" of operators"
  print "\t Average time: \t\t ", op2AvrTime
  print "\t Average drivers:\t\t ", op2AvrDrivers
  print "\t Average heuristic:\t\t ", op2AvrHeuristic
  
  if op1AvrHeuristic == op2AvrHeuristic:
    print "Both operators has the same heurístic resuluts!!!"
    return
  
  if op1AvrHeuristic < op2AvrHeuristic:
    best = "allOneFirst"
    worst = "fullFirst"
  else:
    best = "fullFirst"
    worst = "allOneFirst"
  print "The inicialization \"%s\" is better than operator set \"%s\"" % (best, worst)
  return best
  

def test3_SimulatedAnnealingParams(initDistrib="fullFirst"):
  lK = [1,5,25,125]
  ll = [0.1,0.01,0.001,0.0001]

  for kParameter in lK:
    for lParameter in ll:
      lcost = []
      for i in xrange(10):  
	s = State(nPassengers=100, nMaxDrivers=100, initialDistribution=initDistrib)
	c = Carmageddon(s, "km", "1")
	finalState = c.run('hillClimbing',kParameter,lParameter,100)
	lcost.append(c.printableHeuristic(finalState))
      print "Average solution cost for params k = "+str(kParameter)+", lambda = "+str(lParameter)+" :"
      print "\t",reduce(lambda x, y: x + y, lcost)/len(lcost)
      print ""
      
       
def test4_TemporalEvolution(operatorSet="1", initDistrib="fullFirst"):
  print "Starting test at: ", datetime.now()
  
  N = 100
  incn = 100
  results = []
  for i in range(5):
    M = N/2
    nP = M
    nD = N-M
    s = State(nPassengers=nP, nMaxDrivers=nD, initialDistribution=initDistrib)
    c = Carmageddon(s, "km", operatorSet)
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()
    
    results.append((N, M, (tf - to), c.printableHeuristic(finalState), finalState.getNumDrivers()))
    N += incn
    print "Iteration ", i, " takes ", results[-1][2], " with N ", N, " M ", M, " optimizit to " , results[-1][3], " and ", results[-1][3], " drivers"

  print "Test finishes at ", datetime.now()
    
  for i in results:
    print "With N = %d M = %d it takes %s seconds resulting in %d heuristic value and %d drivers" % i
  
  return results

def test5_SecondHeuristicPonderation():
  pass

def test6_HCvsSA(operatorSet="1", initDistrib="fullFirst", k=1, lam=0.001, lim=100):
  ############################################################################
  ############################## Test executions #############################
  ############################################################################
  
  ################################ HC - km ###############################
  i = 0
  hcKmTime = []
  hcKmDrivers = []
  hcKmDistance = []
  hcKmHeuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " HC - KM"
    s = State(nPassengers=10, nMaxDrivers=10, initialDistribution=initDistrib)
    c = Carmageddon(s, "km", operatorSet)
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()    
    hcKmTime.append(tf - to)
    
    hcKmDrivers.append(finalState.getNumDrivers())
    hcKmDistance.append(finalState.getKm())
    hcKmHeuristic.append(c.printableHeuristic(finalState))
    i += 1
   
  ################################# HC - veh ################################
  i = 0
  hcVehTime = []
  hcVehDrivers = []
  hcVehDistance = []
  hcVehHeuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " HC - VEH"
    s = State(nPassengers=10, nMaxDrivers=10, initialDistribution=initDistrib)
    c = Carmageddon(s, "veh", operatorSet)
    
    to = datetime.now()
    finalState = c.run("hillClimbing")
    tf = datetime.now()    
    hcVehTime.append(tf - to)
    
    hcVehDrivers.append(finalState.getNumDrivers())
    hcVehDistance.append(finalState.getKm())
    hcVehHeuristic.append(c.printableHeuristic(finalState))
    i += 1
    
  ################################# SA - km ################################
  i = 0
  saKmTime = []
  saKmDrivers = []
  saKmDistance = []
  saKmHeuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " SA - KM"
    s = State(nPassengers=10, nMaxDrivers=10, initialDistribution=initDistrib)
    c = Carmageddon(s, "km", operatorSet)
    
    to = datetime.now()
    finalState = c.run("simulatedAnnealing", k, lam, lim)
    tf = datetime.now()    
    saKmTime.append(tf - to)
    
    saKmDrivers.append(finalState.getNumDrivers())
    saKmDistance.append(finalState.getKm())
    saKmHeuristic.append(c.printableHeuristic(finalState))
    i += 1
    
  ################################# SA - veh ################################
  i = 0
  saVehTime = []
  saVehDrivers = []
  saVehDistance = []
  saVehHeuristic = []
  for execution in range(ITERATIONS):
    print "Executing iteration ", i, " SA - VEH"
    s = State(nPassengers=10, nMaxDrivers=10, initialDistribution=initDistrib)
    c = Carmageddon(s, "veh", operatorSet)
    
    to = datetime.now()
    finalState = c.run("simulatedAnnealing", k, lam, lim)
    tf = datetime.now()    
    saVehTime.append(tf - to)
    
    saVehDrivers.append(finalState.getNumDrivers())
    saVehDistance.append(finalState.getKm())
    saVehHeuristic.append(c.printableHeuristic(finalState))
    
  ## Stats
  hcKmAvrTime = reduce(lambda x, y: x + y, hcKmTime)/len(hcKmTime)
  hcKmAvrDrivers = reduce(lambda x, y: x + y, hcKmDrivers)/len(hcKmDrivers)
  hcKmAvrDistance = reduce(lambda x, y: x + y, hcKmDistance)/len(hcKmDistance)
  hcKmAvrHeuristic = reduce(lambda x, y: x + y, hcKmHeuristic)/len(hcKmHeuristic)
  
  hcVehAvrTime = reduce(lambda x, y: x + y, hcVehTime)/len(hcVehTime)
  hcVehAvrDrivers = reduce(lambda x, y: x + y, hcVehDrivers)/len(hcVehDrivers)
  hcVehAvrDistance = reduce(lambda x, y: x + y, hcVehDistance)/len(hcVehDistance)
  hcVehAvrHeuristic = reduce(lambda x, y: x + y, hcVehHeuristic)/len(hcVehHeuristic)
  
  saKmAvrTime = reduce(lambda x, y: x + y, saKmTime)/len(saKmTime)
  saKmAvrDrivers = reduce(lambda x, y: x + y, saKmDrivers)/len(saKmDrivers)
  saKmAvrDistance = reduce(lambda x, y: x + y, saKmDistance)/len(saKmDistance)
  saKmAvrHeuristic = reduce(lambda x, y: x + y, saKmHeuristic)/len(saKmHeuristic)
  
  saVehAvrTime = reduce(lambda x, y: x + y, saVehTime)/len(saVehTime)
  saVehAvrDrivers = reduce(lambda x, y: x + y, saVehDrivers)/len(saVehDrivers)
  saVehAvrDistance = reduce(lambda x, y: x + y, saVehDistance)/len(saVehDistance)
  saVehAvrHeuristic = reduce(lambda x, y: x + y, saVehHeuristic)/len(saVehHeuristic)
  
  print "\t\t Average results of \"HC - KM\" of operators"
  print "\t Average time: \t\t ", hcKmAvrTime
  print "\t Average drivers:\t\t ", hcKmAvrDrivers
  print "\t Average distance:\t\t ", hcKmAvrDistance
  print "\t Average heuristic:\t\t ", hcKmAvrHeuristic
  print "\t\t Average results of \"HC - VEH\" of operators"
  print "\t Average time: \t\t ", hcVehAvrTime
  print "\t Average drivers:\t\t ", hcVehAvrDrivers
  print "\t Average distance:\t\t ", hcVehAvrDistance
  print "\t Average heuristic:\t\t ", hcVehAvrHeuristic
  print "\n\n"
  print "\t\t Average results of \"SA - KM\" of operators"
  print "\t Average time: \t\t ", saKmAvrTime
  print "\t Average drivers:\t\t ", saKmAvrDrivers
  print "\t Average distance:\t\t ", saKmAvrDistance
  print "\t Average heuristic:\t\t ", saKmAvrHeuristic
  print "\t\t Average results of \"SA - VEH\" of operators"
  print "\t Average time: \t\t ", saVehAvrTime
  print "\t Average drivers:\t\t ", saVehAvrDrivers
  print "\t Average distance:\t\t ", saVehAvrDistance
  print "\t Average heuristic:\t\t ", saVehAvrHeuristic  
  

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
    print "\t # Optimizer can be km or veh"
    print "\t # OperatorSet can be 1 or 2"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy prog.py 200 100 allOneFirst km 1 hillClimbing"
    print ""
    print "or"
    print "\t python carmageddon.py configfile.cfg Optimizer OperatorSet Algorism"
    print "\t # Where configfile.cfg is a saved state"
    print "\t # Optimizer can be km or veh"
    print "\t # OperatorSet can be 1 or 2"
    print "\t # Algorism can be hillClimbing or simulatedAnnealing"
    print "\t Example: pypy prog.py states.cfg veh 2 simulatedAnnealing"

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
