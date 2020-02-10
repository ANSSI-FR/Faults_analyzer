#!/usr/bin/env python3
import os, sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from modules.core import Core

from config import CONFIG

if __name__ == "__main__":
    c = Core(**CONFIG)

    print("#"*80)
    print("Manips:")
    print("#"*80)
    for manip in c.get_manips():
        manip.print_info()

    print("#"*80)
    print("Results list:")
    print("#"*80)
    for results in c.get_results_list():
        print("-"*50)
        print("id_name: {}\n".format(results.id_name))
        print("-"*50)
        for result in results.results:
            result.print_info()

    print("#"*80)
    print("Doing analysis:")
    print("#"*80)
    manips_to_analyze = [1]
    c.analyze_manips(manips_to_analyze, progress=True)

    print("#"*80)
    print("Results list:")
    print("#"*80)
    for results in c.get_results_list():
        print("-"*50)
        print("id_name: {}\n".format(results.id_name))
        print("-"*50)
        for result in results.results:
            result.print_info()

    print("#"*80)
    print("Forcing analysis:")
    print("#"*80)
    manips_to_analyze = [0]
    c.analyze_manips(manips_to_analyze, force=True, progress=True)

    print("#"*80)
    print("Results list:")
    print("#"*80)
    for results in c.get_results_list():
        print("-"*50)
        print("id_name: {}\n".format(results.id_name))
        print("-"*50)
        for result in results.results:
            result.print_info()

    print("#"*80)
    print("Merging Results:")
    print("#"*80)
    results_to_merge = ["bcm2837_orrR5_iv3_EM_fix_20200124","bcm2837_andR8_iv4_EM_fix_20200127"]
    result_to_merge = 1
    columns_to_merge = [0,1,2]
    columns_in_common = [0]
    name = "My Merge !!!"
    c.merge(results_to_merge, result_to_merge, columns_to_merge,
            columns_in_common, name)

    print("#"*80)
    print("Results list:")
    print("#"*80)
    for results in c.get_results_list():
        print("-"*50)
        print("id_name: {}\n".format(results.id_name))
        print("-"*50)
        for result in results.results:
            result.print_info()

    print("#"*80)
    print("Saving Results:")
    print("#"*80)
    results_to_save = 2
    filename = "MyMerge"
    c.save(results_to_save, filename)

    print("#"*80)
    print("Plotting Results:")
    print("#"*80)
    results_to_plot = "My Merge !!!"
    result_to_plot = 0
    style_name = "multibar"
    data_to_plot_index_list = [1,2,3,4]
    data_labels_index = 0
    c.plot(results_to_plot, result_to_plot, style_name,
           data_to_plot_index_list, data_labels_index)
