import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import parser.manage_manip as mm

def export_data_for_latex(x_values, y_values, filename):
    if(len(x_values) != len(y_values)):
        print("Error X et Y lengths are not matching ({} and {})".format(len(x_values), len(y_values)))
        return -1
    f = open(filename, "w")
    for i, x in enumerate(x_values):
        data = "{} {}\n".format(x_values[i], y_values[i])
        f.write(data)
    f.close()

def safe_int(v):
    try:
        ret = int(v)
    except ValueError:
        ret = -1
    return ret

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    parser.add_argument("-np", "--no-plot", help="don't plot data", action="store_true")
    parser.add_argument("-e", "--export", help="export data in the specified file", type=str)
    return parser.parse_args()

def comp_delays(manip):
    delays = manip.get_params()['sweep']['injector']['D']
    means = []
    mean = 0
    nb_values = 0
    for delay in delays:
        for ope in manip:
            if (ope.is_broken() == 0) and (ope.get("plan.done") == True):
                log = ope.get("log")
                if (log.find("reboot") == -1) and (log.find("cnt=2500") == -1):
                    if float(ope.get("injector.D")) == delay:
                        cnt = safe_int(log.split("=")[-1][:-1])
                        if cnt != -1:
                            mean += cnt
                            nb_values += 1
        if nb_values != 0:
            mean = mean / nb_values
            if mean <= 2500:
                means.append(mean)
            else:
                means.append(0)
            mean = 0
            nb_values = 0

    return means, delays

def get_points(manip):
    delays = []
    values = []
    i_values = []
    cnt_i_values = []
    i_delays = []
    j_values = []
    j_delays = []
    delays_fault = []
    for ope in manip:
        if (ope.is_broken() == 0) and (ope.get("plan.done") == True):
            log = ope.get("log")
            if (log.find("reboot") == -1) and (log.find("cnt=2500") == -1):
                cnt = log.split(" ")[2].split("=")[1]
                if cnt[-1] == "'":
                    cnt = safe_int(cnt[:-1])
                else:
                    cnt = safe_int(cnt)
                if cnt <= 2500:
                    delay = float(ope.get("injector.D"))*1e6
                    delays.append(delay)
                    values.append(cnt)

                i = safe_int(log.split("=")[1].split(" ")[0])
                if i <= 2500:
                    delay = float(ope.get("injector.D"))*1e6
                    cnt = log.split(" ")[2].split("=")[1]
                    if cnt[-1] == "'":
                        cnt = safe_int(cnt[:-1])
                    else:
                        cnt = safe_int(cnt)
                    i_delays.append(delay)
                    i_values.append(i)
                    cnt_i_values.append(cnt)

                j = safe_int(log.split("=")[2].split(" ")[0])
                if j <= 2500:
                    delay = float(ope.get("injector.D"))*1e6
                    j_delays.append(delay)
                    j_values.append(j)
                delay = float(ope.get("injector.D"))*1e6
                delays_fault.append(delay)

    return values, delays, i_values, i_delays, j_values, j_delays, cnt_i_values, delays_fault

def print_means_per_delay(means, delays):
    if len(delays) != len(means):
        for i in range(len(delays)-len(means)):
            means.append(0)
    for i,delay in enumerate(delays):
        delays[i] = delay*1e9
    print(means)
    print(delays)
    plt.scatter(delays, means, s=10)
    plt.show()

args = get_args()
manip_dir = args.manip_dir
if manip_dir[-1] != "/":
    manip_dir += "/"

manip = mm.manage_manip(manip_dir)
values, delays, i_values, i_delays, j_values, j_delays, cnt_i_values, delays_fault = get_points(manip)

if args.export:
    export_data_for_latex(delays, values, args.export)

if not args.no_plot:
    plt.scatter(delays, values, s=10)
    plt.xlabel("Delay ($\mu$s)")
    plt.ylabel("cnt")
    plt.show()

    plt.scatter(i_delays, i_values, s=10)
    plt.xlabel("Delays ($\mu$s)")
    plt.ylabel("i")
    plt.show()

    plt.scatter(j_delays, j_values, s=10)
    plt.xlabel("Delays ($\mu$s)")
    plt.ylabel("j")
    plt.show()

    plt.scatter(delays, values, s=10)
    plt.scatter(i_delays, i_values, s=10)
    plt.scatter(j_delays, j_values, s=10)
    plt.legend(["cnt", "i", "j"])
    plt.show()

    plt.hist([values, i_values, j_values], bins=50, edgecolor="white")
    plt.legend(["cnt", "i", "j"])
    plt.show()

    plt.hist(delays_fault, bins=50, edgecolor="white")
    plt.xlabel("Delays ($\mu$s)")
    plt.show()
