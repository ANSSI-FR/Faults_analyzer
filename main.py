#!/usr/bin/env python3

import os, sys
import logging
from utils import *
from bin_utils import *
from analyzer import Analyzer
from argparse import ArgumentParser
from plotter import Plotter, PlotterType

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
PARSER.add_argument("-t", "--trace", help="If set, will print in real time the matrix.", action="store_true")
args = PARSER.parse_args()

MODULE_NAME = args.params_file.replace(".py","").replace("/",".")
MODULE = import_module(MODULE_NAME)
PARAMS = MODULE.PARAMS

anal = Analyzer(**PARAMS)
anal.run_analysis()

default_values = PARAMS["default_values"]
obs_names = PARAMS["obs_names"]
to_test = PARAMS["to_test"]
values_after_execution = anal.get_values_after_execution()
reboot_powers = anal.get_reboot_powers()
reboot_delays = anal.get_reboot_delays()
fault_powers = anal.get_fault_powers()
fault_delays = anal.get_fault_delays()
faulted_obs = anal.get_faulted_obs()
faulted_values = anal.get_faulted_values()
faulted_values_occurrence = anal.get_faulted_values_occurrence()
powers = anal.get_powers()
delays = anal.get_delays()
fault_models = anal.get_fault_models()
general_stats = anal.get_general_stats()

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
        "values": general_stats["titles"],
        "results": [general_stats["data"]],
        "titles": ["Stat", "Value"]
    },
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

# if get_exp_type(PARAMS) is "memory":
#     result_tables.append(
#         {
#             "values": format_table(faulted_values, data_format),
#             "results": [norm_percent(faulted_values_occurrence), format_table(base_address, data_format)],
#             "titles": ["Faulted values", "Occurrence (%)", "Base address"]
#         })

if not obs_value_after_execution_origin_occurrence is None:
    result_tables.append(
        {
            "values": obs_names,
            "results": [norm_percent(obs_value_after_execution_origin_occurrence)],
            "titles": ["Origin of the faulted value after execution", "Occurence (%)"]
        })

str_tables = ""
html_str_tables = ""

for result_table in result_tables:
    table = create_table(**result_table)
    str_tables += table.get_string() + "\n"
    html_str_tables += table.get_html_string()

print(str_tables)

reboot_matrix = anal.get_reboot_matrix()
fault_matrix = anal.get_fault_matrix()
done_matrix = anal.get_done_matrix()

if "coordinates" in PARAMS:
    to_plot = [
        {
            "title": "Done",
            "type": PlotterType.MATRIX,
            "data": done_matrix
        },
        {
            "title": "Reboots",
            "type": PlotterType.MATRIX,
            "data": reboot_matrix
        },
        {
            "title": "Faults",
            "type": PlotterType.MATRIX,
            "data": fault_matrix
        }
    ]
    pl = Plotter(to_plot)
    pl.show()

# if TRACE:
#     #update dataframe
#     #pass dataframe to analyzer
#     #run analysis
#     #get matrix
#     #plot matrix
#     pass

