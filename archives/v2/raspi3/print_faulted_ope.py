import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import parser.manage_manip as mm

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    return parser.parse_args()

args = get_args()
manip_dir = args.manip_dir
if manip_dir[-1] != "/":
    manip_dir += "/"

manip = mm.manage_manip(manip_dir)
nb_faults = 0
for ope in manip:
    if ope.get("fault") == True:
        print(ope)
        nb_faults += 1

print("{} faults".format(nb_faults))
