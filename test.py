#!/usr/bin/env python3

from analyzer import Analyzer
from manip import Manip
from result import Result
from results import Results

from manips_manager import ManipsManager
from results_manager import ResultsManager

from manip_info_list import manip_info_list, carto_info_list
from manip_info_formater import format_manip_info

from prompt import Prompt

manips = []
for manip_info in manip_info_list:
    formated_manip_info = format_manip_info(manip_info)
    manips.append(Manip(**formated_manip_info))
for manip_info in carto_info_list:
    formated_manip_info = format_manip_info(manip_info)
    formated_manip_info.update({"carto": True})
    manips.append(Manip(**formated_manip_info))

p = Prompt(manips)
p.cmdloop()

exit(0)

#mm = ManipsManager(manips)
#manips_to_analyze = mm.start_interface()

results_list = []
for manip in manips_to_analyze:
    params = manip.get_params()
    print("\nAnalyzing {}\n".format(manip.id_name))
    anal = Analyzer(progress=True, **params)
    result_dict_list = anal.get_results()
    result_dict_list.append(anal.get_effects_distribution())

    result_list = []
    for result_dict in result_dict_list:
        result = Result(**result_dict)
        result_list.append(result)

    results = Results(result_list, manip.id_name)
    results_list.append(results)

    print("\n{} analysis done\n".format(manip.id_name))

rm = ResultsManager(results_list)
rm.start_interface()
