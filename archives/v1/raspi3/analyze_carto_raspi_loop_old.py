import json
import numpy as np
import matplotlib as mpl
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
    parser.add_argument("--no-reboot", help="if the flag is set, only non rebooting effects will appear on the cartography", action="store_true")
    return parser.parse_args()

def safe_int_from_tab(tab, i):
    try:
        ret = int(tab[i])
    except (ValueError, IndexError):
        ret = -1
    return ret

def parse_log(log):
    log = log.split(" ")
    cnt = safe_int_from_tab(log, 1)
    i = safe_int_from_tab(log, 4)
    j = safe_int_from_tab(log, 7)
    return cnt, i, j

def build_matrix(manip, no_reboot):
    matrix = np.zeros(manip.get_size())
    cnt_values = []
    power_values = []
    for ope in manip:
        if ope.is_broken() == 0:
            if ope.get("plan.done") == "True":
                log = ope.get("log")
                if log.find("cnt: 250000 | i: 500 | j: 500") == -1:
                    if log.find("reboot") != -1 and no_reboot:
                        pass
                    else:
                        x_grid = int(ope.get("x_grid"))
                        y_grid = int(ope.get("y_grid"))
                        matrix[y_grid, x_grid] += 1
                        cnt, i, j = parse_log(log)
                        cnt_values.append(cnt)
                        power_values.append(ope.get("injector.P"))
    return matrix, cnt_values, power_values

def plot_matrix(matrix):
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.size"] = 12
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #colorbar
    bounds = np.linspace(matrix.min(), matrix.max(), matrix.max()-matrix.min()+1)
    cmap = plt.cm.jet
    cmap = plt.get_cmap("OrRd")
    norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5, matrix.max()+1+0.5, 1), cmap.N)
    cax = ax.matshow(matrix, cmap=cmap, norm=norm)
    fig.colorbar(cax, ticks=bounds)
    plt.show()

def plot_cnt_values(cnt_values):
    min_cnt = 0
    max_cnt = 250000
    dist = [0]*(max_cnt+1)
    for v in cnt_values:
        if (v >= 0) and (v <= 250000):
            dist[v] += 1
    for i,d in enumerate(dist):
        if d != 0:
            print("cnt = {} obtained {} times".format(i, d))

def plot_power_values(manip, power_values):
    powers = manip.get_params()['sweep']['injector']['P']
    dist = [0]*len(powers)
    for v in power_values:
        ind = powers.index(int(v))
        dist[ind] += 1
    for i,d in enumerate(dist):
        print("P = {}V faulted {} times".format(powers[i], d))

args = get_args()
manip_dir = args.manip_dir
if manip_dir[-1] != "/":
    manip_dir += "/"

manip = mm.manage_manip(manip_dir)
matrix, cnt_values, power_values = build_matrix(manip, args.no_reboot)
plot_matrix(matrix)
plot_cnt_values(cnt_values)
plot_power_values(manip, power_values)
