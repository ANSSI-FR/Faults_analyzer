import sys
import pandas as pd
import numpy as np
import argparse
import plotter

sys.path.append("/media/nas/projects/liblsc/liblsc_stable")

from manip_utils import calcer
from manip_utils import bin_utils as bu

default_values = [((1<<(31-i))+(1<<i)) for i in range(10)]
#default_values[3] = 255
#default_values[9] = 85
cmp_bypass_v = 170
#default_values[5] = default_values[8]
#default_values[0] += 100
#default_values[1] = 1
#default_values = [((1<<(31-i))+(1<<i)) if i != 0 else 1020 for i in range(10)]
comp_default_values = [bu.comp( ((1<<(31-i))+(1<<i)), 32 ) for i in range(10)]
delays = [0, 0.5e-9, 1e-9, 1.5e-9, 2e-9, 2.5e-9, 3e-9, 3.5e-9, 4e-9, 4.5e-9]
powers = [250, 300, 350]

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
            if ( bu.to_unsigned(ope[reg], 32) != default_values[i]) and not np.isnan(ope[reg]):
                ret[i] = True
    return ret

def get_num_faulted_reg(ope):
    reg_is_faulted = get_faulted_reg(ope)
    for i, reg_faulted in enumerate(reg_is_faulted):
        if reg_faulted:
            return i
    return -1

def is_faulted_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) in default_values:
            print(ope)
            return True
    return False

def is_faulted_or_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for k in range(10):
            if bu.s2u(ope[reg], 32) == default_values[i]|default_values[k]:
                return True
    return False

def is_faulted_comp_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) in comp_default_values:
            if bu.s2u(ope[reg], 32) != comp_default_values[i]:
                return True
    return False

def is_all_zero(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) == 0:
            return True
    return False

def is_all_one(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) == 0xffffffff:
            return True
    return False

def is_all_flip(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) == comp_default_values[i]:
            return True
    return False

def is_add_with_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] + default_values[j], 32):
                return True
    return False

def is_and_with_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] & default_values[j], 32):
                return True
    return False

def is_and_with_comp_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] & comp_default_values[j], 32):
                return True
    return False

def is_xor_with_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] ^ default_values[j], 32):
                return True
    return False

def is_sub_with_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] - default_values[j], 32):
                return True
    return False

def is_or_with_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] | default_values[j], 32):
                return True
    return False

def is_or_2_other_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            for k in range(10):
                if bu.s2u(ope[reg], 32) == bu.s2u(default_values[j] | default_values[k], 32):
                    if (i == j) or (i == k):
                        return False
                    return True
    return False

def is_minus_one(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) == default_values[i]-1:
            return True
    return False

def is_cmp_bypass(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if (i == 9) and (bu.s2u(ope[reg],32) == cmp_bypass_v):
            return True
    return False

def is_cst(ope, cst):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) == cst:
            return True
    return False

def get_copied_reg(ope):
    ret = [False]*10
    if is_set_as_faulted(ope) and is_faulted_other_reg(ope):
        i = get_num_faulted_reg(ope)
        reg = "r{}".format(i)
        j = default_values.index(bu.s2u(ope[reg], 32))
        ret[j] = True
    return ret

def get_comp_copied_reg(ope):
    ret = [False]*10
    if is_set_as_faulted(ope) and is_faulted_comp_other_reg(ope):
        i = get_num_faulted_reg(ope)
        reg = "r{}".format(i)
        j = comp_default_values.index(bu.s2u(ope[reg], 32))
        ret[j] = True
    return ret

def get_num_copied_reg(ope):
    reg_is_copied = get_copied_reg(ope)
    for i, reg_copied in enumerate(reg_is_copied):
        if reg_copied:
            return i
    return -1

def get_faulted_with_other_reg_value_reg(ope):
    ret = [False]*10
    if is_set_as_faulted(ope) and is_faulted_other_reg(ope):
        ret = get_faulted_reg(ope)
    return ret

def get_other_reg_relation(df):
    ret = np.zeros((10,10))
    for _, ope in df.iterrows():
        if is_set_as_faulted(ope) and is_faulted_other_reg(ope):
            i = get_num_faulted_reg(ope)
            j = get_num_copied_reg(ope)
            ret[i][j] += 1
    return ret

def get_or_ope2(ope):
    ret = [False]*10
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for j in range(10):
            if bu.s2u(ope[reg], 32) == bu.s2u(default_values[i] | default_values[j], 32):
                ret[j] = True
    return ret

def print_bin_diff_faulted_reg(ope):
    i = get_num_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        print("0x{:08x} -> 0x{:08x}".format(default_values[i], int(bu.s2u(ope[reg], 32))))
        bu.bin_diff( default_values[i], bu.s2u(ope[reg], 32), 32)

def get_fault_model_reduced(ope):
    ret = [False]*3
    if is_set_as_faulted(ope):
        if is_or_with_other_reg(ope):
            ret[0] = True
        elif is_or_2_other_reg(ope):
            ret[1] = True
        else:
            print_bin_diff_faulted_reg(ope)
            ret[2] = True
    return ret

def get_fault_model_or(ope):
    ret = [False]*7
    if is_set_as_faulted(ope):
        if is_faulted_other_reg(ope):
            ret[0] = True
        elif is_faulted_comp_other_reg(ope):
            ret[1] = True
        elif is_all_zero(ope):
            ret[2] = True
        elif is_all_flip(ope):
            ret[3] = True
        elif is_or_with_other_reg(ope):
            ret[4] = True
        elif is_or_2_other_reg(ope):
            ret[5] = True
        else:
            print_bin_diff_faulted_reg(ope)
            ret[6] = True
    return ret

def get_fault_model(ope):
    ret = [False]*14
    if is_set_as_faulted(ope):
        if is_faulted_other_reg(ope):
            ret[0] = True
        elif is_faulted_comp_other_reg(ope):
            ret[1] = True
        elif is_all_zero(ope):
            ret[2] = True
        elif is_all_one(ope):
            ret[3] = True
        elif is_all_flip(ope):
            ret[4] = True
        elif is_add_with_other_reg(ope):
            ret[5] = True
        elif is_and_with_other_reg(ope):
            ret[6] = True
        elif is_minus_one(ope):
            ret[7] = True
        elif is_xor_with_other_reg(ope):
            ret[8] = True
        elif is_sub_with_other_reg(ope):
            ret[9] = True
        elif is_or_with_other_reg(ope):
            ret[10] = True
        elif is_and_with_comp_other_reg(ope):
            ret[11] = True
        elif is_or_2_other_reg(ope):
            ret[12] = True
        else:
            print_bin_diff_faulted_reg(ope)
            ret[13] = True
    return ret

def get_cmp_fault_model(ope):
    ret = [False]*3
    if is_set_as_faulted(ope):
        if is_cmp_bypass(ope):
            ret[0] = True
        elif is_cst(ope, 0xfffcb924):
            ret[1] = True
        else:
            print_bin_diff_faulted_reg(ope)
            ret[2] = True
    return ret

def is_unknown(ope):
    if is_set_as_faulted(ope):
        if is_faulted_other_reg(ope):
            return False
        elif is_faulted_comp_other_reg(ope):
            return False
        elif is_all_zero(ope):
            return False
        elif is_all_one(ope):
            return False
        elif is_all_flip(ope):
            return False
        elif is_add_with_other_reg(ope):
            return False
        elif is_and_with_other_reg(ope):
            return False
        elif is_minus_one(ope):
            return False
        elif is_xor_with_other_reg(ope):
            return False
        elif is_sub_with_other_reg(ope):
            return False
        elif is_or_with_other_reg(ope):
            return False
        elif is_and_with_comp_other_reg(ope):
            return False
        elif is_or_2_other_reg(ope):
            return False
        elif is_cmp_bypass(ope):
            return False
        else:
            return True

def get_delay_fault_dist(ope):
    ret = [False]*len(delays)
    if is_cmp_bypass(ope):
        i = delays.index(ope["injector_D"])
        ret[i] = True
    return ret

def get_power_fault_dist(ope):
    ret = [False]*len(powers)
    if is_cmp_bypass(ope):
        i = powers.index(ope["injector_P"])
        ret[i] = True
    return ret

def add_bar_style(plots, style):
    for plot in plots:
        if plot["type"] == "bar":
            plot.update(style)

latex_bar = {
    "show_data_value": True,
    "x_ticklabels_fontsize": 20,
    "y_ticklabels_fontsize": 20,
    "colors": "#003366",
    "bar_width": 0.5,
    #"rotate_x_labels": True
}

rules = {"plots": [
    # {
    #     "title": "Complementary register value copied distribution",
    #     "type" : "bar",
    #     "compute": get_comp_copied_reg,
    #     "show_data_value": True,
    #     "x_ticklabels": ["r{}".format(i) for i in range(10)]
    # }
    # ,
    #Distribution of copied registers
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_copied_reg,
    #     "show_data_value": True,
    #     "x_ticklabels": ["r{}".format(i) for i in range(10)]
    # }
    # ,
    # {
    #     "title": "OR 2nd operand distribution",
    #     "type" : "bar",
    #     "compute": get_or_ope2,
    #     "show_data_value": True,
    #     "x_ticklabels": ["r{}".format(i) for i in range(10)]
    # }
    #,
    # Distribution of faulted between all registers with other register value
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_faulted_with_other_reg_value_reg,
    #     "show_data_value": True,
    #     "x_ticklabels": ["r{}".format(i) for i in range(10)]
    # }
    #,
    # Distribution of faulted between all registers
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_faulted_reg,
    #     "show_data_value": True,
    #     "x_ticklabels": ["r{}".format(i) for i in range(10)]
    # }
    # ,
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_cmp_fault_model,
    #     "show_data_value": True,
    #     "x_ticklabels": ["cmp bypassed a", "r0 = 0xfffcb924", "Unknown"],
    #     "y_label": "%",
    #     "rotate_x_labels": True
    # }
    #,
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_fault_model_or,
    #     "show_data_value": True,
    #     "x_ticklabels": ["Other register\nvalue", "Other register\ncomplementary value", "All 0", "All flip", "Or with other register", "Or between\n2 other registers", "Unknown"],
    #     "rotate_x_labels": True
    # }
    #,
    {
        "title": "",
        "type" : "bar",
        "compute": get_fault_model,
        "show_data_value": True,
        "x_ticklabels": ["Other register\nvalue", "Other register\ncomplementary value", "All 0", "All 1", "All flip", "Add with\nother register", "And with\nother register",  "Val-1", "Xor with\nother register", "Sub with\nother register", "Or with\nother register", "And with\nother register\ncomplementary value", "Or between\n2 other registers", "Unknown"],
        "rotate_x_labels": True
    }
    # ,
    # {
    #     "title": "",
    #     "type" : "bar",
    #     "compute": get_fault_model_reduced,
    #     "show_data_value": False,
    #     "x_ticklabels": ["Or with other register", "Or between\n2 other registers", "Unknown"],
    #     "x_ticklabels_fontsize": 20,
    #     "y_ticklabels_fontsize": 20,
    #     "colors": "#003366",
    #     "bar_width": 0.2,
    #     "rotate_x_labels": True
    # }
    #,
    # {
    #     "title": "Faulted register all 0",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_all_zero
    # },
    # {
    #     "title": "Faulted register all flip",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_all_flip
    # },
    # {
    #     "title": "Faulted register all 1",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_all_one
    # },
    # {
    #     "title": "Faults",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_faulted
    # }
    #,
    # {
    #     "title": "Faulted register has other register value",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_faulted_other_reg
    # }
    # ,
    # {
    #     "title": "Faulted register has unknown fault model",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_unknown
    # }
    # ,
    # {
    #     "title": "Bypass cmp",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_cmp_bypass
    # }
    # ,
    # {
    #     "title": "Fault per delay",
    #     "type" : "bar",
    #     "compute": get_delay_fault_dist,
    #     "show_data_value": True,
    #     "x_ticklabels": ["{}".format(i) for i in delays],
    #     "x_label": "Delay in s"
    # }
    # ,
    # {
    #     "title": "Fault per power",
    #     "type" : "bar",
    #     "compute": get_power_fault_dist,
    #     "show_data_value": True,
    #     "x_ticklabels": ["{}".format(i) for i in powers],
    #     "x_label": "Voltage in V"
    # }
    # ,
    # {
    #     "title": "Faulted register is or with other register",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_faulted_or_other_reg
    # }
    #,
    # {
    #     "title": "Faulted register has other register complementary value",
    #     "type" : "matrix",
    #     "matrix_x" : "plan_xgrid",
    #     "matrix_y" : "plan_ygrid",
    #     "compute" : is_faulted_comp_other_reg
    # },
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
# to_plot.append({
#     "title": "",
#     "type": "matrix",
#     "data": get_other_reg_relation(df),
#     "x_label": "Copied register",
#     "y_label": "Faulted regiser"
# })
add_bar_style(to_plot, latex_bar)
pl = plotter.Plotter(to_plot)
pl.show()
