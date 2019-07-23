#!/usr/bin/env python3

from results import merge_results
from analyzer import Analyzer
from formater import Formater
from manip import Manip, format_manip_info
from plotter import PlotterType, Plotter
from manips_manager import ManipsManager
from results_manager import ResultsManager
from my_thread import MyThread

from test_manip_info_list import carto_info_list, base_dir

from carto_analyzer import CartoAnalyzer

manips = []
for manip_info in carto_info_list:
    formated_manip_info = format_manip_info(manip_info)
    manips.append(Manip(**formated_manip_info))
mm = ManipsManager(base_dir, manips)
mm.manage_manips()

results_list = []

def plot_matrix(anal):
    done_matrix = anal.get_done_matrix()
    reboot_matrix = anal.get_reboot_matrix()
    fault_matrix = anal.get_fault_matrix()
    to_plot = [
        {
            "data": done_matrix,
            "type": PlotterType.MATRIX,
            "title": "Done"
        },
        {
            "data": reboot_matrix,
            "type": PlotterType.MATRIX,
            "title": "Reboots"
        },
        {
            "data": fault_matrix,
            "type": PlotterType.MATRIX,
            "title": "Faults"
        }
    ]
    pl = Plotter(to_plot)
    pl.show()

for manip in manips:
    params = manip.get_params()
    print("\nAnalyzing {}\n".format(manip.result_name))
    anal = CartoAnalyzer(progress=True, **params)
    results = anal.get_results()
    results.add_result(anal.get_effects_distribution())
    results_list.append(results)
    print("\n{} analysis done\n".format(manip.result_name))

th = MyThread(plot_matrix, anal)
th.start()

rm = ResultsManager(results_list)
rm.start_interface()

th.join()
