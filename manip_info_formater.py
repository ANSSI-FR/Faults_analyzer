import os, sys

from importlib import import_module

sys.path += [os.getcwd()]

def get_params(params_file):
    module_name = params_file.replace(".py", "").replace("/", ".")
    module = import_module(module_name)
    return module.params

def format_manip_info(manip_info):
    result_file = manip_info["base_dir"] + "/devices/" + manip_info["device"] + "/manips/" + manip_info["manip_name"] + "/results/" + manip_info["result_name"] + "/main.csv"
    analysis_params = get_params(manip_info["params_file"])
    id_name = manip_info["id_name"]

    ret = {
        "result_file": result_file,
        "analysis_params": analysis_params,
        "id_name": id_name
    }

    return ret
