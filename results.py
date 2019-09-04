import logging

from result import Result

def merge_results(results_list, result_to_merge, columns_to_merge,
                  columns_in_common):
    merged_labels, merged_data = get_merged_labels_and_data(results_list,
                                                            result_to_merge,
                                                            columns_to_merge,
                                                            columns_in_common)
    merged_result_title = "Merged " + results_list[0].get_result(result_to_merge).title
    return Result(merged_result_title, merged_data, merged_labels)

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
                label = "{} {}".format(results.get_path(),
                                             results.get_result(result_to_merge).labels[column_to_merge])
                data = results.get_result(result_to_merge).data[column_to_merge]
                merged_labels.append(label)
                merged_data.append(data)
    return merged_labels, merged_data

class Results():

    """Class for storing and managing the results of an experiment.

    """

    base_dir = ""
    device = ""
    manip = ""
    result_dir = ""
    results = []
    nb_results = 0

    def __init__(self, base_dir, device, manip, result_dir, results):
        self.base_dir = base_dir
        self.device = device
        self.manip = manip
        self.result_dir = result_dir
        self.results = results
        self.nb_results = len(self.results)

    def get_path(self):
        return "{}:{}:{}".format(self.device, self.manip, self.result_dir)

    def __str__(self):
        return self.get_str()

    def get_str(self):
        ret = "Results from {}\n".format(self.get_path())
        for res in self.results:
            ret += "{}\n".format(res)
        return ret

    def get_html_str(self):
        ret = "<h1>Results from {}\n".format(self.get_path())
        for res in self.results:
            ret += res.get_html_str() + "\n"
        return ret

    def get_results(self):
        return self.results

    def set_results(self, results):
        self.results = results
        self.nb_results = len(self.results)

    def add_result(self, result):
        self.results.append(result)
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

######### TEST ###########
if __name__ == "__main__":
    results_dict = [
        {
            "title": "Test title",
            "data": [["one", "two", "three", "four", "five"], [4,5,6,36,9], [45,8,7,69,5]],
            "labels": ["name", "number of a", "number of b"]
        },
        {
            "title": "Test title 2",
            "data": [["arc", "boat", "camp", "damage", "fire"], [4,5,6,36,9], [45,8,7,69,5]],
            "labels": ["name", "number of accident", "number of death"]
        },
    ]

    results_list = []
    for res in results_dict:
        results_list.append(Result(**res))

    results = Results("test_base_dir", "test_device", "test_manip",
                      "test_result_dir", results_list)
    results_2 = Results("test_base_dir", "test_device", "test_manip_2",
                        "test_result_dir", results_list)
    print(results)
    print(results.get_html_str())
    print(results.get_results_titles_str())

    print(merge_results([results, results_2], 0, [0,1], [0]))
