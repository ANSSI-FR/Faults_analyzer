import plotter
import sys
import numpy as np
import pandas as pd

sys.path.append("/media/nas/projects/liblsc/liblsc_stable")

from manip_utils import bin_utils as bu

result_dir = "/media/nas/projects/Fault_attacks/EM/Raspi3/raspi3_manip_liblsc/liblsc/results_good"
manip_dirs_faulted_reg = ["rasp_regtest_movr0r0", "rasp_regtest_movr3r3"]
exps_faulted_reg = ["mov r0, r0", "mov r3, r3"]

manip_dirs_copied_reg = ["rasp_regtest_movallreg_fix", "rasp_regtest_orallreg"]
exps_copied_reg = ["mov rX, rX", "or rX, rX"]

regs = ["r{}".format(i) for i in range(10)]
default_values = [((1<<(31-i))+(1<<i)) for i in range(10)]

manip_dirs = manip_dirs_copied_reg
exps = exps_copied_reg

results_files = [result_dir + "/" + dir + "/main.csv" for dir in manip_dirs]
dfs = [pd.read_csv(result_file, error_bad_lines=False) for result_file in results_files]


def get_faulted_reg(ope):
    if ope["plan_done"] == True:
        for i in range(10):
            reg = "r{}".format(i)
            if (bu.to_unsigned(ope[reg], 32) != default_values[i]) and not np.isnan(ope[reg]):
                return i
    return -1

def get_faulted_regs(df, regs):
    fault_per_reg = [0] * len(regs)
    for _, ope in df.iterrows():
        i = get_faulted_reg(ope)
        if not i is -1:
            fault_per_reg[i] += 1
    norm_fault_per_reg = [float(i)/sum(fault_per_reg)*100 for i in fault_per_reg]
    return norm_fault_per_reg

def is_faulted_other_reg(ope):
    i = get_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        if bu.s2u(ope[reg], 32) in default_values:
            return True
    return False

def get_copied_reg(ope):
    faulted_reg = get_faulted_reg(ope)
    if not faulted_reg is -1:
        faulted_reg_name = "r{}".format(faulted_reg)
        copied_reg = default_values.index(bu.s2u(ope[faulted_reg_name], 32))
        return copied_reg
    return -1

def get_copied_regs(df, regs):
    copied_reg = [0] * len(regs)
    for _, ope in df.iterrows():
        if is_faulted_other_reg(ope):
            i = get_copied_reg(ope)
            if not i is -1:
                copied_reg[i] += 1
    norm_copied_reg = [float(i)/sum(copied_reg)*100 for i in copied_reg]
    return norm_copied_reg

def get_or_reg(ope):
    i = get_faulted_reg(ope)
    if i != -1:
        reg = "r{}".format(i)
        for k in range(10):
            if bu.s2u(ope[reg], 32) == default_values[i]|default_values[k]:
                return k
    return -1

def get_or_regs(df, regs):
    or_regs = [0] * len(regs)
    for _, ope in df.iterrows():
        i = get_or_reg(ope)
        if not i is -1:
            or_regs[i] += 1
    norm_or_regs = [float(i)/sum(or_regs)*100 for i in or_regs]
    return norm_or_regs

to_plot = [{
    "title": "",
    "type": "multibar",
#    "data": [get_copied_regs(df, regs) for df in dfs],
    "data": [get_copied_regs(dfs[0], regs), get_or_regs(dfs[1], regs)],
    "x_ticklabels": regs,
    "bar_width": 0.3,
    "y_label": "%",
    "legend": exps,
    "colors": ["#003366", "#dd6e42"]
}]

pl = plotter.Plotter(to_plot)
#pl.show()
pl.export_tikz("tikz/copied_reg_multi.tex")
