import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os, sys, inspect
import time
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import parser.manage_manip as mm
from plotter.plotter import Plotter

def safe_int(v):
    try:
        ret = int(v)
    except ValueError:
        ret = -1
    return ret

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="Directory which stores the results of the manip")
    manip_dir = parser.parse_args().manip_dir
    if manip_dir[-1] != "/":
        manip_dir += "/"
    return manip_dir

def get_points(manip):
    delays = []
    values = []
    manip.refresh_results()
    for ope in manip:
        if ope.get("plan.done") == True:
            log = ope.get("log")
            if (log.find("reboot") == -1) and (log.find("cnt=2500") == -1):
                cnt = log.split(" ")[2].split("=")[1]
                if cnt[-1] == "'":
                    cnt = safe_int(cnt[:-1])
                else:
                    cnt = safe_int(cnt)
                if cnt <= 3000:
                    delay = float(ope.get("injector.D"))*1e6
                    delays.append(delay)
                    values.append(cnt)
    return [delays, values]

def get_faults_and_reboots(manip):
    reboots = 0
    faults = 0
    manip.refresh_results()
    for ope in manip:
        if ope.get("plan.done") == True:
            log = ope.get("log")
            if log.find("reboot") != -1:
                reboots += 1
            if (log.find("reboot") == -1) and (log.find("cnt=2500") == -1):
                faults += 1
    return [reboots, faults]

def build_to_plot(manip):
    cnt_vs_delay = get_points(manip)
    reboots_and_faults = get_faults_and_reboots(manip)
    to_plot = [
        {
            "type": "scatter",
            "data": cnt_vs_delay,
            "x_label": "Delay ($\mu$s)",
            "y_label": "cnt"
        },
        {
            "type": "bar",
            "data": reboots_and_faults,
            "x_ticklabels": ["Reboots", "Faults"],
            "show_data_value": True
        }
    ]
    return to_plot

manip_dir = get_args()
manip = mm.manage_manip(manip_dir)
to_plot = build_to_plot(manip)
suptitle = "Trace delay cartography \"{}\"".format(manip_dir)
pl = Plotter(to_plot, figsuptitle="", nb_to_plot=len(to_plot))
pl.init_plot()
while 1:
    pl.set_to_plot(build_to_plot(manip))
    pl.show(blocking=False)
    time.sleep(0.5)
