import sys
import pandas as pd
import numpy as np
import argparse
import time

sys.path.append("/media/manip_local/raspi3_manip_liblsc/liblsc")

from manip_utils import calcer
from manip_utils import plotter
from manip_utils import bin_utils as bu

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    manip_dir = parser.parse_args().manip_dir
    if manip_dir[-1] != "/":
        manip_dir = manip_dir + "/"
    return manip_dir

rules = {"plots": [
    {
        "title": "Progress",
        "type": "matrix",
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid",
        "compute": lambda i: i["plan_done"]
    },
    {
        "title": "Reboots",
        "type": "matrix",
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid",
        "compute": lambda i: i["plan_done"] and i["reboot"]
    },
    {
        "title": "Faults",
        "type": "matrix",
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid",
        "compute": lambda i: i["plan_done"] and i["fault"]
    }
]}

manip_dir = get_args()
master_file = manip_dir + "main.csv"
df = pd.read_csv(master_file, error_bad_lines=False)

to_plot = calcer.work(df, rules)
pl = plotter.Plotter(to_plot, figsuptitle="")
pl.init_plot()
while 1:
    df = pd.read_csv(master_file, error_bad_lines=False)
    pl.set_to_plot(calcer.work(df, rules))
    pl.show(blocking=False)
