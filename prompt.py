from cmd import Cmd
from manips_manager import ManipsManager
from utils import str_to_index_list, intable
from analyzer import Analyzer
from results import Results, merge_results
from results_manager import ResultsManager
from carto_analyzer import CartoAnalyzer

def check_nb_args(cmd, maxi=None, mini=1):
    if len(cmd) < mini:
        print("Error: wrong number of arguments")
        return False
    if maxi != None:
        if len(cmd) > maxi:
            print("Error: wrong number of arguments")
            return False
    return True

class Prompt(Cmd):

    prompt = "fa> "
    intro = "Welcome! Type ? to list commands"
    exit_msg = "I hope to see you soon !"

    def __init__(self, manips):
        super().__init__()
        self.mm = ManipsManager(manips)
        self.rm = ResultsManager()
        self.merged_results = None

    def get_manip_results(self, manip_index):
        if self.mm.manips[manip_index].analyzed:
            id_name = self.mm.manips[manip_index].id_name
            return self.rm.get_results_from_id_name(id_name)

    def get_manip_results_index(self, manip_index):
        if self.mm.manips[manip_index].analyzed:
            id_name = self.mm.manips[manip_index].id_name
            return self.rm.get_results_index_from_id_name(id_name)

    def default(self, inp):
        inp_split = inp.split(" ")
        cmd = inp_split[0]
        args = inp_split[1:]
        if cmd == "a":
            return self.do_analyze(args)
        elif cmd == "e":
            return self.do_exit(args)
        elif cmd == "p":
            return self.print_data(args)
        elif cmd == "r":
            return self.remove(args)
        elif cmd == "s":
            return self.select(args)
        elif cmd == "m":
            return self.merge(args)
        else:
            super().default(inp)

    def get_results_from_manips_index_list(self, index_list):
        results_list = []
        for manip_index in index_list:
            results_index = self.get_manip_results_index(manip_index)
            results_list.append(self.rm.results_list[results_index])
        return results_list

    def merge(self, args):
        if check_nb_args(args, maxi=4, mini=4):
            manips_index_list = str_to_index_list(args[0])
            results_list = self.get_results_from_manips_index_list(manips_index_list)
            result_to_merge = int(args[1])
            columns_to_merge = str_to_index_list(args[2])
            columns_in_common = str_to_index_list(args[3])
            merged_result = merge_results(results_list, result_to_merge,
                                          columns_to_merge, columns_in_common)
            if self.merged_results == None:
                merged_results = Results([merged_result], "Merged results")
                self.rm.add_results(merged_results)
                self.mm.add_manip("",{},"Merged results")
            else:
                self.merged_results.add_result(**merged_result)

    def do_merge(self, inp):
        inp = inp.rstrip().split(" ")
        self.merge(inp)

    def plot(self, args):
        if check_nb_args(args, maxi=5, mini=3):
            manip_index = int(args[0])
            results_index = self.get_manip_results_index(manip_index)
            result_index = int(args[1])
            style_name = args[2]
            if len(args) == 5:
                data_to_plot_index_list = str_to_index_list(args[3])
                data_labels = int(args[4])
                self.rm.plot_result(results_index, result_index, style_name,
                                    data_to_plot_index_list, data_labels)
            elif len(args) == 4:
                print("Error: data labels index is missing")
            else:
                self.rm.plot_result(results_index, result_index, style_name)

    def do_plot(self, inp):
        inp = inp.rstrip().split(" ")
        self.plot(inp)

    def save(self, args):
        if check_nb_args(args, maxi=2, mini=2):
            manip_index = int(args[0])
            filename = args[1]
            results_index = self.get_manip_results_index(manip_index)
            self.rm.save(results_index, filename)

    def do_save(self, inp):
        inp = inp.rstrip().split(" ")
        self.save(inp)

    def load(self, args):
        if check_nb_args(args, maxi=1, mini=1):
            filename = args[0]
            self.rm.load(filename)
            id_name = self.rm.results_list[-1].id_name
            self.mm.get_manip_from_id_name(id_name).analyzed = True

    def do_load(self, inp):
        inp = inp.rstrip().split(" ")
        self.load(inp)

    def do_analyze(self, inp):
        manips_to_analyze = self.mm.get_selected_manips()
        for manip in manips_to_analyze:
            if not manip.analyzed:
                params = manip.get_params()
                if manip.carto:
                    anal = CartoAnalyzer(progress=True, **params)
                else:
                    anal = Analyzer(progress=True, **params)
                results = Results(anal.get_results(), manip.id_name)
                self.rm.add_results(results)
                manip.analyzed = True

    def do_exit(self, inp):
        print(self.exit_msg)
        return True

    def check_arg_and_get_result_titles(self, manip_index):
        if intable(manip_index):
            manip_index = int(manip_index)
            return self.get_result_titles(manip_index)
        else:
            print("Error: wrong argument")

    def get_result_titles(self, manip_index):
        results_index = self.get_manip_results_index(manip_index)
        if results_index == None:
            print("Error: analysis not done")
            return
        return self.rm.get_result_titles(results_index)

    def check_args_and_get_result(self, manip_index, result_index_list):
        if intable(manip_index):
            manip_index = int(manip_index)
            results_index = self.get_manip_results_index(manip_index)
            if results_index == None:
                print("Error: analysis not done")
                return
            if result_index_list in ["a", "all"]:
                return self.rm.get_all_result_str(results_index)
            else:
                result_index_list = str_to_index_list(result_index_list)
                if not result_index_list == None:
                    return self.rm.get_result_str(results_index, result_index_list)

    def get_to_print(self, args):
        if len(args) == 0:
            return self.mm.get_manips_str()
        elif len(args) == 1:
            return self.check_arg_and_get_result_titles(args[0])
        elif len(args) == 2:
            return self.check_args_and_get_result(args[0], args[1])
        else:
            return "Error: wrong number of arguments"

    def print_data(self, args):
        to_print = self.get_to_print(args)
        if to_print != None:
            print(to_print)

    def do_print(self, inp):
        inp = inp.rstrip().split(" ")
        self.print_data(inp)

    def select(self, args):
        if check_nb_args(args, maxi=1, mini=1):
            if args[0] in ["a", "all"]:
                self.mm.select_all_manips()
            else:
                index_list = str_to_index_list(args[0])
                if not index_list == None:
                    self.mm.select_manips(index_list)

    def do_select(self, inp):
        inp = inp.rstrip().split(" ")
        self.select(inp)

    def remove(self, args):
        if check_nb_args(args, maxi=1, mini=1):
            if args[0] in ["a", "all"]:
                self.mm.remove_all_manips()
            else:
                index_list = str_to_index_list(args[0])
                if not index_list == None:
                    self.mm.remove_manips(index_list)

    def do_remove(self, inp):
        inp = inp.rstrip().split(" ")
        self.remove(inp)
