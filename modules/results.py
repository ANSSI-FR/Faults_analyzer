import json
from prettytable import PrettyTable

from .utils import numpy_to_native_list

def merge_results(results_list, result_to_merge, columns_to_merge,
                  columns_in_common):
    """Merge results into a new result.

    :param results_list: the list of results to merge the result from.
    :param result_to_merge: the index of the result to merge.
    :param columns_to_merge: the list of index of the columns to merge from the result.
    :param columns_in_common: the list of index of the columns to merge to include once in the merged result.

    :return: a dictionary containing the elements of a result.

    """
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
    """Extract the labels and the data to be merged.

    :param results_list: the list of results to merge the result from.
    :param result_to_merge: the index of the result to merge.
    :param columns_to_merge: the list of index of the columns to merge from the result.
    :param columns_in_common: the list of index of the columns to merge to include once in the merged result.

    :return: the merged labels and the merged data.

    """
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
    """Extract the common label from a label list. All the labels in the label list will have the common part removed.

    :param labels: the list of labels to extract the common part from.

    :return: the part of the labels.
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

class Result():
    """A class storing a result and formatting it. A result is a title describing the result, labels that describe the different values and the corresponding data.

    """
    def __init__(self, title, data, labels):
        """Constructor of a result. Initialize a prettytable object for printing the result.

        """
        self.title = title
        self.data = data
        self.labels = labels
        self.table = self.create_prettytable()

    def create_prettytable(self):
        """Create the prettytable object for printing the result.

        :return: a prettytable object containing the labels as head of columns and the data as columns.

        """
        t = PrettyTable()
        for i, col in enumerate(self.data):
            if len(col) > 0:
                t.add_column(self.labels[i], col)
        return t

    def get_str(self):
        """:return: a printable string which is a table containing the result.

        """
        return "{}\n{}".format(self.title, self.table.get_string())

    def __str__(self):
        """:return: a printable string which is a table containing the result.

        """
        return self.get_str()

    def get_html_str(self):
        """:return: a html string representing the result.

        """
        return "<h2>{}</h2>\n{}".format(self.title, self.table.get_html_string())

    def get_latex_str(self):
        """:return: a latex string representing the result.

        """
        ret = "{}\n\\caption".format(self.table.get_latex_string())
        ret += "{" + self.title + "}"
        return ret

    def get_dict(self):
        """:return: a dictionary representing the result.

        """
        ret = {
            "title": self.title,
            "data": self.data,
            "labels": self.labels
        }
        return ret

    def get_JSON_dict(self):
        """:return: a JSON compliant dictionary representing the result.

        """
        ret = {
            "title": self.title,
            "data": [numpy_to_native_list(d) for d in self.data],
            "labels": self.labels
        }
        return ret

class CartoResult():
    """A class a result from a cartography. This kind of result is described with a title, a label and data, usually a matrix.

    """
    def __init__(self, title, data, label):
        """Constructor of a cartography result. Just initialize the title, the data and
the label attributes.

        """
        self.title = title
        self.data = data
        self.label = label

    def get_str(self):
        """:return: a printable string, the format of the data depends on its own string representation.

        """
        ret = self.title + "\n"
        ret += str(self.data)
        return ret

    def __str__(self):
        """:return: a printable string, the format of the data depends on its own string representation.

        """
        return self.get_str()

    def get_html_str(self):
        """This function does nothing, it exists for compatibility. Need to find a way to represent a matrix in HTML.

        """
        print("Error: CartoResult.get_html_str() is not implemented")

    def get_latex_str(self):
        """This function does nothing, it exists for compatibility. Need to find a way to represent a matrix in Latex.

        """
        print("Error: CartoResult.get_latex_str() is not implemented")

    def get_dict(self):
        """:return: a dictionary representing the result.

        """
        ret = {
            "title": self.title,
            "data": self.data,
            "label": self.label
        }
        return ret

    def get_JSON_dict(self):
        """:return: a JSON compliant dictionary representing the result.

        """
        ret = {
            "title": self.title,
            "data": [numpy_to_native_list(d) for d in self.data],
            "label": self.label
        }
        return ret

class Results():

    """Class for storing and managing the results of an experiment.

    """
    def __init__(self, results, id_name):
        """Constructor of the class.

        :param results: a list of dictionaries representing the results. The method will create the corresponding Result objects.
        :param id_name: a unique string which identify the set of results.

        """
        self.results = []
        self.id_name = id_name
        for result_dict in results:
            if "label" in result_dict:
                self.results.append(CartoResult(**result_dict))
            else:
                self.results.append(Result(**result_dict))
        self.nb_results = len(self.results)

    def save(self, filename):
        """Save the results as a JSON compliant dictionary containing the id_name and a list of JSON compliant dictionaries representing the results.

        :param filename: the name of the file to save the results in.

        """
        to_save = {
            "id_name": self.id_name,
            "results": [result.get_JSON_dict() for result in self.results]
        }
        fp = open(filename, "w")
        json.dump(to_save, fp)
        fp.close()

    def __str__(self):
        """:return: A printable string of all the results.

        """
        return self.get_str()

    def get_str(self):
        """:return: A printable string of all the results.

        """
        ret = "Results from {}\n".format(self.id_name)
        for res in self.results:
            ret += "{}\n".format(res)
        return ret

    def get_html_str(self):
        """:return: A HTML string of all the results.

        """
        ret = "<h1>Results from {}</h1>\n".format(self.id_name)
        for res in self.results:
            ret += res.get_html_str() + "\n"
        return ret

    def get_results(self):
        """:return: the results as a list of Result objects."""
        return self.results

    def set_results(self, results):
        """Set the results attribute from the given ones.

        :param results: a list of dictionaries representing the results to set.

        """
        for result_dict in results:
            self.results.append(Result(**result_dict))
        self.nb_results = len(self.results)

    def add_result(self, title, data, labels):
        """Add a result to the results list.

        :param title: the title of the result.
        :param data: the data of the result.
        :param labels: the labels of the results.

        """
        self.results.append(Result(title, data, labels))
        self.nb_results += 1

    def get_result_from_title(self, result_title):
        """:param result_title: the title of the result to get.

        :return: a Result object corresponding to the result with the corresponding title, None if there is no result with this title.

        """
        for res in self.results:
            if res.title == result_title:
                return res

    def get_result(self, index):
        """:param index: the index of the result to get.

        :return: the result as a Result object at the given index, None if the index is out of range of the results list.

        """
        if index < self.nb_results:
            return self.results[index]

    def get_result_index(self, result_title):
        """:param result: the title string of the result to get the index.

        :return: the index of the result which match the given title.

        """
        for i in range(self.nb_results):
            if self.results[i].title == result_title:
                return i

    def get_results_titles(self):
        """:return: a list containing the titles of the results in the list.

        """
        ret = []
        for res in self.results:
            ret.append(res.title)
        return ret

    def get_results_titles_str(self):
        """:return: a string representing the titles of the results in the list with their corresponding index in the list.

        """
        titles = self.get_results_titles()
        ret = ""
        for i, title in enumerate(titles):
            ret += "[{}] {}\n".format(i, title)
        return ret
