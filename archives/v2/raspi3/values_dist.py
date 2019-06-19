import sys
import pandas as pd
import argparse
import numpy as np

sys.path.append("/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")

from ManipUtils import plotter
from ManipUtils import bin_utils as bu

default_values = [((1<<(31-i))+(1<<i)) for i in range(10)]
# default_values[3] = 255
# default_values[9] = 85
#default_values[0] += 100
#default_values[1] = 1
#default_values = [((1<<(31-i))+(1<<i)) if i != 0 else 1020 for i in range(10)]
#default_values = [((1<<(31-i))+(1<<i)) if i != 3 else 2497 for i in range(10)]
#default_values = [2497 if i==3 else 2496 if i==9 else ((1<<(31-i))+(1<<i)) for i in range(10)]
comp_default_values = [bu.comp( ((1<<(31-i))+(1<<i)), 32 ) for i in range(10)]
immediate_values = range(256)
comp_immediate_values = [bu.comp(i, 32) for i in range(256)]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    parser.add_argument("-r", "--register", help="Register you want to display the distribution", type=int, default=0)
    args = parser.parse_args()
    return args.manip_dir, args.register

def get_values(df, reg):
    values = []
    dist = []
    for _, exp in df.iterrows():
        val = exp["r{}".format(reg)]
        if not np.isnan(val):
            val = int(val)
            if bu.s2u(val,32) != default_values[reg]:
                hex_val = "0x{:08X}".format(bu.s2u(val,32))
                if hex_val not in values :
                    values.append(hex_val)
                    dist.append(1)
                else:
                    i = values.index(hex_val)
                    dist[i] += 1
    return values, dist


def get_all_immediate_values(df):
    values = []
    dist = []
    for _, exp in df.iterrows():
        for i in range(10):
            val = exp["r{}".format(i)]
            if not np.isnan(val):
                val = int(val)
                if bu.s2u(val,32) != default_values[i]:
                    hex_val = "0x{:08X}".format(bu.s2u(val,32))
                    if bu.s2u(val,32) in immediate_values:
                        if hex_val not in values :
                            values.append(hex_val)
                            dist.append(1)
                        else:
                            i = values.index(hex_val)
                            dist[i] += 1
    return values, dist

def get_all_comp_immediate_values(df):
    values = []
    dist = []
    for _, exp in df.iterrows():
        for i in range(10):
            val = exp["r{}".format(i)]
            if not np.isnan(val):
                val = int(val)
                if bu.s2u(val,32) != default_values[i]:
                    hex_val = "0x{:08X}".format(bu.s2u(val,32))
                    if bu.s2u(val,32) in comp_immediate_values:
                        if hex_val not in values :
                            values.append(hex_val)
                            dist.append(1)
                        else:
                            i = values.index(hex_val)
                            dist[i] += 1
    return values, dist

def get_all_values(df):
    values = []
    dist = []
    for _, exp in df.iterrows():
        for i in range(10):
            val = exp["r{}".format(i)]
            if not np.isnan(val):
                val = int(val)
                if bu.s2u(val,32) != default_values[i]:
                    hex_val = "0x{:08X}".format(bu.s2u(val,32))
                    if hex_val not in values :
                        values.append(hex_val)
                        dist.append(1)
                    else:
                        i = values.index(hex_val)
                        dist[i] += 1
    s = sum(dist)
    if s != 0:
        norm = [round(float(i)/s, 2) for i in dist]
    else:
        norm = [0 for i in dist]
    dist = norm
    return values, dist


def plot_values_dist(df, reg):
    values, dist = get_values(df, reg)
    #values, dist = get_all_values(df)
    #values, dist = get_all_immediate_values(df)
    #values, dist = get_all_comp_immediate_values(df)

    to_plot = [{
        "title": "Values distribution for faulted registers",
        "type": "bar",
        "data": dist,
        "x_ticklabels": values,
        #"show_data_value": True
        #"rotate_x_labels": True
    }]

    pl = plotter.Plotter(to_plot)
    pl.init_plot()
    pl.show()

manip_dir, reg = get_args()
main_file = manip_dir + "/main.csv"

df = pd.read_csv(main_file)

plot_values_dist(df, reg)
