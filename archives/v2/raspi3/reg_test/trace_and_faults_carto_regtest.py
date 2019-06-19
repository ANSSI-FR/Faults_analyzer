import sys
import pandas as pd
import numpy as np
import argparse
import time
import plotter

sys.path.append("/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")

from manip_utils import calcer
from manip_utils import bin_utils as bu

default_values = [((1<<(31-i))+(1<<i)) for i in range(10)]
# default_values[3] = 255
# default_values[9] = 85
#default_values[5] = default_values[8]
#default_values[0] += 100
#default_values[1] = 1
#default_values =  [((1<<(31-i))+(1<<i)) if i != 3 else 170 for i in range(10)]
#default_values =  [((1<<(31-i))+(1<<i)) if i != 0 else 1020 for i in range(10)]
#default_values =  [((1<<(31-i))+(1<<i)) if i != 3 else 2497 for i in range(10)]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    manip_dir = parser.parse_args().manip_dir
    if manip_dir[-1] != "/":
        manip_dir = manip_dir + "/"
    return manip_dir

def is_set_as_faulted(ope):
    ret = False
    if ope["plan_done"] == True:
        if ope["fault"] == True:
            ret = True
    return ret

def is_faulted(ope):
    ret = False
    if ope["plan_done"] == True:
        for i in range(10):
            reg = "r{}".format(i)
            if ( bu.to_unsigned(ope[reg], 32) != default_values[i] ) and not np.isnan(ope[reg]):
                ret = True
    return ret

def is_r_faulted(r):
    def is_faulted(ope):
        ret = False
        if ope["plan_done"] == True:
            reg = "r{}".format(r)
            if ( bu.to_unsigned(ope[reg], 32) != default_values[r] ) and not np.isnan(ope[reg]):
                ret = True
        return ret
    return is_faulted

def get_faulted_reg(ope):
    ret = [False]*10
    if ope["plan_done"] == True:
        for i in range(10):
            reg = "r{}".format(i)
            if ( bu.to_unsigned(ope[reg], 32) != default_values[i] ) and not np.isnan(ope[reg]):
                ret[i] = True
    return ret

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
    },
    {
        "title": "Nb faults per register",
        "type" : "bar",
        "compute": get_faulted_reg,
        "show_data_value": True,
        "x_ticklabels": ["r{}".format(i) for i in range(10)]
    }
    # ,
    # {
    #     "title": "Faults",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_faulted
    # }
    # ,
    # *[{
    #     "title": "r{}".format(i),
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_r_faulted(i)
    # } for i in [0,1,2,3,4,5,6,7,8,9]]
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
    time.sleep(0.2)
