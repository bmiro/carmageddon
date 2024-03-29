# -*- coding: utf-8 -*-

from passenger import *
from driver import *

from random import random, randint

from re import match, split, compile

MAX_KM = 30000

HUGE_VALUE = 10000

PES_VEHICLE = 10000000

class State(object):
  def __init__(self, nPassengers=30, nMaxDrivers=30, 
                     citySize=10000.0, squareSize=100.0, 
                     initialDistribution="fullFirst", 
                     cfgfile=None):

    self.__driverCount = 0
    self.__passengerCount = 0
    
    self.__nPassengers = nPassengers
    self.__nMaxDrivers = nMaxDrivers

    self.__citySize = citySize
    self.__squareSize = squareSize
    
    # Dict of drivers, driver name as key pointing to driver obcjet
    self.__carmageddons = {}
    
    #  Dict of passengeres, passenger name as key pointing to a tupla
    # of passenger object and driver name
    self.__passengers = {}
    
    if cfgfile != None:
      print "Loading form file"
      self.loadFromFile(cfgfile)
    else:
      self.genRandomState(initialDistribution, 3)

  ##########################################################
  ################# State generation Methods ###############
  ########################################################## 
  """ Allocs passengers in drivers, there are two criteria:
  " fullFirst:   that first full a driver before assigning a
  "             passenger to an emtpy driver
  " allOneFirst: that doesn't assing a N+1 passenger to a
  "             driver until all the driers has N passengers
  """
  def allocPassengersFullFirst(self, maxFullFirst):
    alloqued = 0
    for p in self.__passengers:
      for d in self.__carmageddons.itervalues():
	if len(d.getPassengers()) < maxFullFirst:
	  d.pickupPassenger(p)
	  self.__passengers[p] = (self.__passengers[p][0], d.getName())
	  alloqued += 1
	  break
    if alloqued != len(self.getPassengers()):
      print "There are unalloqued passengers!" #TODO throw exception
  
  
  def allocPassengersAllOneFirst(self):
    alloqued = 0
    it = 0
    for p in self.__passengers:
      for d in self.__carmageddons.itervalues():
	if len(d.getPassengers()) == it:
	  d.pickupPassenger(p)
	  
	  self.__passengers[p] = (self.__passengers[p][0], d.getName())
	  alloqued += 1
	  break
      if (alloqued % self.getNumDrivers()) == 0:
	it += 1
	
    if alloqued != len(self.getPassengers()):
      print "There are unalloqued passengers!" #TODO throw exception
  


  ##########################################################
  ################ Random generation Methods ###############
  ##########################################################   
  def genRandomState(self, criteria="fullFirst", maxFullFirst=3):
    for d in range(self.__nMaxDrivers):
      drv = self.genRandomDriver()
      self.__carmageddons[drv.getName()] = drv

    for p in range(self.__nPassengers):
      pss = self.genRandomPassenger()
      self.__passengers[pss.getName()] = (pss, None) 

    if criteria=="fullFirst":
      self.allocPassengersFullFirst(maxFullFirst)
    elif criteria=="allOneFirst":
      self.allocPassengersAllOneFirst()
    else:
      print "The criteria must match fullFrist or allOneFirst" 

    
  def genRandomDriver(self):
    name = str(self.__driverCount)
    name = '0'*(4-len(str(name))) + name
    d = Driver('D-' + name, randint(0, self.__citySize), \
                            randint(0, self.__citySize), \
                            randint(0, self.__citySize), \
                            randint(0, self.__citySize), 2)
    self.__driverCount += 1
    return d


  def genRandomPassenger(self):
    name = str(self.__passengerCount)
    name = '0'*(4-len(str(name))) + name
    p = Passenger('P-' + name, randint(0, self.__citySize), \
                               randint(0, self.__citySize), \
                               randint(0, self.__citySize), \
                               randint(0, self.__citySize))
    self.__passengerCount += 1
    return p


  ##########################################################
  #################### State info Methods ##################
  ##########################################################  
  def getDrivers(self):
    return self.__carmageddons


  def setDrivers(self, d):
    self.__carmageddons = d


  def getPassengers(self):
    return self.__passengers


  def setPassengers(self, p):
    self.__passengers = p


  def getNumPassengers(self):
    return len(self.__passengers)


  def getNumDrivers(self):
    return len(self.__carmageddons)


  def whoPickuped(self, passenger):
    return self.__passengers[passenger][1]
    
  def getKm(self):
    i = 0     
    for p in self.__carmageddons.itervalues():
      incr = p.getRouteWeight(self)
      if incr > MAX_KM:
        i += HUGE_VALUE*(incr-MAX_KM)
      i += incr
    return i

  def getKm_an(self):
    i = 0     
    for p in self.__carmageddons.itervalues():
      incr = p.getRouteWeight(self)
      if incr > MAX_KM:
        i += HUGE_VALUE*(incr-MAX_KM)
    return i
    
  def isGood(self):
    for d in self.getDrivers().itervalues():
      if d.getRouteWeight(self) > MAX_KM:
        return False
    return True

  ##########################################################
  #################### Operators Methods ###################
  ##########################################################
  """ Recives two key for each driver (degradated and carrier) """
  def degradateDriver(self, degradatedDriver, carrierDriver):
    if not self.__carmageddons[degradatedDriver].isEmpty():
      print "Trying to degradeta a not empty driver!" #TODO aixecar excepció
      return -1


    if self.getNumDrivers() == 0:
      print "You can not degradate the last driver!" # TODO aixecar excepció
      return -3

    d = self.__carmageddons.pop(degradatedDriver)
    d = copy(d)
    name = d.getName()
    name = name.replace('D', 'P')
    name = name.replace('-', 'D')
    p = Passenger(name, d.getOrigin()[0], d.getOrigin()[1], \
                        d.getDestination()[0], d.getDestination()[1])

    newdriver_pick = copy(self.__carmageddons[carrierDriver])
    self.__carmageddons[carrierDriver] = newdriver_pick
    self.__carmageddons[carrierDriver].pickupPassenger(name)
    self.__passengers[p.getName()] = (p, self.__carmageddons[carrierDriver].getName())
    
    
  """ Passenger is a passenger name and also newCarrier the new driver name """
  def switchPassenger(self, passenger, newCarrier):
    driver = self.__passengers[passenger][1]

    newdriver_leave = copy(self.__carmageddons[driver])
    self.__carmageddons[driver] = newdriver_leave
    self.__carmageddons[driver].leavePassenger(passenger)

    newdriver_pick = copy(self.__carmageddons[newCarrier])
    self.__carmageddons[newCarrier] = newdriver_pick
    self.__carmageddons[newCarrier].pickupPassenger(passenger)

    self.__passengers[passenger] = (self.__passengers[passenger][0], newCarrier)


  def swapPassengers(self, p1name, p2name):
    d1name = self.__passengers[p1name][1]
    d2name = self.__passengers[p2name][1]

    newDriverLeave = copy(self.__carmageddons[d1name])
    self.__carmageddons[d1name] = newDriverLeave
    self.__carmageddons[d1name].leavePassenger(p1name)
    self.__carmageddons[d1name].pickupPassenger(p2name)

    newDriverPick = copy(self.__carmageddons[d2name])
    self.__carmageddons[d2name] = newDriverPick
    self.__carmageddons[d2name].leavePassenger(p2name)
    self.__carmageddons[d2name].pickupPassenger(p1name)

    self.__passengers[p1name] = (self.__passengers[p1name][0], d2name)
    self.__passengers[p2name] = (self.__passengers[p2name][0], d1name)


  ####################################################
  #################### IO Methods ####################
  ####################################################
  def saveToFile(self, dstFile):
    f = open(dstFile, 'w')
    drivers = list(self.__carmageddons)
    drivers.sort()
    
    line = "## Declaring drivers\n"
    line += "##      name \t x0 \t y0 \t x1 \t y1 \t capacity \n"
    f.write(line)
    for drv in drivers:
      d = self.__carmageddons[drv]
      ori = d.getOrigin()
      dst = d.getDestination()
      line = "driver:\t" + d.getName() + "\t" + str(ori[0]) + "\t" + str(ori[1])
      line +=                            "\t" + str(dst[0]) + "\t" + str(dst[1])
      line += "\t"
      
      line = line + str(d.getMaxSpace()) + "\n"
      f.write(line)
      
    passengers = list(self.__passengers)
    passengers.sort()
    line = "\n\n## Declaring passengers\n"
    line += "##              name \t x0 \t y0 \t x1 \t y1 \n"
    f.write(line)
    for pss in passengers:
      p = self.__passengers[pss][0]
      ori = p.getOrigin()
      dst = p.getDestination()
      line = "passenger:\t" + p.getName() + "\t" + str(ori[0]) + "\t" + str(ori[1])
      line +=                               "\t" + str(dst[0]) + "\t" + str(dst[1])
      line += "\n"
      f.write(line)
      
      
    line = "\n\n## Who pickups who...\n"
    f.write(line)
    for drv in drivers:
      d = self.__carmageddons[drv]
      line = d.getName() + ":"
      for p in d.getPassengers():
        line += "\t" + p
        line += "\n"
        f.write(line)
    f.close()
    
    
  def loadFromFile(self, srcFile):
    drvRegex = compile(r"driver:\s+(?P<name>D-\d+)\s+(?P<xo>\d+)\s+(?P<yo>\d+)\s+(?P<xd>\d+)\s+(?P<yd>\d+)\s+(?P<maxspace>\d+)")
    pssRegex = compile(r"passenger:\s+(?P<name>P[-D]\d+)\s+(?P<xo>\d+)\s+(?P<yo>\d+)\s+(?P<xd>\d+)\s+(?P<yd>\d+)\s*")
    pckRegex = compile(r"(?P<driver>D-\d+):\s+((P[-D]\d+)\s+)*")
    
    f =  open(srcFile, 'r')      
    for line in f:
      m = drvRegex.match(line)
      if m:
        self.__carmageddons[m.group("name")] = Driver(m.group("name"), \
	                                    int(m.group("xo")), int(m.group("yo")), \
	                                    int(m.group("xd")), int(m.group("yd")), \
	                                    int(m.group("maxspace")))
      self.__driverCount += 1
      continue

      m = pssRegex.match(line)
      if m:
        self.__passengers[m.group("name")] = (Passenger(m.group("name"), \
	                              int(m.group("xo")), int(m.group("yo")), \
	                              int(m.group("xd")), int(m.group("yd"))), None)
        self.__passengerCount += 1
        continue
	
      m = pckRegex.match(line)
      if m:
        driver = m.group("driver")
        passengers = split("\s+", line)[1:][:-1]
        print passengers
        for p in passengers:
          self.__carmageddons[driver].pickupPassenger(p)
          self.__passengers[p] = (self.__passengers[p][0], driver)
    f.close()

  def __repr__(self):
    s = "\nDrivers info:\n"
    for c in self.__carmageddons:
      s += "\t" + c + " pickups: \n"
      if self.__carmageddons[c].isEmpty():
        s += "None\n"
      else:
        for p in self.__carmageddons[c].getPassengers():
          s += "\t\t" + p + "\n"
          
    s += "\n\nThe amount of distance is " + str(self.getKm())
    s += " and there are " + str(self.getNumDrivers()) + " drivers\n\n"
    if not self.isGood():
      s += "\tTHIS IS A BAD RESULT!! THERE ARE DRIVERS THAT ARRIVES TOO LATE!!\n"

    return s


