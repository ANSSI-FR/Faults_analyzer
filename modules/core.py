import sys

from pathlib import Path
from os import listdir
from os.path import isfile, join

from .manips_manager import ManipsManager
from .results_manager import ResultsManager
from .manip_info_formater import get_params

def get_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

class Core():
    def __init__(self,
                 main_dir=str(Path.home()) + "/fault_analyzer/",
                 results_dir="results/",
                 manips_dir="manips/",
                 parameters_dir="parameters/"):
        self.results_dir = main_dir + results_dir
        self.manips_dir = main_dir + manips_dir
        self.parameters_dir = main_dir + parameters_dir
        self.directories = [self.results_dir, self.manips_dir, self.parameters_dir]
        self.mm = ManipsManager()
        self.rm = ResultsManager()

    def create_directories(self):
        for directory in self.directories:
            print("Creating " + directory)
            Path(directory).mkdir(parents=True, exist_ok=True)

    def get_results_files(self):
        return get_files(self.results_dir)

    def get_manips_files(self):
        return get_files(self.manips_dir)

    def load_results(self, filename):
        """Load Results from a file. Set the corresponding Manip as analyzed.

        :param str filename: the filename to load the results from.

        """
        self.rm.load(self.results_dir + filename)
        id_name = self.rm.results_list[-1].id_name
        manip = self.mm.get_manip_from_id_name(id_name)
        if manip != None:
            manip.analyzed = True
        else:
            #Create new manip for storing the loaded result
            self.mm.add_manip(None, None, id_name)
            self.mm.get_manip_from_id_name(id_name).analyzed = True

    def get_params_from_manip_file(self, filename):
        s = filename.split("_")
        params_file = s[0] + "_" + s[1] + "_" + s[2] + ".py"
        return get_params(params_file, import_path=self.parameters_dir)

    def load_manip(self, filename):
        id_name = filename.replace(".csv", "")
        if not self.rm.is_in_results(id_name):
            result_file = self.manips_dir + filename
            analysis_params = self.get_params_from_manip_file(filename)
            self.mm.add_manip(result_file, analysis_params, id_name)

if __name__ == "__main__":
    c = Core()
