#!/usr/bin/env python3
import matplotlib.pyplot as plt

from results import merge_results
from analyzer import Analyzer
from formater import Formater
from manip import Manip, format_manip_info
from plotter import PlotterType, Plotter
from manips_manager import ManipsManager
from results_manager import ResultsManager
from my_thread import MyThread
from result import Result
from carto_result import CartoResult
from results import Results

from test_manip_info_list import carto_info_list, base_dir

from carto_analyzer import CartoAnalyzer

manips = []
for manip_info in carto_info_list:
    formated_manip_info = format_manip_info(manip_info)
    manips.append(Manip(**formated_manip_info))
mm = ManipsManager(base_dir, manips)
mm.manage_manips()

results_list = []

for manip in manips:
    params = manip.get_params()
    print("\nAnalyzing {}\n".format(manip.result_name))
    anal = CartoAnalyzer(progress=True, **params)
    result_dict_list = anal.get_results()
    result_dict_list.append(anal.get_effects_distribution())
    result_dict_list += anal.get_matrix_results()

    result_list = []
    for result_dict in result_dict_list:
        result = Result(**result_dict)
        result_list.append(result)

    carto_result_list = []
    for result_dict in anal.get_matrices():
        result = CartoResult(**result_dict)
        carto_result_list.append(result)

    results = Results(manip.base_dir, manip.device, manip.manip_name,
                      manip.result_name, result_list+carto_result_list)

    results_list.append(results)

    print("\n{} analysis done\n".format(manip.result_name))

rm = ResultsManager(results_list, latex=True)
rm.start_interface()
