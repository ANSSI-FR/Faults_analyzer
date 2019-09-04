import numpy as np

import matplotlib.pyplot as plt

import plot_styles

from plotter import Plotter, PlotterType
from cmd_interface import CmdInterface
from utils import str_to_index_list
from results import *
from result import get_common_label_from_labels

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

    s, save <result_index> <table_index> <filename> (format) : save the result in the file named filename. An optional format can be given among "txt", "html" and "latex" (default is "txt").
    """
    help_msg = CmdInterface.help_msg + local_help_msg

    def __init__(self, results_list, cmap=plt.cm.YlOrRd, latex=False):
        self.results_list = results_list
        self.results_str = ""
        self.done = False
        self.cmap = cmap
        self.latex = latex

    def get_results_lists_titles(self):
        ret = ""
        for i, results in enumerate(self.results_list):
            ret += "[{}] {} {} {}\n".format(i, results.device, results.manip,
                                            results.result_dir)
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
        if len(cmd) == 1:
            print(self.get_results_lists_titles())
        elif len(cmd) == 2:
            index = int(cmd[1])
            print(self.get_result_tables_titles(index))
        elif len(cmd) == 3:
            result_index = int(cmd[1])
            table_index = cmd[2]
            self.clear_results_str()
            if table_index in ["a", "all"]:
                print(self.results_list[result_index])
            else:
                index_list = str_to_index_list(table_index)
                print(self.results_list[result_index].get_path())
                for i in index_list:
                    print(self.results_list[result_index].get_result(i))

    def get_reduced_results_list(self, results_index_str):
        if results_index_str in ["a", "all"]:
            return self.results_list
        else:
            index_list = str_to_index_list(results_index_str)
            ret = []
            for index in index_list:
                ret.append(self.results_list[index])
            return ret

    def get_columns_to_merge_from_str(self, string, nb_col):
        if string in ["a", "all"]:
            return list(np.arange(nb_col))
        else:
            return str_to_index_list(string)

    def eval_merge_cmd(self, cmd):
        reduced_results_list = self.get_reduced_results_list(cmd[1])
        table_to_merge = int(cmd[2])
        nb_columns = len(reduced_results_list[0].get_result(table_to_merge).labels)
        columns_to_merge = self.get_columns_to_merge_from_str(cmd[3], nb_columns)
        columns_in_common = str_to_index_list(cmd[4])
        result = merge_results(reduced_results_list, table_to_merge,
                               columns_to_merge, columns_in_common)
        for results in reduced_results_list:
            results.add_result(result)
        print("Merge done.")

    def convert_arg(self, arg):
        try:
            return float(arg)
        except:
            return arg

    def get_plot_style_from_cmd(self, cmd, start_index):
        plot_style = {}
        for i in range(start_index, len(cmd)):
            arg = cmd[i].split("=")
            plot_style.update({arg[0]: self.convert_arg(arg[1])})
        return plot_style

    def get_plot_params(self, cmd):
        plot_type = cmd[3]
        if plot_type in [PlotterType.MATRIX, PlotterType.MATRIXSCATTER,
                         "matrix", "matrixscatter"]:
            params = {"type": plot_type}
            start_index = 4
        else:
            params = {
                "type": plot_type,
                "data_to_plot": str_to_index_list(cmd[4]),
                "labels": int(cmd[5])
            }
            start_index = 6
        params.update({"plot_style": self.get_plot_style_from_cmd(cmd, start_index)})
        return params

    def get_matrix_to_plot_for_style(self, result):
        if hasattr(result, "data") and hasattr(result, "label"):
            to_plot = {
                "data": result.data,
                "colorbar_label": result.label
            }
            return to_plot
        else:
            print("Error: wrong type of result, cannot be plot.")

    def get_pie_to_plot_for_style(self, result, data_index, labels_index):
        data_to_plot, data_labels = self.remove_0_values(result.data[data_index],
                                                         result.data[labels_index])
        to_plot = {
            "data": data_to_plot,
            "labels": data_labels
        }
        return to_plot

    def get_multibar_to_plot_for_style(self, result, data_index, labels_index):
        data_to_plot, data_labels = self.remove_0_values_multi([result.data[index] for index in data_index], result.data[labels_index])

        to_plot = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": result.labels[labels_index],
            "bar_width": 0.6/len(result.data),
        }

        labels = [result.labels[index] for index in data_index]
        label = get_common_label_from_labels(labels)
        to_plot.update({"y_label": label})
        to_plot.update({"legend": labels})
        return to_plot

    def remove_0_values(self, data, labels):
        ret_data = []
        ret_labels = []
        for i, d in enumerate(data):
            if d != 0:
                ret_data.append(d)
                ret_labels.append(labels[i])
        return ret_data, ret_labels

    def are_all_0(self, lists, index):
        for l in lists:
            if l[index] != 0:
                return False
        return True

    def remove_0_values_multi(self, data_list, labels):
        ret_data_list = [[] for i in range(len(data_list))]
        ret_labels = []
        for i in range(len(data_list[0])):
            if not self.are_all_0(data_list, i):
                for k, data in enumerate(data_list):
                    ret_data_list[k].append(data[i])
                ret_labels.append(labels[i])
        return ret_data_list, ret_labels

    def get_bar_to_plot_for_style(self, result, data_index, labels_index):
        data_to_plot, data_labels = self.remove_0_values(result.data[data_index],
                                                         result.data[labels_index])
        to_plot = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": result.labels[labels_index],
            "y_label": result.labels[data_index]
        }
        return to_plot

    def get_to_plot_from_style(self, results_index, table_index, style, cmd):
        result = self.results_list[results_index].get_result(table_index)

        if style["type"] in ["matrix", "matrixscatter", PlotterType.MATRIX, PlotterType.MATRIXSCATTER]:
            to_plot = self.get_matrix_to_plot_for_style(result)

        elif style["type"] in ["pie", PlotterType.PIE]:
            if len(cmd) == 6:
                data_index = int(cmd[4])
                labels_index = int(cmd[5])
                to_plot = self.get_pie_to_plot_for_style(result, data_index,
                                                          labels_index)
            else:
                print("Error: wrong number of arguments.")

        elif style["type"] in ["multibar", PlotterType.MULTIBAR]:
            if len(cmd) == 6:
                data_index = str_to_index_list(cmd[4])
                labels_index = int(cmd[5])
                to_plot = self.get_multibar_to_plot_for_style(result,
                                                              data_index,
                                                              labels_index)
            else:
                print("Error: wrong number of arguments.")

        elif style["type"] in ["bar", PlotterType.BAR]:
            if len(cmd) == 6:
                data_index = int(cmd[4])
                labels_index = int(cmd[5])
                to_plot = self.get_bar_to_plot_for_style(result, data_index,
                                                         labels_index)
            else:
                print("Error: wrong number of arguments.")

        if to_plot != None:
            to_plot.update(style)
            to_plot.update(plot_styles.temp)
            return to_plot

    def eval_plot_cmd(self, cmd):
        results_index = int(cmd[1])
        table_index = int(cmd[2])
        if cmd[3] in plot_styles.styles:
            style = plot_styles.styles[cmd[3]]
            to_plot = self.get_to_plot_from_style(results_index, table_index, style, cmd)
        else:
            params = self.get_plot_params(cmd)
            to_plot = self.results_list[results_index].get_result(table_index).get_to_plot(params)
        if to_plot != None:
            pl = Plotter([to_plot], cmap=self.cmap, latex=self.latex)
            pl.show()

    def check_nb_args(self, cmd, maxi=None, mini=1):
        # TODO: mettre dans la classe mère
        if len(cmd) < mini:
            print("Error: wrong number of arguments")
            return False
        if maxi != None:
            if len(cmd) > maxi:
                print("Error: wrong number of arguments")
                return False
        return True

    def get_save_style(self, cmd):
        style = "txt"
        if len(cmd) == 5:
            if cmd[4] in ["txt", "html", "latex"]:
                style = cmd[4]
        return style

    def get_to_write(self, results_index, table_index, style):
        to_write = ""
        if style == "txt":
            to_write = self.results_list[results_index].get_result(table_index).get_str()
        elif style == "html":
            to_write = self.results_list[results_index].get_result(table_index).get_html_str()
        elif style == "latex":
            to_write = self.results_list[results_index].get_result(table_index).get_latex_str()
        return to_write

    def eval_save_cmd(self, cmd):
        results_index = int(cmd[1])
        table_index = int(cmd[2])
        filename = cmd[3]
        style = self.get_save_style(cmd)
        f = open(filename, "a+")
        f.write(self.get_to_write(results_index, table_index, style) + "\n")
        f.close()
        print("Results saved in {}.".format(filename))

    def sanitize_cmd(self, cmd):
        #TODO: classe mere
        while "" in cmd:
            cmd.remove("")
        return cmd

    def eval_cmd(self, cmd):
        super().eval_cmd(cmd)
        parsed_cmd = cmd.split(" ")
        parsed_cmd = self.sanitize_cmd(parsed_cmd)
        if parsed_cmd[0] in ["p", "print"]:
            if self.check_nb_args(parsed_cmd, maxi=3):
                self.eval_print_cmd(parsed_cmd)
        elif parsed_cmd[0] in ["m", "merge"]:
            if self.check_nb_args(parsed_cmd, mini=5, maxi=5):
                self.eval_merge_cmd(parsed_cmd)
        elif parsed_cmd[0] in ["pl", "plot"]:
            if self.check_nb_args(parsed_cmd, mini=4):
                self.eval_plot_cmd(parsed_cmd)
        elif parsed_cmd[0] in ["s", "save"]:
            if self.check_nb_args(parsed_cmd, mini=4, maxi=5):
                self.eval_save_cmd(parsed_cmd)

