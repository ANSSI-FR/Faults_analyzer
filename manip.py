import os, sys

from importlib import import_module
from utils import *

import pandas as pd

sys.path += [os.getcwd()]

def format_manip_info(manip_info):
    manip_info.update({"analysis_params": get_params(manip_info)})
    manip_info.pop("params_file")
    return manip_info

def get_params(manip_info):
    params_file = manip_info["params_file"]
    module_name = params_file.replace(".py", "").replace("/", ".")
    module = import_module(module_name)
    return module.params

class ManipInfoMaker():

    def __init__(self, base_dir):
        self.manip_info = {
            "base_dir": base_dir,
            "device": "",
            "manip": "",
            "result": "",
            "params_file": ""
        }
        self.done = False

    def print_help(self):
        help_str = """Commands:
        s, set <key> <value> : set the key element at the given value

        l, list <key> : list the available keys regarding the manip information

        p, print : print the current manip information

        h, help : display this help

        d, e, q, done, exit, quit : leave this interface
        """
        print(help_str)

    def list_key(self, key):
        dir_to_print = "{}/devices".format(self.manip_info["base_dir"])
        if key == "device":
            pass
        elif key == "manip":
            print(self.manip_info["device"])
            dir_to_print += "/{}/manips".format(self.manip_info["device"])
        elif key == "result":
            dir_to_print += "/{}/manips/{}/results".format(self.manip_info["device"], self.manip_info["manip"])
        elif key == "params_file":
            dir_to_print += "/{}/manips/{}".format(self.manip_info["device"], self.manip_info["manip"])
        else:
            print("Key {} does not exists".format(key))
            return
        dir_list = os.listdir(dir_to_print)
        print_list(dir_list)

    def print_manip_info(self):
        for info in self.manip_info:
            print("{}: {}".format(info, self.manip_info[info]))

    def update_manip_info(self, key, value):
        if key in self.manip_info:
            self.manip_info.update({key: value})
        else:
            print("Key {} does not exists".format(key))

    def eval_cmd(self, cmd):
        parsed_cmd = cmd.split(" ")
        if parsed_cmd[0] in ["s", "set"]:
            if len(parsed_cmd) != 3:
                print("Error: wrong number of arguments (expected 2, got {})".format(len(parsed_cmd)-1))
                return
            self.update_manip_info(parsed_cmd[1], parsed_cmd[2])
        elif parsed_cmd[0] in ["p", "print"]:
            self.print_manip_info()
        elif parsed_cmd[0] in ["h", "help"]:
            self.print_help()
        elif parsed_cmd[0] in ["d", "e", "q", "done", "exit", "quit"]:
            self.done = True
        elif parsed_cmd[0] in ["l", "list"]:
            if len(parsed_cmd) != 2:
                print("Error: wrong number of arguments (expected 1, got {})".format(len(parsed_cmd)-1))
                return
            self.list_key(parsed_cmd[1])

    def make_manip_info(self):
        print("Welcome in the manip maker !")
        self.print_help()
        while not self.done:
            cmd = input("> ")
            self.eval_cmd(cmd)
        return format_manip_info(self.manip_info)

    def set_manip_info(self, manip_info):
        self.manip_info = manip_info

class Manip():

    device = ""
    manip_name = ""
    result_name = ""
    base_dir = ""
    result_dir = ""
    result_file = "main.csv"
    analysis_params = {}

    def __init__(self, base_dir, device, manip_name, result_name,
                 analysis_params, result_file="main.csv"):
        self.base_dir = base_dir
        self.device = device
        self.manip_name = manip_name
        self.result_name = result_name
        self.result_file = result_file
        self.set_result_dir()
        self.analysis_params = analysis_params

    def set_result_dir(self):
        self.result_dir = "{}/devices/{}/manips/{}/results/{}".format(self.base_dir, self.device, self.manip_name, self.result_name)

    def get_result_file_path(self):
        return "{}/{}".format(self.result_dir, self.result_file)

    def get_dataframe(self):
        result_file = self.get_result_file_path()
        return pd.read_csv(result_file, error_bad_lines=False)

    def get_params(self):
        self.analysis_params.update({"dataframe": self.get_dataframe()})
        self.analysis_params.update({"exp": self.result_name})
        return self.analysis_params

    def __str__(self):
        ret = ""
        ret += "device: {}\n".format(self.device)
        ret += "manip: {}\n".format(self.manip_name)
        ret += "result: {}\n".format(self.result_name)
        return ret


