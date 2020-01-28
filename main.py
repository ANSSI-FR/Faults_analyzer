#!/usr/bin/env python3
from modules.core import Core

from config import CONFIG

if __name__ == "__main__":
    c = Core(**CONFIG)
    c.create_directories()
    res_files = c.get_results_files()
    print(res_files)
    for f in res_files:
        c.load_results(f)
    for manip in c.mm.manips:
        manip.print_info()

    for results in c.rm.results_list:
        print("id_name: {}\n".format(results.id_name))
        for result in results.results:
            result.print_info()

    man_files = c.get_manips_files()
    for f in man_files:
        c.load_manip(f)

    for manip in c.mm.manips:
        manip.print_info()
