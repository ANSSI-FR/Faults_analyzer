from prettytable import PrettyTable
from plotter import Plotter, PlotterType

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

class Result():

    title = ""
    data = ""
    labels = ""

    def __init__(self, title, data, labels):
        self.title = title
        self.data = data
        self.labels = labels
        self.table = self.create_prettytable()

    def create_prettytable(self):
        t = PrettyTable()
        for i, col in enumerate(self.data):
            if len(col) > 0:
                t.add_column(self.labels[i], col)
        return t

    def get_str(self):
        return "{}\n{}".format(self.title, self.table.get_string())

    def __str__(self):
        return self.get_str()

    def get_html_str(self):
        return "<h2>{}</h2>\n{}".format(self.title, self.table.get_html_string())

    def get_latex_str(self):
        ret = "{}\n\\caption".format(self.table.get_latex_string())
        ret += "{" + self.title + "}"
        return ret

    def get_to_plot(self, to_plot_params):
        if (to_plot_params["type"] is PlotterType.PIE) or (to_plot_params["type"] == "pie"):
            return self.result_to_pie(to_plot_params)
        if (to_plot_params["type"] is PlotterType.BAR) or (to_plot_params["type"] == "bar"):
            return self.result_to_bar(to_plot_params)
        if (to_plot_params["type"] is PlotterType.MULTIBAR) or (to_plot_params["type"] == "multibar"):
            return self.result_to_multibar(to_plot_params)

    def result_to_multibar(self, to_plot_params):
        data = self.get_data_from_index_list(self.data, to_plot_params["data_to_plot"])
        data_labels = self.get_data_from_index_list(self.labels, to_plot_params["data_to_plot"])
        label = get_common_label_from_labels(data_labels)
        to_plot = {"data": data,
                   "x_ticklabels": self.data[to_plot_params["labels"]],
                   "type": PlotterType.MULTIBAR,
                   "x_label": self.labels[to_plot_params["labels"]],
                   "y_label": label,
                   "bar_width": 0.6/len(data),
                   "legend": data_labels,
                   "x_label_fontsize": 16,
                   "y_label_fontsize": 16,
                   "x_ticklabels_fontsize": 16,
                   "y_ticklabels_fontsize": 16,
                   "legend_fontsize": 16
        }
        return to_plot

    def get_data_from_index_list(self, data, index_list):
        ret = []
        for index in index_list:
            ret.append(data[index])
        return ret

    def result_to_bar(self, to_plot_params):
        to_plot = {"data": self.data[to_plot_params["data_to_plot"][0]],
                   "x_ticklabels": self.data[to_plot_params["labels"]],
                   "type": PlotterType.BAR,
                   "x_label": self.labels[to_plot_params["labels"]],
                   "y_label": self.labels[to_plot_params["data_to_plot"][0]]}
        return to_plot

    def result_to_pie(self, to_plot_params):
        to_plot = {"data": self.data[to_plot_params["data_to_plot"][0]],
                   "labels": self.data[to_plot_params["labels"]],
                   "type": PlotterType.PIE}
        return to_plot

######### TEST ###########
if __name__ == "__main__":
    res = {
        "title": "Test title",
        "data": [["one", "two", "three", "four", "five"], [4,5,6,36,9], [45,8,7,69,5]],
        "labels": ["name", "number of a", "number of b"]
    }

    r = Result(**res)
    print(r)
    print(r.get_html_str())
    print(r.get_latex_str())

    to_plot_params_list = [
        {
            "type": PlotterType.MULTIBAR,
            "data_to_plot": [1,2],
            "labels": 0
        },
        {
            "type": PlotterType.BAR,
            "data_to_plot": [1],
            "labels": 0
        },
        {
            "type": PlotterType.PIE,
            "data_to_plot": [1],
            "labels": 0
        },
    ]

    to_plot = []
    for to_plot_params in to_plot_params_list:
        to_plot.append(r.get_to_plot(to_plot_params))
    pl = Plotter(to_plot)
    pl.show()
