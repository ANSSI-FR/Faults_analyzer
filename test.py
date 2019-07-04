#!/usr/bin/env python3

import os, sys
import logging

from importlib import import_module

from utils import *
from bin_utils import *
from analyzer import Analyzer
from argparse import ArgumentParser
from formater import Formater

sys.path += [os.getcwd()]

PARSER = ArgumentParser(description="Todo.")
PARSER.add_argument("params_file", help="File containing the paramaters for the analysis.", type=str)
PARSER.add_argument("-t", "--trace", help="If set, will print in real time the matrix.", action="store_true")
args = PARSER.parse_args()

MODULE_NAME = args.params_file.replace(".py","").replace("/",".")
MODULE = import_module(MODULE_NAME)
TO_ANALYZE = MODULE.TO_ANALYZE

for to_a in TO_ANALYZE:
    params = to_a["params"]

    print("\n\nAnalyzing {}\n".format(to_a["file"]))

    anal = Analyzer(**params)
    results = anal.get_results()
    results.append(anal.get_effects_distribution())
    
    to_a.update({"results": results})

    form = Formater(results)
    result_str = form.get_printable_str()

    to_a.update({"result_str": result_str})
    
    print(result_str)
    for to_plot in to_a["to_plot"]:
        form.set_to_plot(**to_plot)
    pl = form.get_plotter()
    pl.show()

# form.set_to_plot(-1, PlotterType.PIE, 1, 0)
# pl = form.get_plotter()
# pl.show()

# form.set_to_plot(-1, PlotterType.BAR, 1, 0)
# pl = form.get_plotter()
# pl.show()
