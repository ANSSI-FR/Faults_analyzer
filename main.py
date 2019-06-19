#!/usr/bin/env python3

from utils import *
from bin_utils import *
from analyzer import Analyzer
from argparse import ArgumentParser

PARSER = ArgumentParser(description="Todo.")
PARSER.add_argument("params_file", help="File containing the paramaters for the analysis.", type=str)
args = PARSER.parse_args()

params_module = "params.{}".format(args.params_file)
PARAMS = import_params(params_module)

anal = Analyzer(PARAMS)
anal.run_analysis()

default_values = PARAMS["default_values"]
obs_names = PARAMS["obs_names"]
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
nb_faulted_obs = anal.get_nb_faulted_obs()

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
        "results": [format_table(default_values, data_format), format_table(values_after_execution, data_format), norm_percent(faulted_obs)],
        "titles": ["Observed", "Default value", "Value after execution", "Fault (%)"]
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

print("Number of operation to do: {}".format(nb_to_do))
print("Number of operation done: {}".format(nb_done))
print("Percentage done: {:3.2f}%".format(100*nb_done/float(nb_to_do)))
print("Number of reboots: {}".format(nb_reboots))
print("Percentage of reboots: {:3.2f}%".format(100*nb_reboots/float(nb_done)))
print("Number of faults: {}".format(nb_faults))
print("Percentage of faults: {:3.2f}%".format(100*nb_faults/float(nb_done)))
print("Number of faulted obs: {}".format(nb_faulted_obs))
print("Average faulted obs per fault: {:3.2f}".format(nb_faulted_obs/float(nb_faults)))

for result_table in result_tables:
    print_result(**result_table)
