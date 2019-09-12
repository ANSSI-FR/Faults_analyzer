import matplotlib.pyplot as plt
import numpy as np

from plotter import Plotter, PlotterType
from plot_styles import styles, tmp_style
from results import CartoResult

def remove_0_values(data, labels):
    ret_data = []
    ret_labels = []
    for i, d in enumerate(data):
        if d != 0:
            ret_data.append(d)
            ret_labels.append(labels[i])
    return ret_data, ret_labels

def are_all_0(lists, index):
    for l in lists:
        if l[index] != 0:
            return False
    return True

def remove_0_values_multi(data_list, labels):
    ret_data_list = [[] for i in range(len(data_list))]
    ret_labels = []
    for i in range(len(data_list[0])):
        if not are_all_0(data_list, i):
            for k, data in enumerate(data_list):
                ret_data_list[k].append(data[i])
            ret_labels.append(labels[i])
    return ret_data_list, ret_labels

def get_common_label_from_labels(labels):
    split_labels = []
    ret = ""
    for label in labels:
        split_labels.append(label.split(" "))
    for word in split_labels[0]:
        in_all = True
        for split_label in split_labels:
            if not word in split_label:
                in_all = False
        if in_all:
            for i, label in enumerate(labels):
                labels[i] = label.replace(word, "")
            ret += word + " "
    return ret

class PlotManager():
    def __init__(self, result):
        self.result = result

    def plot(self, style_name, data_to_plot_index_list=None, data_labels_index=None):
        if style_name in styles:
            self.plot_result(styles[style_name], data_to_plot_index_list,
                             data_labels_index)
        else:
            print("Error: unknown plot style")

    def get_matrix_to_plot(self):
        if type(self.result) == CartoResult:
            ret = {
                "data": np.array(self.result.data),
                "colorbar_label": self.result.label
            }
            return ret
        else:
            print("Error: result cannot be plot as a matrix")

    def get_multibar_to_plot(self, data_to_plot_index_list, data_labels_index):
        data_to_plot = [self.result.data[index] for index in data_to_plot_index_list]
        data_labels = self.result.data[data_labels_index]
        data_to_plot, data_labels = remove_0_values_multi(data_to_plot, data_labels)
        labels = [self.result.labels[index] for index in data_to_plot_index_list]
        label = get_common_label_from_labels(labels)
        ret = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": self.result.labels[data_labels_index],
            "bar_width": 0.6/len(data_to_plot),
            "y_label": label,
            "legend": labels
        }
        return ret

    def get_pie_to_plot(self, data_to_plot_index_list, data_labels_index):
        data_to_plot = self.result.data[data_to_plot_index_list[0]]
        data_labels = self.result.data[data_labels_index]
        data_to_plot, data_labels = remove_0_values(data_to_plot, data_labels)
        ret = {
            "data": data_to_plot,
            "labels": data_labels
        }
        return ret

    def get_bar_to_plot(self, data_to_plot_index_list, data_labels_index):
        data_to_plot = self.result.data[data_to_plot_index_list[0]]
        data_labels = self.result.data[data_labels_index]
        data_to_plot, data_labels = remove_0_values(data_to_plot, data_labels)
        ret = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": self.result.labels[data_labels_index],
            "y_label": self.result.labels[data_to_plot_index_list[0]]
        }
        return ret

    def plot_result(self, plot_style, data_to_plot_index_list=None,
                    data_labels_index=None):
        if plot_style["type"] in ["matrix", "matrixscatter",
                                  PlotterType.MATRIX, PlotterType.MATRIXSCATTER]:
            to_plot = self.get_matrix_to_plot()
        elif plot_style["type"] in ["multibar", PlotterType.MULTIBAR]:
            if (data_to_plot_index_list != None) and (data_labels_index != None):
                to_plot = self.get_multibar_to_plot(data_to_plot_index_list,
                                                    data_labels_index)
            else:
                print("Error: missing arguments")
        elif plot_style["type"] in ["pie", PlotterType.PIE]:
            if (data_to_plot_index_list != None) and (data_labels_index != None):
                to_plot = self.get_pie_to_plot(data_to_plot_index_list,
                                                    data_labels_index)
            else:
                print("Error: missing arguments")
        elif plot_style["type"] in ["bar", PlotterType.BAR]:
            if (data_to_plot_index_list != None) and (data_labels_index != None):
                to_plot = self.get_bar_to_plot(data_to_plot_index_list,
                                                    data_labels_index)
            else:
                print("Error: missing arguments")


        if to_plot != None:
            to_plot.update(plot_style)
            to_plot.update(tmp_style)
            pl = Plotter([to_plot], cmap=plt.cm.YlOrRd)
            pl.show()
