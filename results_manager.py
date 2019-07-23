from cmd_interface import CmdInterface
from utils import str_to_index_list
from results import *

class ResultsManager(CmdInterface):

    local_help_msg = """
    p, print (result_index) (table_index) : print the available results
        if result_index is given: print the available tables in the corresponding result
        if result_index and table_index are given: print the corresponding table in the corresponding result
            result_index can be a coma separated list (for instance "1,2,4") or a range (for instance "2-8") or "a" or "all" to print every table

    m, merge <results_index_list> <table_index> <columns_to_merge> <columns_in_common> : create a new result which contain the merged table from the available results
        results_index_list is the index of the results to merge from
        table_index is the index of the table to merge
        columns_to_merge is the columns to merge, it can be a coma separated list, a range, "a" or "all"
        columns_in_common is the columns in common, i.e. to include in the new result but not to duplicate, it can be a coma separated list, a range, "a" or "all"

    pl, plot <result_index> <table_index> <plot_type> <data> <labels> : plot the data from the table of the result with the corresponding type using the labels.
    """
    help_msg = CmdInterface.help_msg + local_help_msg

    def __init__(self, results_list):
        self.results_list = results_list
        self.results_str = ""
        self.done = False

    def get_results_lists_titles(self):
        ret = ""
        for i, results in enumerate(self.results_list):
            ret += "[{}] {}\n".format(i, results.exp)
        return ret

    def get_result_tables_titles(self, results_index):
        return self.results_list[results_index].get_results_titles_str()

    def format_index_list(self, index_list):
        if type(index_list) is list:
            return index_list
        elif type(index_list) is str:
            return str_to_index_list(index_list)

    def add_set_result_table_to_str(self, results_index, result_table_index_list):
        result_table_index_list = self.format_index_list(result_table_index_list)
        for result_table_index in result_table_index_list:
            self.add_result_table_to_str(results_index, result_table_index)

    def add_result_table_to_str(self, results_index, result_table_index):
        self.results_str += self.results_list[results_index].get_result_table_str(result_table_index)
        self.results_str += "\n"

    def add_results_table_to_str(self, results_index):
        self.results_str += self.results_list[results_index].get_results_table_str()
        self.results_str += "\n"

    def clear_results_str(self):
        self.results_str = ""

    def get_results_str(self):
        return self.results_str

    def eval_print_cmd(self, cmd):
        to_print = ""
        if len(cmd) == 1:
            to_print = self.get_results_lists_titles()
        elif len(cmd) == 2:
            index = int(cmd[1])
            to_print = self.get_result_tables_titles(index)
        elif len(cmd) == 3:
            result_index = int(cmd[1])
            table_index = cmd[2]
            self.clear_results_str()
            if table_index in ["a", "all"]:
                self.add_results_table_to_str(result_index)
            else:
                self.add_set_result_table_to_str(result_index, table_index)
            to_print = self.results_str
        print(to_print)

    def get_reduced_results_list(self, results_index_str):
        if results_index_str in ["a", "all"]:
            return self.results_list
        else:
            index_list = str_to_index_list(results_index_str)
            ret = []
            for index in index_list:
                ret.append(self.results_list[index])
            return ret

    def eval_merge_cmd(self, cmd):
        reduced_results_list = self.get_reduced_results_list(cmd[1])
        table_to_merge = int(cmd[2])
        nb_columns = len(reduced_results_list[0].get_result_from_index(table_to_merge)["labels"])
        columns_to_merge = str_to_binary_table(cmd[3], nb_columns)
        columns_in_common = str_to_binary_table(cmd[4], nb_columns)
        results = merge_results(reduced_results_list, table_to_merge, columns_to_merge, columns_in_common)
        self.results_list.append(results)

    def eval_plot_cmd(self, cmd):
        results_index = int(cmd[1])
        table_index = int(cmd[2])
        plot_type = cmd[3]
        data = str_to_index_list(cmd[4])
        labels = int(cmd[5])
        pl = self.results_list[results_index].get_plotter(table_index, plot_type, data, labels)
        pl.show()

    def eval_cmd(self, cmd):
        super().eval_cmd(cmd)
        parsed_cmd = cmd.split(" ")
        if parsed_cmd[0] in ["p", "print"]:
            self.eval_print_cmd(parsed_cmd)
        if parsed_cmd[0] in ["m", "merge"]:
            self.eval_merge_cmd(parsed_cmd)
        if parsed_cmd[0] in ["pl", "plot"]:
            if len(parsed_cmd) == 6:
                self.eval_plot_cmd(parsed_cmd)
            else:
                print("Error: wrong number of arguments")
