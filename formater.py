from prettytable import PrettyTable
from plotter import Plotter, PlotterType, types_str

class Formater():

    def __init__(self, results):
        self.results = results
        self.to_print = [True] * len(self.results)
        self.to_plot = [False] * len(self.results)

    def _create_table(self, labels, data):
        t = PrettyTable()
        for i, col in enumerate(data):
            t.add_column(labels[i], col)
        return t

    def set_all_to_print(self, v):
        self.to_print = [v] * len(self.results)

    def toggle_to_print(self, i):
        self.to_print[i] = not self.to_print[i]

    def get_printable_str(self): 
        ret_str = ""
        for i, result in enumerate(self.results):
            if self.to_print[i]:
                local_res = result.copy()
                title = local_res.pop("title")
                t = self._create_table(**local_res)
                ret_str += "\n" + title + "\n"
                ret_str += t.get_string() + "\n"
        return ret_str

    def get_html_str(self):
        ret_str = ""
        for i, result in enumerate(self.results):
            if self.to_print[i]:
                local_res = result.copy()
                title = local_res.pop("title")
                t = self._create_table(**local_res)
                ret_str += "<h2>" + title + "</h2>"
                ret_str += t.get_html_string() + "<br>"
        return ret_str

    def result_to_pie(self, result, to_plot):
        to_plot = {"data": result["data"][to_plot["data_to_plot"][0]],
                   "labels": result["data"][to_plot["labels"]],
                   "type": PlotterType.PIE}
        return to_plot

    def result_to_bar(self, result, to_plot):
        to_plot = {"data": result["data"][to_plot["data_to_plot"][0]],
                   "x_ticklabels": result["data"][to_plot["labels"]],
                   "type": PlotterType.BAR,
                   "x_label": result["labels"][to_plot["labels"]],
                   "y_label": result["labels"][to_plot["data_to_plot"]]}
        return to_plot

    def get_data_from_index_list(self, result, index_list):
        ret = []
        for index in index_list:
            ret.append(result["data"][index])
        return ret

    def get_data_labels_from_index_list(self, result, index_list):
        ret = []
        for index in index_list:
            ret.append(result["labels"][index])
        return ret

    def get_common_label_from_labels(self, labels):
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


    def result_to_multibar(self, result, to_plot):
        data = self.get_data_from_index_list(result, to_plot["data_to_plot"])
        data_labels = self.get_data_labels_from_index_list(result, to_plot["data_to_plot"])
        label = self.get_common_label_from_labels(data_labels)
        to_plot = {"data": data,
                   "x_ticklabels": result["data"][to_plot["labels"]],
                   "type": PlotterType.MULTIBAR,
                   "x_label": result["labels"][to_plot["labels"]],
                   "y_label": label,
                   "bar_width": 0.6/len(data),
                   "legend": data_labels
        }
        return to_plot

    def result_to_plot(self, result, to_plot):
        if (to_plot["type"] is PlotterType.PIE) or (to_plot["type"] == "pie"):
            return self.result_to_pie(result, to_plot)
        if (to_plot["type"] is PlotterType.BAR) or (to_plot["type"] == "bar"):
            return self.result_to_bar(result, to_plot)
        if (to_plot["type"] is PlotterType.MULTIBAR) or (to_plot["type"] == "multibar"):
            return self.result_to_multibar(result, to_plot)

    def remove_all_to_plot(self):
        self.to_plot = [False] * len(self.results)

    def set_to_plot(self, result_index, plot_type, data_to_plot=1, data_labels=0):
        """Add a rule for plotting the target result.

        Arguments:

        result_index (int) - The index of the result to plot. The result is a
        table.

        plot_type (PlotterType) - The way to plot the result.

        data_to_plot (int) - The column index of the data to plot from the
        result. Default value is 1.

        data_labels (int) - The column index to use as labels from the result. Default
        value is 0.

        Example:

        Considering the following result table with the call
        set_to_plot(result_index, plot_type, 1, 0):

        +----------+------------+
        | City     | Population | <-- used as axis labels if needed
        +----------+------------+
        | New York | 8623000    |
        | Paris    | 2141000    |
        | London   | 8136000    |
        +----------+------------+
           /|\          /|\
            |            |
         used as       used as
        labels in     data in
        the plot       the plot

        """
        if (plot_type in PlotterType) or (plot_type in types_str):
            i = result_index
            self.to_plot[i] = {
                "type": plot_type,
                "data_to_plot": data_to_plot,
                "labels": data_labels
            }

    def get_plotter(self):
        to_plot = []
        for i, result in enumerate(self.results):
            if self.to_plot[i] != False:
                to_plot.append(self.result_to_plot(result, self.to_plot[i]))
        return Plotter(to_plot)
