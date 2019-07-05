import logging

from formater import Formater

def get_merged_labels(results_list, result_to_merge, columns_to_merge,
                      columns_in_common):
    ret = []
    for i_res, results in enumerate(results_list):
        labels = results.get_result(result_to_merge)["labels"]
        for i, label in enumerate(labels):
            if columns_to_merge[i]:
                if columns_in_common[i]:
                    if i_res == 0:
                        ret.append(label)
                else:
                    to_append = "{} - {}".format(label, results.exp.split("/")[-2])
                    ret.append(to_append)
    return ret

def get_merged_data(results_list, result_to_merge, columns_to_merge,
                    columns_in_common):
    ret = []
    for i_res, results in enumerate(results_list):
        data = results.get_result(result_to_merge)["data"]
        for i, d in enumerate(data):
            if columns_to_merge[i]:
                if columns_in_common[i]:
                    if i_res == 0:
                        ret.append(d)
                else:
                    ret.append(d)
    return ret

def get_merged_exp(results_list):
    ret = "Merged results of ["
    for results in results_list:
        ret += "{}, ".format(results.exp.split("/")[-2])
    ret += "]"
    return ret

def merge_results(results_list, result_to_merge, columns_to_merge,
                  columns_in_common):
    merged_title = result_to_merge
    merged_labels = get_merged_labels(results_list, result_to_merge,
                                      columns_to_merge, columns_in_common)
    merged_data = get_merged_data(results_list, result_to_merge,
                                  columns_to_merge, columns_in_common)
    merged_result = {
        "title": merged_title,
        "labels": merged_labels,
        "data": merged_data
    }

    merged_exp = get_merged_exp(results_list)

    ret = Results(merged_exp)
    ret.add_result(merged_result)

    return ret

class Results():

    """Class for storing and managing the results of an experiment.

    """

    exp = None
    results = []
    nb_results = 0

    def __init__(self, exp, results=[]):
        self.exp = exp
        self.set_results(results)

    def get_results(self):
        return self.results

    def set_results(self, results):
        self.results = results
        self.nb_results = len(self.results)
        self.form = Formater(self.results)

    def add_result(self, result):
        self.results.append(result)
        self.nb_results += 1
        self.form = Formater(self.results)

    def get_result(self, result):
        for res in self.results:
            if res["title"] == result:
                return res

    def get_result_index(self, result):
        if type(result) == int:
            return result
        elif type(result) == str:
            for i in range(self.nb_results):
                if self.results[i]["title"] == result:
                    return i
        else:
            logging.error("Cannot find index for result '{}'".format(result))
    
    def get_results_titles(self):
        ret = []
        for res in self.results:
            ret.append(res["title"])
        return ret

    def get_results_titles_str(self):
        titles = self.get_results_titles()
        ret = ""
        for i, title in enumerate(titles):
            ret += "[{}] {}\n".format(i, title)
        return ret

    def get_results_table_str(self):
        self.form.set_all_to_print(True)
        return self.form.get_printable_str()

    def get_result_table_str(self, result):
        result_index = self.get_result_index(result)
        self.form.set_all_to_print(False)
        self.form.toggle_to_print(result_index)
        return self.form.get_printable_str()

    def get_results_html_str(self):
        self.form.set_all_to_print(True)
        return self.form.get_html_str()

    def get_result_table_str(self, result):
        result_index = self.get_result_index(result)
        self.form.set_all_to_print(False)
        self.form.toggle_to_print(result_index)
        return self.form.get_printable_str()

    def set_to_plot(self, result, plot_type, data_to_plot, data_labels):
        result_index = self.get_result_index(result)
        self.form.set_to_plot(result_index, plot_type, data_to_plot,
                              data_labels)

    def get_label_index(self, result, label):
        if type(label) == int:
            return label
        elif type(label) == str:
            result_index = self.get_result_index(result)
            labels = self.results[result_index]["labels"]
            for i in range(len(labels)):
                if labels[i] == label:
                    return i
        else:
            logging.error("Cannot find index for label '{}'".format(label))

    def get_plotter(self, result, plot_type, data_to_plot, data_labels):
        result_index = self.get_result_index(result)
        label_index = self.get_label_index(result, data_labels)
        data_index = self.get_label_index(result, data_to_plot)
        self.form.remove_all_to_plot()
        self.form.set_to_plot(result_index, plot_type, data_index, label_index)
        return self.form.get_plotter()
