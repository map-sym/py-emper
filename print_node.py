#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys
import sqlite3

from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 3:
    print_error("USAGE: %s <database> <node>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])
handler.enable_diagram()

try: nodename = handler.get_nodename(int(sys.argv[2]))
except ValueError: nodename = sys.argv[2]    

scale =  handler.get_parameter("scale")
pnumber = handler.calc_points(nodename)
if pnumber == 0:
    print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename))
    raise ValueError("wrong arg")

print_out("name: %s" % nodename)    
print_out("atoms: %s" % pnumber)
print_out("area: %g" % (scale * pnumber))

print_out("population:")
natffer = handler.select_many("SELECT name FROM nations")
for nation in natffer:
    query = "SELECT n_%s FROM nodes WHERE name='%s'" % (nation[0], nodename)
    number = handler.select_row(query, 0)
    if int(number[0]) > 0:
        print_out("\t%s: %d" % (nation[0], number[0]))

buffer = {}
for x,y in handler.nodepoints_generator(nodename):    
    for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        try:
            if handler.is_node(x+dx, y+dy, nodename):
                continue
            othernode = handler.diagram[(x+dx, y+dy)][0]
        except KeyError: continue
        try: buffer[othernode] += 1
        except KeyError: buffer[othernode] = 1

print_out("borders:")
for name in buffer.keys():
    print_out("\t%s: %d" % (name, buffer[name]))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)