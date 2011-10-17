# -*- coding: utf-8 -*-

class Passenger(object):
  def __init__(self, name, xo, yo, xd, yd):
    self.__name = name
    self.__xo = xo
    self.__yo = yo
    self.__xd = xd
    self.__yd = yd


  def getDestination(self):
    return (self.__xd, self.__yd)


  def getOrigin(self):
    return (self.__xo, self.__yo)


  def getName(self):
    return self.__name
