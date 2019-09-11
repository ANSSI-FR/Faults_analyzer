import numpy as np
import json
import matplotlib.pyplot as plt

import plot_styles

from plotter import Plotter, PlotterType
from utils import str_to_index_list

from result import get_common_label_from_labels
from results import Results

class ResultsManager():
    def __init__(self, results_list=[], cmap=plt.cm.YlOrRd, latex=False, result_dir="."):
        super().__init__()
        self.results_list = results_list
        self.cmap = cmap
        self.latex = latex
        self.result_dir = result_dir

    def get_results_index(self, results):
        return self.results_list.index(results)

    def add_results(self, results):
        self.results_list.append(results)

    def get_result_titles(self, results_index):
        if results_index < len(self.results_list):
            return self.results_list[results_index].get_results_titles_str()

    def get_all_result_str(self, results_index):
        if results_index < len(self.results_list):
            return str(self.results_list[results_index])

    def get_result_str(self, results_index, result_index_list):
        ret = ""
        if results_index < len(self.results_list):
            for i in result_index_list:
                if i < self.results_list[results_index].nb_results:
                    ret += str(self.results_list[results_index].get_result(i)) + "\n"
            return ret

    def save(self, results_index, filename):
        if results_index < len(self.results_list):
            self.results_list[results_index].save(filename)

    def load(self, filename):
        fp = open(self.result_dir + "/" + filename, "r")
        results_dict = json.loads(fp.read())
        self.results_list.append(Results(**results_dict))

    def get_results_from_id_name(self, id_name):
        for results in self.results_list:
            if results.id_name == id_name:
                return results

    def get_results_index_from_id_name(self, id_name):
        results = self.get_results_from_id_name(id_name)
        return self.results_list.index(results)

##### PLOTTING METHODS #####

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
