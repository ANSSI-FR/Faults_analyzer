import sys
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

import plotter

sys.path.append("/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")

from manip_utils import calcer
from manip_utils import bin_utils as bu

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    manip_dir = parser.parse_args().manip_dir
    if manip_dir[-1] != "/":
        manip_dir = manip_dir + "/"
    return manip_dir

def is_faulted(ope):
    return (ope["plan_done"] and ope["fault"])

def is_reboot(ope):
    return (ope["plan_done"] and ope["reboot"])

def is_faulted_exploitable(ope):
    if is_faulted(ope):
        if np.isnan(ope["i"]) or np.isnan(ope["j"]) or np.isnan(ope["cnt"]):
            return False
        else:
            return True

def is_done(ope):
    return ope["plan_done"]

rules = {"plots": [
    {
        "title": "",
        "type" : "matrix",
        "compute": is_reboot,
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid"
    },
    {
        "title": "Faults",
        "type" : "matrix",
        "compute": is_faulted,
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid"
    },
    {
        "title": "Exploitable Faults",
        "type" : "matrix",
        "compute": is_faulted_exploitable,
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid"
    },
    {
        "title": "Done",
        "type" : "matrix",
        "compute": is_done,
        "matrix_x": "plan_xgrid",
        "matrix_y": "plan_ygrid"
    }
]}

manip_dir = get_args()
master_file = manip_dir + "main.csv"

df = pd.read_csv(master_file, error_bad_lines=False)

to_plot = calcer.work(df, rules)

pl = plotter.Plotter(to_plot)
#pl.set_colormap(plt.get_cmap("OrRd"))
pl.export_tikz("tikz/rasp_exploitable_loop_faults.tex")
pl.show()
