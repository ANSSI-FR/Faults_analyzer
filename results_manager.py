import json

from results import Results

class ResultsManager():
    def __init__(self, results_list=[], result_dir="."):
        super().__init__()
        self.results_list = results_list
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
