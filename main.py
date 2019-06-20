#!/usr/bin/env python3

import os, sys
from utils import *
from bin_utils import *
from analyzer import Analyzer
from argparse import ArgumentParser

sys.path += [os.getcwd()]

def get_exp_type(PARAMS):
    if "type" in PARAMS:
        return PARAMS["type"]
    else:
        return None

def get_fault_model_number(fault_model_list, fault_model):
    return fault_model_list[1][fault_model_list[0].index(fault_model)]

PARSER = ArgumentParser(description="Todo.")
PARSER.add_argument("params_file", help="File containing the paramaters for the analysis.", type=str)
args = PARSER.parse_args()

MODULE_NAME = args.params_file.replace(".py","").replace("/",".")
MODULE = import_module(MODULE_NAME)
PARAMS = MODULE.PARAMS

anal = Analyzer(PARAMS)
anal.run_analysis()

default_values = PARAMS["default_values"]
obs_names = PARAMS["obs_names"]
to_test = PARAMS["to_test"]
values_after_execution = anal.get_values_after_execution()
nb_to_do = anal.get_nb_to_do()
nb_done = anal.get_nb_done()
nb_reboots = anal.get_nb_reboots()
reboot_powers = anal.get_reboot_powers()
reboot_delays = anal.get_reboot_delays()
nb_faults = anal.get_nb_faults()
fault_powers = anal.get_fault_powers()
fault_delays = anal.get_fault_delays()
faulted_obs = anal.get_faulted_obs()
faulted_values = anal.get_faulted_values()
faulted_values_occurrence = anal.get_faulted_values_occurrence()
powers = anal.get_powers()
delays = anal.get_delays()
fault_models = anal.get_fault_models()

obs_value_after_execution_origin_occurrence = None
if get_fault_model_number(fault_models, "Other obs value after execution"):
    obs_value_after_execution_origin_occurrence = anal.get_other_obs_value_after_execution_origin_occurence()

nb_faulted_obs = anal.get_nb_faulted_obs()
base_address = None
if get_exp_type(PARAMS) is "memory":
    base_address = anal.get_base_address()

data_format = PARAMS["data_format"]
nb_bits = PARAMS["nb_bits"]

values_after_execution = to_unsigned_list(values_after_execution, nb_bits)
faulted_values = to_unsigned_list(faulted_values, nb_bits)

result_tables = [
    {
        "values": powers,
        "results": [norm_percent(fault_powers), norm_percent(reboot_powers)],
        "titles": ["Power value (V)", "Fault (%)", "Reboot (%)"]
    },
    {
        "values": delays,
        "results": [norm_percent(fault_delays), norm_percent(reboot_delays)],
        "titles": ["Delay (ns)", "Fault (%)", "Reboot (%)"]
    },
    {
        "values": obs_names,
        "results": [format_table(default_values, data_format), format_table(values_after_execution, data_format), norm_percent(faulted_obs), to_test],
        "titles": ["Observed", "Default value", "Value after execution", "Fault (%)", "Tested"]
    },
    {
        "values": format_table(faulted_values, data_format),
        "results": [norm_percent(faulted_values_occurrence)],
        "titles": ["Faulted values", "Occurrence (%)"]
    },
    {
        "values": fault_models[0],
        "results": [norm_percent(fault_models[1])],
        "titles": ["Fault model", "Occurrence (%)"]
    }
]

if get_exp_type(PARAMS) is "memory":
    result_tables.append(
        {
            "values": format_table(faulted_values, data_format),
            "results": [norm_percent(faulted_values_occurrence), format_table(base_address, data_format)],
            "titles": ["Faulted values", "Occurrence (%)", "Base address"]
        })

if not obs_value_after_execution_origin_occurrence is None:
    result_tables.append(
        {
            "values": obs_names,
            "results": [norm_percent(obs_value_after_execution_origin_occurrence)],
            "titles": ["Origin of the faulted value after execution", "Occurence (%)"]
        })

stats_str = ""
stats_str += "Number of operation to do: {}\n".format(nb_to_do)
stats_str += "Number of operation done: {}\n".format(nb_done)
stats_str += "Percentage done: {:3.2f}%\n".format(100*nb_done/float(nb_to_do))
stats_str += "Number of reboots: {}\n".format(nb_reboots)
stats_str += "Percentage of reboots: {:3.2f}%\n".format(100*nb_reboots/float(nb_done))
stats_str += "Number of faults: {}\n".format(nb_faults)
stats_str += "Percentage of faults: {:3.2f}%\n".format(100*nb_faults/float(nb_done))
stats_str += "Number of faulted obs: {}\n".format(nb_faulted_obs)
stats_str += "Average faulted obs per fault: {:3.2f}\n".format(nb_faulted_obs/float(nb_faults))

f = open("results.html", "a")

f.write("<p>" + stats_str.replace("\n","<br>") + "</p>")

print(stats_str)
for result_table in result_tables:
    print_result(**result_table)
    add_to_html_file(f, **result_table)

f.close()
