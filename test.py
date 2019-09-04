#!/usr/bin/env python3

from analyzer import Analyzer
from manip import Manip, format_manip_info
from manips_manager import ManipsManager
from results_manager import ResultsManager
from result import Result
from results import Results

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
    anal = Analyzer(progress=True, **params)
    result_dict_list = anal.get_results()
    result_dict_list.append(anal.get_effects_distribution())

    result_list = []
    for result_dict in result_dict_list:
        result = Result(**result_dict)
        result_list.append(result)

    results = Results(manip.base_dir, manip.device, manip.manip_name,
                      manip.result_name, result_list)
    results_list.append(results)

    print("\n{} analysis done\n".format(manip.result_name))

rm = ResultsManager(results_list)
rm.start_interface()
