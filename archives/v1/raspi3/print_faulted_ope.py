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
for ope in manip:
    if ope.get("plan.done") == "True":
        log = ope.get("log")
        if log.find("i=50 j=50 cnt=2500") == -1:
            if log.find("reboot") == -1:
                print(ope)
