import numpy as np

import matplotlib.pyplot as plt

import plot_styles

from plotter import Plotter, PlotterType
from cmd_interface import CmdInterface
from utils import str_to_index_list
from results import *
from result import get_common_label_from_labels

class ResultsManager(CmdInterface):
    def __init__(self, results_list=[], cmap=plt.cm.YlOrRd, latex=False):
        super().__init__()
        self.results_list = results_list
        self.cmap = cmap
        self.latex = latex

    def get_results_index(self, results):
        return self.results_list.index(results)

    def add_results(self, results):
        self.results_list.append(results)

    def get_results_lists_titles(self):
        ret = ""
        for i, results in enumerate(self.results_list):
            ret += "[{}] {}\n".format(i, results.id_name)
        return ret

    def get_result_tables_titles(self, results_index):
        return self.results_list[results_index].get_results_titles_str()

    get_results_titles = get_result_tables_titles

    def get_all_results_str(self, results_index):
        return str(self.results_list[results_index])

    def get_results_str(self, results_index, result_index_list):
        ret = ""
        for i in result_index_list:
            ret += str(self.results_list[results_index].get_result(i)) + "\n"
        return ret

    def eval_print_cmd(self, cmd):
        if len(cmd) == 1:
            print(self.get_results_lists_titles())
        elif len(cmd) == 2:
            index = int(cmd[1])
            print(self.get_result_tables_titles(index))
        elif len(cmd) == 3:
            result_index = int(cmd[1])
            table_index = cmd[2]
            if table_index in ["a", "all"]:
                print(self.results_list[result_index])
            else:
                index_list = str_to_index_list(table_index)
                print(self.results_list[result_index].id_name)
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
        results = Results([result], "Merged results")
        self.results_list.append(results)
        print("Merge done.")

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
        if to_plot != None:
            pl = Plotter([to_plot], cmap=self.cmap, latex=self.latex)
            pl.show()

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

