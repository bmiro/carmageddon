# -*- coding: utf-8 -*-

from sys import argv
from state import State

s = State(cfgfile=argv[1])
for d in s.getDrivers().itervalues():
  print d.printRoute(s)