import logging
import json
from prettytable import PrettyTable
from utils import numpy_to_native_list

def merge_results(results_list, result_to_merge, columns_to_merge,
                  columns_in_common):
    merged_labels, merged_data = get_merged_labels_and_data(results_list,
                                                            result_to_merge,
                                                            columns_to_merge,
                                                            columns_in_common)
    merged_result_title = "Merged " + results_list[0].get_result(result_to_merge).title
    ret = {"title": merged_result_title,
           "data": merged_data,
           "labels": merged_labels}
    return ret

def get_merged_labels_and_data(results_list, result_to_merge, columns_to_merge,
                               columns_in_common):
    merged_data = []
    merged_labels = []
    for column_to_merge in columns_to_merge:
        if column_to_merge in columns_in_common:
            label = results_list[0].get_result(result_to_merge).labels[column_to_merge]
            data = results_list[0].get_result(result_to_merge).data[column_to_merge]
            merged_labels.append(label)
            merged_data.append(data)
        else:
            for results in results_list:
                label = "{} {}".format(results.id_name,
                                       results.get_result(result_to_merge).labels[column_to_merge])
                data = results.get_result(result_to_merge).data[column_to_merge]
                merged_labels.append(label)
                merged_data.append(data)
    return merged_labels, merged_data

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

    def get_dict(self):
        ret = {
            "title": self.title,
            "data": [numpy_to_native_list(d) for d in self.data],
            "labels": self.labels
        }
        return ret


class Results():

    """Class for storing and managing the results of an experiment.

    """
    def __init__(self, results, id_name):
        self.results = []
        self.id_name = id_name
        for result_dict in results:
            self.results.append(Result(**result_dict))
        self.nb_results = len(self.results)

    def save(self, filename):
        to_save = {
            "id_name": self.id_name,
            "results": [result.get_dict() for result in self.results]
        }
        fp = open(filename, "w")
        json.dump(to_save, fp)
        fp.close()

    def __str__(self):
        return self.get_str()

    def get_str(self):
        ret = "Results from {}\n".format(self.id_name)
        for res in self.results:
            ret += "{}\n".format(res)
        return ret

    def get_html_str(self):
        ret = "<h1>Results from {}</h1>\n".format(self.id_name)
        for res in self.results:
            ret += res.get_html_str() + "\n"
        return ret

    def get_results(self):
        return self.results

    def set_results(self, results):
        for result_dict in results:
            self.results.append(Result(**result_dict))
        self.nb_results = len(self.results)

    def add_result(self, title, data, labels):
        self.results.append(Result(title, data, labels))
        self.nb_results += 1

    def get_result_title(self, index):
        return self.results[index].title

    def get_result_from_title(self, result):
        for res in self.results:
            if res.title == result:
                return res

    def get_result(self, index):
        return self.results[index]

    def get_result_index(self, result):
        if type(result) == int:
            return result
        elif type(result) == str:
            for i in range(self.nb_results):
                if self.results[i].title == result:
                    return i
        else:
            logging.error("Cannot find index for result '{}'".format(result))

    def get_results_titles(self):
        ret = []
        for res in self.results:
            ret.append(res.title)
        return ret

    def get_results_titles_str(self):
        titles = self.get_results_titles()
        ret = ""
        for i, title in enumerate(titles):
            ret += "[{}] {}\n".format(i, title)
        return ret
