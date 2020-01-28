import os, sys

from importlib import import_module

sys.path += [os.getcwd()]

def get_params(params_file, import_path=""):
    """Extract the params object from a given Python file.

    :param str params_file: the Python file to get the params object from.

    :returns: the params object from the given Python file.

    """
    sys.path += [import_path]
    module_name = params_file.replace(".py", "").replace("/", ".")
    module = import_module(module_name)
    return module.params

def format_manip_info(manip_info):
    """Format the ANSSI/LSC manip_info dictionary format into a more generic format compliant with the Manip class.

    :param dict manip_info: the information about the a manip to format.

    :returns: a dictionary containing all the attributes for creating a Manip class.

    """
    result_file = manip_info["base_dir"] + "/devices/" + manip_info["device"] + "/manips/" + manip_info["manip_name"] + "/results/" + manip_info["result_name"] + "/main.csv"
    analysis_params = get_params(manip_info["params_file"])
    id_name = manip_info["id_name"]

    ret = {
        "result_file": result_file,
        "analysis_params": analysis_params,
        "id_name": id_name
    }

    return ret
