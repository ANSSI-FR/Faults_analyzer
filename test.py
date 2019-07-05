#!/usr/bin/env python3

from results import merge_results
from analyzer import Analyzer
from formater import Formater
from manip import Manip, format_manip_info
from plotter import PlotterType
from manips_manager import ManipsManager

from test_manip_info_list import manip_info_list, base_dir

def print_results_list(result_list):
    for i, results in enumerate(results_list):
        to_print = "[{}] {}".format(i, results.exp)
        print(to_print)

manips = []
for manip_info in manip_info_list:
    formated_manip_info = format_manip_info(manip_info)
    manips.append(Manip(**formated_manip_info))
mm = ManipsManager(base_dir, manips)
mm.manage_manips()

results_list = []

for manip in manips:
    params = manip.get_params()
    print("\nAnalyzing {}\n".format(manip.result_name))
    anal = Analyzer(**params)
    results = anal.get_results()
    results.add_result(anal.get_effects_distribution())
    results_list.append(results)
    print("\n{} analysis done\n".format(manip.result_name))

print_results_list(results_list)

for results in results_list:
    results_str = results.get_results_table_str()
    print(results_str)

    result_str = results.get_result_table_str(2)
    print(result_str)

    titles_str = results.get_results_titles_str()
    print(titles_str)

    pl = results.get_plotter("Effects distribution", PlotterType.PIE, "Occurrence",
                             "Effect")
    pl.show()

# merged_result = merge_results(results_list, "Fault model statistics" ,
#                               [True]*2, [True, False])
# form = Formater(merged_result.get_results())
# res_str = form.get_printable_str()
# print(res_str)
