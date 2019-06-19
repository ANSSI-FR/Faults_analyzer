import pandas as pd
import argparse
import math
from prettytable import PrettyTable

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    return parser.parse_args()

def get_manip_dir(args):
    manip_dir = args.manip_dir
    if manip_dir[-1] != "/":
        manip_dir += "/"
    return manip_dir

def is_done(ope):
    return ope["plan_done"]

def get_values_from_log(ope):
    log = ope["log"]
    log = log.split(":")
    values = log[1:-1]
    values = [int(v) for v in values]
    return values

def is_set_as_faulted(ope):
    if is_done(ope):
        return ope["fault"]
    return False

def is_set_as_reboot(ope):
    if is_done(ope):
        return ope["reboot"]
    return False

def get_faulted_reg(ope, registers, default_values, to_test):
    reg_values = get_values_from_log(ope)
    for i in range(len(registers)):
        if to_test[i]:
            if reg_values[i] != default_values[i]:
                return i, reg_values[i]

def norm_percent(raw):
    return [float(i)/sum(raw)*100 for i in raw]

def update_result(ope, values, result, param):
    param_value = ope[param]
    value_index = values.index(param_value)
    result[value_index] += 1

def update_powers(ope, power_values, power_result):
    update_result(ope, power_values, power_result, "injector_P")

def update_delays(ope, delay_values, delay_result):
    update_result(ope, delay_values, delay_result, "injector_D")

def update_faulted_registers(ope, registers, default_values, faulted_registers, to_test):
    faulted_reg, _ = get_faulted_reg(ope, registers, default_values, to_test)
    faulted_registers[faulted_reg] += 1

def update_faulted_values(ope, registers, default_values, faulted_values, faulted_value_occurrence, to_test):
    _, faulted_value = get_faulted_reg(ope, registers, default_values, to_test)
    if not faulted_value in faulted_values:
        faulted_values.append(faulted_value)
        faulted_values_occurrence.append(1)
    else:
        for i, value in enumerate(faulted_values):
            if value == faulted_value:
                faulted_values_occurrence[i] += 1

def format_table(table, format_str):
    return [format_str.format(i) for i in table]

def print_result(values, results, titles=[]):
    t = PrettyTable(titles)
    for i in range(len(values)):
        line = [values[i]]
        for j in range(len(results)):
            line.append(results[j][i])
        t.add_row(line)
    print(t)

args = get_args()
manip_dir = get_manip_dir(args)
result_file = manip_dir + "/main.csv"
df = pd.read_csv(result_file, error_bad_lines=False)

nb_faults = 0
nb_reboots = 0
nb_done = 0

powers = list(df.injector_P.unique())
fault_powers = [0]*len(powers)
reboot_powers = [0]*len(powers)

delays = list(df.injector_D.unique())
fault_delays = [0]*len(delays)
reboot_delays = [0]*len(delays)

registers = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
default_values = [((1 << (63 - i)) + (1 << i)) for i in range(len(registers))]
faulted_registers = [0]*len(registers)
to_test = [False,True,False,False,False,False,True,True,False,False,True,True,True,True]

faulted_values = []
faulted_values_occurrence = []
values_after_execution = []

for _, ope in df.iterrows():
    if is_done(ope):
        nb_done += 1
        if len(values_after_execution) == 0:
            if not is_set_as_reboot(ope) and not is_set_as_faulted(ope):
                values_after_execution = get_values_from_log(ope)

    if is_set_as_reboot(ope):
        nb_reboots += 1
        update_powers(ope, powers, reboot_powers)
        update_delays(ope, delays, reboot_delays)

    if is_set_as_faulted(ope):
        nb_faults += 1
        update_powers(ope, powers, fault_powers)
        update_delays(ope, delays, fault_delays)
        update_faulted_registers(ope, registers, default_values, faulted_registers, to_test)
        update_faulted_values(ope, registers, default_values, faulted_values, faulted_values_occurrence, to_test)

fault_powers = norm_percent(fault_powers)
reboot_powers = norm_percent(reboot_powers)
fault_delays = norm_percent(fault_delays)
reboot_delays = norm_percent(reboot_delays)
faulted_registers = norm_percent(faulted_registers)
faulted_values_occurrence = norm_percent(faulted_values_occurrence)

hex_format = "0x{:016x}"
faulted_values = format_table(faulted_values, hex_format)
hex_default_values = format_table(default_values, hex_format)
values_after_execution = format_table(values_after_execution, hex_format)

print("Total operations : {}".format(nb_done))
print("Reboots : {}".format(nb_reboots))
print("Faults : {}".format(nb_faults))
print_result(powers, [fault_powers, reboot_powers], ["Power value (V)", "Fault (%)", "Reboot (%)"])
print_result(delays, [fault_delays, reboot_delays], ["Delay (?)", "Fault (%)", "Reboot (%)"])
print_result(registers, [hex_default_values, values_after_execution, faulted_registers], ["Registers", "Default value", "Values after execution", "Fault (%)"])
print_result(faulted_values, [faulted_values_occurrence], ["Faulted values", "Occurrence (%)"])
