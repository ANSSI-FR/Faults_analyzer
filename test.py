#!/usr/bin/env python3

from results import merge_results
from analyzer import Analyzer
from formater import Formater
from manip import Manip, format_manip_info
from plotter import PlotterType
from manips_manager import ManipsManager
from results_manager import ResultsManager

from test_manip_info_list import manip_info_list, base_dir

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
    anal = Analyzer(**params, progress=True)
    results = anal.get_results()
    results.add_result(anal.get_effects_distribution())
    results_list.append(results)
    print("\n{} analysis done\n".format(manip.result_name))

rm = ResultsManager(results_list)
rm.start_interface()
