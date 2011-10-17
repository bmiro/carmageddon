# -*- coding: utf-8 -*-

from passenger import *
from driver import *

from random import random, randint

class State(object):
  def __init__(self, nPassengers=100, nMaxDrivers=60, citySize=10000.0, squareSize=100.0):

    self.__citySize = citySize
    self.__squareSize = squareSize
    
    # Dict of drivers, driver name as key pointing to driver obcjet
    self.__carmageddons = {}
    
    #  Dict of passengeres, passenger name as key pointing to a tupla
    # of passenger object and driver name
    self.__passengers = {}

    for d in range(nMaxDrivers):
      drv = self.genRandomDriver()
      self.__carmageddons[drv.getName()] = drv

    for p in range(nPassengers):
      pss = self.genRandomPassenger()

      alloqued = False
      for c in self.__carmageddons.iterkeys():
        if not self.__carmageddons[c].isFull():
          self.__carmageddons[c].pickupPassenger(pss)
          self.__passengers[pss.getName()] = (pss, c)
          alloqued = True
          break

      if not alloqued:
        print "There are more passengers than free space!!!" #TODO raise exception
 
 
  def genRandomDriver(self):
    d = Driver('D-' + str(random())[2:8], randint(0, self.__citySize), \
                                          randint(0, self.__citySize), \
                                          randint(0, self.__citySize), \
                                          randint(0, self.__citySize), 2)
    return d


  def genRandomPassenger(self):
    p = Passenger('P-' + str(random())[2:8], randint(0, self.__citySize), \
                                             randint(0, self.__citySize), \
                                             randint(0, self.__citySize), \
                                             randint(0, self.__citySize))
    return p


  def getDrivers(self):
    return self.__carmageddons


  def getPassengers(self):
    return self.__passengers


  def getNumPassengers(self):
    return len(self.__passengers)


  def getNumDrivers(self):
    return len(self.__carmageddons)


  """ Recives two key for each driver (degradated and carrier) """
  def degradateDriver(self, degradatedDriver, carrierDriver): #TODO posar un nom mes guais
    if not self.__carmageddons[degradatedDriver].isEmpty():
      print "Trying to degradeta a not empty driver!" #TODO aixecar excepció
      return -1

    if self.__carmageddons[carrierDriver].isFull():
      print "The carrier driver is full" #TODO aixecar excepció
      return -2

    if self.getNumDrivers() == 0:
      print "You can not degradate the last driver!" # TODO aixecar excepció
      return -3

    d = self.__carmageddons.pop(degradatedDriver)
    name = d.getName()
    name = name.replace('D', 'P')
    name = name.replace('-', 'D')
    p = Passenger(name, d.getOrigin()[0], d.getOrigin()[1], \
                        d.getDestination()[0], d.getDestination()[1])

    self.__carmageddons[carrierDriver].pickupPassenger(p)
    self.__passengers[p.getName()] = (p, self.__carmageddons[carrierDriver].getName())
    
    
  """ Passenger is a passenger name and also newCarrier the new driver name """
  def switchPassenger(self, passenger, newCarrier):
    #TODO gestionar excepcions]
    p = self.__passengers[passenger][0]
    self.__carmageddons[self.whoPickuped(passenger)].leavePassenger(p)
    self.__carmageddons[newCarrier].pickupPassenger(p)
    self.__passengers[passenger] = (p, newCarrier)
    


  def whoPickuped(self, passenger):
    return self.__passengers[passenger][1]


  def __repr__(self):
    s = ""
    
    s += "Passenger info:\n"
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
