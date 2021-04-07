import matplotlib.pyplot as plt
import numpy as np

from plotter import Plotter, PlotterType

from .results import CartoResult

def remove_0_values(data, labels):
    """Remove all the values to 0 from a data list and the corresponding index in a labels list.

    :param list data: the data list to remove the 0 from.
    :param list labels: the list labeling the data.

    :returns: the list of the data with the 0 values removed and the corresponding new labels list.

    """
    ret_data = []
    ret_labels = []
    for i, d in enumerate(data):
        if d != 0:
            ret_data.append(d)
            ret_labels.append(labels[i])
    return ret_data, ret_labels

def are_all_0(lists, index):
    """Check if the values at the same index in different list are all to 0.

    :param list lists: a list of lists to check the value in.
    :param int index: the index of the values to check in the lists.

    :returns: True if all the values at the index in the lists are set to 0, False if at least one of them is not 0.

    """
    for l in lists:
        if l[index] != 0:
            return False
    return True

def remove_0_values_multi(data_list, labels):
    """Remove all the values to 0 from several data set sharing the same labels.

    :param list data_list: a list of lists to remove the 0 values from.
    :param list labels: the labels labeling the data list.

    :returns: the data_list with the 0 values removed and the corresponding new labels list.

    """
    ret_data_list = [[] for i in range(len(data_list))]
    ret_labels = []
    for i in range(len(data_list[0])):
        if not are_all_0(data_list, i):
            for k, data in enumerate(data_list):
                ret_data_list[k].append(data[i])
            ret_labels.append(labels[i])
    return ret_data_list, ret_labels

def get_common_label_from_labels(labels):
    """Extract the common part from a set of strings. Also, the common part is removed for all the strings.

    :param list labels: the strings to get the common part from.

    :returns: a string which is the common part of the strings.

    """
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
    """A class that able to manage the way to plot a Result.

    """
    def __init__(self, styles, tmp_style, results=None):
        """Constructor of the class.

        :param Result result: the result containing the data to plot.

        """
        self.results = results
        """The result containing the data to plot."""
        self.tmp_style = tmp_style
        """The temporary plotting style to apply to the plot."""
        self.styles = styles

    def plot(self, style_name, data_to_plot_index_list=None, data_labels_index=None):
        """Check if the given plot style name is in the available styles. If so, plot the result data according to the given parameters.

        :param str style_name: the plot style to used for the plot.
        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        """
        if style_name in self.styles:
            self.style_name = style_name
            self.plot_result(self.styles[style_name], data_to_plot_index_list,
                             data_labels_index, latex=False)
        else:
            print("Error: unknown plot style")

    def get_matrix_to_plot(self):
        """Check the type of the result. If it is a CartoResult object, format the data for plotting a matrix.

        :returns: a Plotter compliant dictionary containing the information for plotting the result as a matrix if the result is a CartoResult object. None in the other case.

        """
        result = self.results[0]
        if type(result) == CartoResult:
            ret = {
                "data": np.array(result.data),
                "colorbar_label": result.label
            }
            return ret
        else:
            print("Error: result cannot be plot as a matrix")

    def get_multibar_to_plot(self, data_to_plot_index_list, data_labels_index):
        """Format the result data for plotting a multibar graph.

        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        :returns: a Plotter compliant dictionary containing the information for plotting the result as a multibar graph.

        """
        result = self.results[0]
        data_to_plot = [result.data[index] for index in data_to_plot_index_list]
        data_labels = result.data[data_labels_index]
        data_to_plot, data_labels = remove_0_values_multi(data_to_plot, data_labels)
        labels = [result.labels[index] for index in data_to_plot_index_list]
        label = get_common_label_from_labels(labels)
        ret = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": result.labels[data_labels_index],
            "bar_width": 0.6/len(data_to_plot),
            "y_label": label,
            "legend": labels
        }
        return ret

    def get_pie_to_plot(self, data_to_plot_index_list, data_labels_index):
        """Format the result data for plotting a pie graph.

        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        :returns: a Plotter compliant dictionary containing the information for plotting the result as a pie graph.

        """
        result = self.results[0]
        data_to_plot = result.data[data_to_plot_index_list[0]]
        data_labels = result.data[data_labels_index]
        data_to_plot, data_labels = remove_0_values(data_to_plot, data_labels)
        ret = {
            "data": data_to_plot,
            "labels": data_labels
        }
        return ret

    def get_bar_to_plot(self, data_to_plot_index_list, data_labels_index, remove_0=True):
        """Format the result data for plotting a bar graph.

        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        :returns: a Plotter compliant dictionary containing the information for plotting the result as a bar graph.

        """
        result = self.results[0]
        data_to_plot = result.data[data_to_plot_index_list[0]]
        data_labels = result.data[data_labels_index]
        if remove_0:
            data_to_plot, data_labels = remove_0_values(data_to_plot, data_labels)
        ret = {
            "data": data_to_plot,
            "x_ticklabels": data_labels,
            "x_label": result.labels[data_labels_index],
            "y_label": result.labels[data_to_plot_index_list[0]]
        }
        return ret

    def get_plot_to_plot(self, data_to_plot_index_list, data_labels_index):
        """Format the result data for plotting a default plot. The default plot
        requires the X values and Y values. The labels are considered as the X
        values and therefore must be values.

        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        :returns: a Plotter compliant dictionary containing the information for plotting the result as a bar graph.

        """
        result = self.results[0]
        data_to_plot_X = result.data[data_labels_index]
        data_to_plot_Y = result.data[data_to_plot_index_list[0]]
        ret = {
            "data": [data_to_plot_X, data_to_plot_Y],
            "x_label": result.labels[data_labels_index],
            "y_label": result.labels[data_to_plot_index_list[0]]
        }
        return ret

    def get_multiplot_to_plot(self, data_to_plot_index_list, data_labels_index):
        result = self.results[0]
        data_to_plot_X = result.data[data_labels_index]
        data_to_plot_Y = [result.data[index] for index in data_to_plot_index_list]
        labels = [result.labels[index] for index in data_to_plot_index_list]
        label = get_common_label_from_labels(labels)
        ret = {
            "data": [data_to_plot_X, data_to_plot_Y],
            "x_label": result.labels[data_labels_index],
            "y_label": label,
            "legend": labels
        }
        return ret

    def get_multimatrixscatterbin_to_plot(self):
        legend = [r.title for r in self.results]
        common = get_common_label_from_labels(legend)
        legend = [l.rstrip() for l in legend]
        ret = {
            "data": [r.data for r in self.results],
            "legend": legend
        }
        return ret

    def get_to_plot(self, plot_style, data_to_plot_index_list=None, data_labels_index=None):
        """Check if the type of the plot_style is available as a Plotter type plot. The supported type are: matrix, matrixscatter, multibar, pie and bar. If so, check that the needed parameters are set. If so, return the formated data for plotitng.

        :param dict plot_style: the style information for the plot.
        :param list data_to_plot_index_list: the list of the index of the data to use as data for the plot.
        :param int data_labels_index: the index of the data to use as labels for the plot.

        """
        to_plot = None
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
        elif plot_style["type"] in ["plot", PlotterType.PLOT]:
            if (data_to_plot_index_list != None) and (data_labels_index != None):
                to_plot = self.get_plot_to_plot(data_to_plot_index_list, data_labels_index)
            else:
                print("Error: missing arguments")
        elif plot_style["type"] in ["multiplot", PlotterType.MULTIPLOT]:
            if (data_to_plot_index_list != None) and (data_labels_index != None):
                to_plot = self.get_multiplot_to_plot(data_to_plot_index_list, data_labels_index)
            else:
                print("Error: missing arguments")
        elif plot_style["type"] in ["multimatrixscatterbin", PlotterType.MULTIMATRIXSCATTERBIN]:
            to_plot = self.get_multimatrixscatterbin_to_plot()

        if to_plot != None:
            to_plot.update(plot_style)
            to_plot.update(self.tmp_style)

        return to_plot

    def plot_result(self, plot_style, data_to_plot_index_list=None,
                    data_labels_index=None, latex=False):
        to_plot = self.get_to_plot(plot_style, data_to_plot_index_list, data_labels_index)
        if to_plot != None:
            cmap = plt.cm.YlOrRd
            cmap = plt.get_cmap("autumn_r")
            pl = Plotter([to_plot], cmap=cmap, latex=latex)
            pl.show()
        else:
            print("Error: unable to generate something to plot in plot_result()")

    def export_tikz(self, plot_style, data_to_plot_index_list=None,
                    data_labels_index=None, filename="tikz_figure.tex"):
        if plot_style in self.styles:
            to_plot = self.get_to_plot(self.styles[plot_style], data_to_plot_index_list, data_labels_index)
            if to_plot != None:
                cmap = plt.cm.YlOrRd
                cmap = plt.get_cmap("autumn_r")
                pl = Plotter([to_plot], cmap=cmap)
                pl.export_tikz(filename=filename)
            else:
                print("Error: unable to generate something to plot in export_tikz()")
        else:
            print("Error: unknown plot style")
