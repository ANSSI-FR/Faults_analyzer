import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import parser.manage_manip as mm
import argparse

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
        print(ope)
