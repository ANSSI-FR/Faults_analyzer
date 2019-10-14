#!/usr/bin/env python3

from modules.manip_info_formater import format_manip_info
from modules.manip import Manip
from modules.prompt import Prompt

from config.manip_info_list import manip_info_list, carto_info_list

if __name__ == "__main__":

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
