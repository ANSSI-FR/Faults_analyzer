#!/usr/bin/env python3

from results import merge_results
from analyzer import Analyzer
from formater import Formater
from manip import Manip, format_manip_info
from plotter import PlotterType, Plotter
from manips_manager import ManipsManager
from results_manager import ResultsManager

from test_manip_info_list import carto_info_list, base_dir

from carto_analyzer import CartoAnalyzer

manips = []
for manip_info in carto_info_list:
    formated_manip_info = format_manip_info(manip_info)
    manips.append(Manip(**formated_manip_info))
mm = ManipsManager(base_dir, manips)
mm.manage_manips()

results_list = []

def create_to_plot(anal):
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
    return to_plot

#TODO: ask for manip to trace

manip = manips[0]
params = manip.get_params()
anal = CartoAnalyzer(**params)

to_plot = create_to_plot(anal)
pl = Plotter(to_plot)
while 1:
    df = manip.get_dataframe()
    anal.set_dataframe(df)
    to_plot = create_to_plot(anal)
    pl.set_to_plot(to_plot)
    pl.show(blocking=False)
