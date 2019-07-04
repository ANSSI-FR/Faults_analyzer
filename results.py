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
                    to_append = "{} - {}".format(label, results.get_exp().split("/")[-2])
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
        ret += "{}, ".format(results.get_exp().split("/")[-2])
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

    def __init__(self, exp):
        self.exp = exp
        self.results = []

    def get_exp(self):
        return self.exp

    def get_results(self):
        return self.results

    def set_results(self, results):
        self.results = results

    def add_result(self, result):
        self.results.append(result)

    def get_result(self, result):
        for res in self.results:
            if res["title"] == result:
                return res
