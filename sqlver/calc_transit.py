#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys, os
import sqlite3, math
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 5:
    print_error("USAGE: %s <database> <start> <proxy> <stop>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])    
handler.enable_diagram()

try: startname = handler.get_nodename(int(sys.argv[2]))
except ValueError: startname = sys.argv[2]    

try: proxyname = handler.get_nodename(int(sys.argv[3]))
except ValueError: proxyname = sys.argv[3]    

try: stopname = handler.get_nodename(int(sys.argv[4]))
except ValueError: stopname = sys.argv[4]    

print_info("%s -> %s -> %s" % (startname, proxyname, stopname))
transit_cost = handler.calc_transit(startname, proxyname, stopname)
print_info("transit cost: %s" % transit_cost)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
