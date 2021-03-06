#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

max_coordinate = 16384

def unit_generator():
    for x in [(0,1), (0,-1), (1,0), (-1,0)]:
        yield x

def print_output(*args):
    print("(o)", *args)

def print_error(*args):
    print("(e)", *args)

def print_warning(*args):
    print("(w)", *args)
