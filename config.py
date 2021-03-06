#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import optparse, os
import ToolBox

parser = optparse. OptionParser()
parser.add_option("-f", "--db-file", dest="dbfile",
                  metavar="FILE", default="demo.sql",
                  help="saved simulator state")
parser.add_option("-d", "--delete", dest="delete",
                  action="store_true", default=False,
                  help="delete parameter")
parser.add_option("-p", "--poor", dest="poor",
                  action="store_true", default=False,
                  help="poor mode to print parameter")
parser.add_option("-n", "--name", dest="name",
                  help="parameter name")
parser.add_option("-v", "--value", dest="value",
                  help="parameter value")

opts, args = parser.parse_args()
if opts.delete and opts.value:
    raise TypeError("(e) set and delete")

###
### main
###

import BusyBoxSQL
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)

if opts.name is not None:
    if opts.delete:
        driver.delete_config_by_name(opts.name)
    elif opts.value is not None:
        driver.set_config_by_name(opts.name, opts.value)
    else:
        value = driver.get_config_by_name(opts.name)
        if opts.poor: print(value)
        else: ToolBox.print_output(f"{opts.name}: {value}")
else:
    dout = driver.get_config_as_dict()
    for name in sorted(dout.keys()):
        ToolBox.print_output(f"{name}: {dout[name]}")
