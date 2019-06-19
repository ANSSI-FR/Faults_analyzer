import parser.operation as ope
import pandas as pd

class manage_manip:

    """
    Return the panda object of the manip
    """
    def init_panda(self):
        data_ok = False
        while not data_ok:
            try:
                f = pd.read_csv(self.master_file, error_bad_lines=False)
                data_ok = True
            except pd.errors.EmptyDataError:
                data_ok = False
        return f

    """
    Return the size of the cartography if this data exists
    """
    def get_size(self):
        return (int(self.panda["plan_xgrid"].max()+1), int(self.panda["plan_ygrid"].max()+1))

    """
    Return the number of repetition of the cartography if this data exists
    """
    def get_repeat(self):
        return self.panda["plan.repeat"].max()

    """
    Return the dictionary containing all the parameters of the cartography
    """
    def get_params(self):
        print("Error : not implemented anymore")
        return -1

    """
    Create a tab of operation (from ope.py) class elements
    """
    def init_results(self):
        results = []
        self.panda = self.init_panda()
        keys = self.panda.columns
        values = self.panda.get_values()
        for v in values:
            result = ope.operation(v, keys)
            results.append(result)
        return results

    """
    Initialize the class manip_manager() with all it's parameters:
    You must pass the directory which store the results of the manip
    """
    def __init__(self, manip_dir):
        self.master_file = manip_dir + "main.csv"
        self.panda = self.init_panda()
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
            if ope.get("plan.done") == False:
                return ope
        return self.results[-1]

    """
    Return the current repetition phase
    """
    def get_current_repeat(self):
        return self.get_current_ope().get("plan.repeat")

    """
    Return the number of manipulations
    """
    def get_nb_ope(self):
        return len(self.results)
