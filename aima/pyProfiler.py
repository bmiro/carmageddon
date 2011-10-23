import pstats
from sys import argv

p = pstats.Stats(argv[1])
q = p.sort_stats('time')
q.print_stats()