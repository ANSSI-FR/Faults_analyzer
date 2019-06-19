import json
import parser.operation as ope
import csv

class manage_manip:

    """
    Initialize the data from the $manip_dir/$params_file file into a dictionnary
    The parameters file must be JSON formated
    """
    def init_params(self):
        path = self.manip_dir + self.params_file
        fd = open(path, "r")
        params = json.load(fd)
        fd.close()
        return params

    """
    Return the size of the cartography if this data exists
    """
    def get_size(self):
        return self.params['carto']['size']

    """
    Return the number of repetition of the cartography if this data exists
    """
    def get_repeat(self):
        return self.params['repeat']

    """
    Return the dictionary containing all the parameters of the cartography
    """
    def get_params(self):
        return self.params

    """
    Set all the data from the $manip_dir/$master_file file into a tab containing every line
    """
    def init_master_data(self):
        path = self.manip_dir + self.master_file
        fd = open(path, "r")
        data = csv.reader(fd)
        #fd.close()
        return list(data)

    """
    Create a tab of operation (from ope.py) class elements from the master_data object
    """
    def init_results(self):
        results = []
        while len(results) < 1:
            master_data = self.init_master_data()
            for i, line in enumerate(master_data):
                if i == 0:
                    keys = line
                else:
                    result = ope.operation(line, keys)
                    if not result.is_broken():
                        results.append(result)
        return results

    """
    Initialize the class manip_manager() with all it's parameters:
    You must pass the directory which store the results of the manip
    """
    def __init__(self, manip_dir):
        self.params_file = "params.json"
        self.master_file = "mastermain.csv"
        self.separator = ","
        self.manip_dir = manip_dir
        self.params = self.init_params()
        self.results = self.init_results()
        self.iterator = 0

    """
    Iterations over a manage_manip class make a loop over every line of results (operation class)
    """
    def __iter__(self):
        return self

    def __next__(self):
            if self.iterator == len(self.results):
                self.iterator = 0
                raise StopIteration
            else:
                try:
                    self.iterator += 1
                    return self.results[self.iterator-1]
                except IndexError:
                    print("self.iterator = {}, len(self.results) = {}".format(self.iterator, len(self.results)))

    """
    Reload the master_data and results elements
    """
    def refresh_results(self):
        self.results = self.init_results()

    """
    Return the last operation undone
    If everything is done, return the last operation
    """
    def get_current_ope(self):
        for ope in self.results:
            if ope.get("plan.done") == "False":
                return ope
        return self.results[-1]

    """
    Return the current repetition phase
    """
    def get_current_repeat(self):
        return self.get_current_ope().get("plan.repeat")
