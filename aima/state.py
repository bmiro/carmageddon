# -*- coding: utf-8 -*-

from passenger import *
from driver import *

from random import random, randint

from re import match, split, compile

MAX_KM = 30000
ANIMALADA = 1000000000
PES_VEHICLE = 10000000

class State(object):
  def __init__(self, nPassengers=50 , nMaxDrivers=50, citySize=10000.0, squareSize=100.0, cfgfile=None):

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
      self.genRandomState()


  ##########################################################
  ################ Random generation Methods ###############
  ##########################################################   
  def genRandomState(self):
    for d in range(self.__nMaxDrivers):
      drv = self.genRandomDriver()
      self.__carmageddons[drv.getName()] = drv

    for p in range(self.__nPassengers):
      pss = self.genRandomPassenger()

      alloqued = False
      for c in self.__carmageddons.iterkeys():
        if len(self.__carmageddons[c].getPassengers()) < 2:
          self.__carmageddons[c].pickupPassenger(pss)
          self.__passengers[pss.getName()] = (pss, c)
          alloqued = True
          break

      if not alloqued:
        print "There are more passengers than free space!!!" #TODO raise exception
    
    
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
      i += p.getRouteWeight(p.getRoute(self))
    return i


  ##########################################################
  #################### Operators Methods ###################
  ##########################################################
  """ Recives two key for each driver (degradated and carrier) """
  def degradateDriver(self, degradatedDriver, carrierDriver): #TODO posar un nom mes guais
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
    self.__carmageddons[carrierDriver].pickupPassenger(p)
    self.__passengers[p.getName()] = (p, self.__carmageddons[carrierDriver].getName())
    
    
  """ Passenger is a passenger name and also newCarrier the new driver name """
  def switchPassenger(self, passenger, newCarrier):
    #TODO gestionar excepcions]
    p = self.__passengers[passenger][0]
    pname = self.__passengers[passenger][1]

    newdriver_leave = copy(self.__carmageddons[pname])
    self.__carmageddons[pname]=newdriver_leave
    self.__carmageddons[pname].leavePassenger(p)

    newdriver_pick = copy(self.__carmageddons[newCarrier])
    self.__carmageddons[newCarrier] = newdriver_pick
    self.__carmageddons[newCarrier].pickupPassenger(p)

    self.__passengers[passenger] = (p, newCarrier)


  def swapPassengers(self, p1name, p2name):
    p1 = self.__passengers[p1name][0]
    d1name = self.__passengers[p1name][1]

    p2 = self.__passengers[p2name][0]
    d2name = self.__passengers[p2name][1]

    newdriver_leave = copy(self.__carmageddons[d1name])
    self.__carmageddons[d1name]=newdriver_leave
    self.__carmageddons[d1name].leavePassenger(p1)
    self.__carmageddons[d1name].pickupPassenger(p2)


    newdriver_pick = copy(self.__carmageddons[d2name])
    self.__carmageddons[d2name] = newdriver_pick
    self.__carmageddons[d2name].leavePassenger(p2)
    self.__carmageddons[d2name].pickupPassenger(p1)

    self.__passengers[p1name] = (p1,d2name)
    self.__passengers[p2name] = (p2,d1name)


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
      line = "driver:\t" + d.getName() + "\t" + str(ori[X]) + "\t" + str(ori[Y])
      line =                      line + "\t" + str(dst[X]) + "\t" + str(dst[Y]) + "\t"
      
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
      line = "passenger:\t" + p.getName() + "\t" + str(ori[X]) + "\t" + str(ori[Y])
      line =                         line + "\t" + str(dst[X]) + "\t" + str(dst[Y]) + "\n"
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
	  self.__carmageddons[driver].pickupPassenger(self.__passengers[p][0])
	  self.__passengers[p] = (self.__passengers[p][0], driver)
	
    f.close()

  def __repr__(self):
    s = "Passenger info:\n"
    for p in self.__passengers:
      s += "\t" + p + " is pickuped by " + self.__passengers[p][1] + "\n"
    
    s += "\nDrivers info:\n"
    for c in self.__carmageddons:
      s += "\t" + c + " pickups: \n"
      if self.__carmageddons[c].isEmpty():
        s += "None\n"
      else:
        for p in self.__carmageddons[c].getPassengers():
          s += "\t\t" + p + "\n"
    return s


  def getKm(self):
    i = 0     
    for p in self.__carmageddons.itervalues():
      incr = p.getRouteWeight(p.getRoute(self))
      if incr > MAX_KM:
        i += ANIMALADA*incr
      i += incr
    return i


