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
            "data": reboot_matrix,
            "type": PlotterType.MATRIX,
            "title": "Reboots"
        },
        {
            "data": fault_matrix,
            "type": PlotterType.MATRIX,
            "title": "Faults"
        },
        {
            "data": reboot_matrix,
            "type": PlotterType.MATRIXSCATTER,
            "title": "Reboots",
            "revert_y_axis": True,
            "image": "bcm2837_square.jpg", #TODO: give the image as a parameter
            "scale_to_image": True
            #"x_scale": 0.5 #TODO: give the x_scale as a parameter
        },
        {
            "data": fault_matrix,
            "type": PlotterType.MATRIXSCATTER,
            "title": "Faults",
            "revert_y_axis": True,
            "image": "bcm2837_square.jpg", #TODO: give the image as a parameter
            "scale_to_image": True
            #"x_scale": 0.5 #TODO: give the x_scale as a parameter
        }
    ]
    pl = Plotter(to_plot, cmap=plt.cm.jet)
    pl.show()

for manip in manips:
    params = manip.get_params()
    print("\nAnalyzing {}\n".format(manip.result_name))
    anal = CartoAnalyzer(progress=True, **params)
    results = anal.get_results()
    results.add_result(anal.get_effects_distribution())
    results_list.append(results)
    print("\n{} analysis done\n".format(manip.result_name))

plot_matrix(anal)

rm = ResultsManager(results_list)
rm.start_interface()
