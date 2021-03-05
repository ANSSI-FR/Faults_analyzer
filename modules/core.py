import sys

from pathlib import Path
from os import listdir, getcwd
from os.path import isfile, join
from importlib import import_module
from enum import Enum

from .manips_manager import ManipsManager
from .results_manager import ResultsManager
from .manip_info_formater import get_params
from .manip import Manip
from .results import Results, merge_results
from .plot_manager import PlotManager

from .new_analyzer.analyzer import Analyzer

def get_files(path):
    """Get the files from a given path.

    :param str path: the path to get the files from
    :return: the name of the files in the directory in the path
    :rtype: list

    """
    return [f for f in listdir(path) if isfile(join(path, f))]

class CoreErrors(Enum):
    """Errors that can be returned from Core functions.

    """
    SUCCESS = 0
    MANIP_ALREADY_ANALYZED = 1
    ANALYZE_MANIP_ARG_NOT_LIST = 2
    MANIP_BAD_ARGUMENT = 3
    TO_MERGE_RESULTS_NOT_LIST = 4
    RESULTS_BAD_ARGUMENT = 5

class Core():
    def __init__(self,
                 main_dir=str(Path.home()) + "/fault_analyzer/",
                 results_dir="results/",
                 manips_dir="manips/",
                 parameters_dir="parameters/",
                 plot_style_file="plot_styles.py"):
        sys.path += [main_dir, getcwd()]
        self.results_dir = main_dir + results_dir
        self.manips_dir = main_dir + manips_dir
        self.parameters_dir = main_dir + parameters_dir
        self.directories = [self.results_dir, self.manips_dir, self.parameters_dir]
        self.mm = ManipsManager()
        self.rm = ResultsManager()
        self.styles, self.tmp_style = self.get_plot_styles(plot_style_file)
        self.pm = PlotManager(self.styles, self.tmp_style)
        self.init()

    def get_plot_styles(self, plot_style_file):
            module_name = plot_style_file.replace(".py", "").replace("/", ".")
            module = import_module("plot." + module_name)
            return module.styles, module.tmp_style

    def init(self):
        """Initialize the results and manips. It is important to start with manips,
        otherwise the analysis parameters would not be loaded, which can be
        useful to redo the analysis.

        """
        self.create_directories()
        man_files = self.get_manips_files()
        for f in man_files:
            self.load_manip(f)
        res_files = self.get_results_files()
        for f in res_files:
            self.load_results(f)

    def get_results_list(self):
        return self.rm.results_list

    def get_manips(self):
        return self.mm.manips

    def create_directories(self):
        for directory in self.directories:
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

    def analyze_manips(self, manips, force=False, progress=False):
        """Check that we receive a list and do the analysis for every manip.

        """
        if type(manips) == list:
            for manip in manips:
                self.analyze_manip(manip, force, progress)
        else:
            return CoreErrors.ANALYZE_MANIP_ARG_NOT_LIST

    def analyze_manip(self, manip, force=False, progress=False):
        if type(manip) == str:
            manip = self.mm.get_manip_from_id_name(manip)
        elif type(manip) == int:
            manip = self.mm.manips[manip]
        elif type(manip) == Manip:
            pass
        else:
            return CoreErrors.MANIP_BAD_ARGUMENT
        print("Analyzing {}".format(manip.id_name))
        self.analyze(manip, force, progress)

    def get_analyzer(self, manip, progress=False):
        """Get the adapted analyzer for a specific Manip. Latter on the analyzer will
        be built via the decorator design pattern.

        :param Manip manip: the Manip to analyze

        """
        params = manip.get_params()
        print("Loading Analyzer")
        params.update({"carto": manip.carto})
        analyzer = Analyzer(**params)
        return analyzer

    def analyze(self, manip, force=False, progress=False, save=False):
        """

        :param Boolean force: flag for forcing the analysis
        """
        if (not manip.analyzed) or (force):
            anal = self.get_analyzer(manip, progress)
            results = Results(anal.get_results(), manip.id_name)
            self.rm.update_results(results)
            manip.analyzed = True
            results_index = self.rm.get_results_index(results)
            if save:
                self.save(results_index, results.id_name)
            return CoreErrors.SUCCESS
        else:
            return CoreErrors.MANIP_ALREADY_ANALYZED

    def get_merge_results(self, results):
        if type(results) == str:
            return self.rm.get_results_from_id_name(results)
        elif type(results) == int:
            manip_id_name = self.mm.manips[results].id_name
            return self.rm.get_results_from_id_name(manip_id_name)
        elif type(results) == Results:
            return results
        else:
            return CoreErrors.RESULTS_BAD_ARGUMENT

    def get_results_to_merge(self, results_list):
        results_to_merge = []
        if type(results_list) == list:
            for results in results_list:
                res = self.get_merge_results(results)
                if res != CoreErrors.RESULTS_BAD_ARGUMENT:
                    results_to_merge.append(res)
                else:
                    return CoreErrors.RESULTS_BAD_ARGUMENT
            return results_to_merge
        else:
            return CoreErrors.TO_MERGE_RESULTS_NOT_LIST

    def merge(self, results_list, result_to_merge, columns_to_merge,
              columns_in_common, name="Merged results"):
        results_to_merge = self.get_results_to_merge(results_list)
        #if results_to_merge in CoreErrors:
        #    return results_to_merge

        merged_result = merge_results(results_to_merge, result_to_merge,
                                      columns_to_merge, columns_in_common)
        if not self.mm.exist(name):
            merged_results = Results([merged_result], name)
            self.rm.add_results(merged_results)
            self.mm.add_manip("", {}, name)
            self.mm.get_manip_from_id_name(name).analyzed = True
        else:
            self.rm.get_results_from_id_name(name).add_result(**merged_result)

        return CoreErrors.SUCCESS

    def save(self, results_index, filename, results_indexes=[]):
        if not filename.lower().endswith(".json"):
            filename += ".json"
        results = self.get_results_from_manip(results_index)
        results.save(filename, results_indexes)
        #self.rm.save(results_index, self.results_dir + filename)
        print("Results of {} saved in {}".format(results.id_name, self.results_dir + filename))

    def get_results_to_plot(self, results):
        if type(results) == str:
            return self.rm.get_results_from_id_name(results)
        elif type(results) == int:
            manip_id_name = self.mm.manips[results].id_name
            return self.rm.get_results_from_id_name(manip_id_name)
        elif type(results) == Results:
            return results

    def plot(self, results, result_index_list, style_name,
             data_to_plot_index_list=None, data_labels_index=None):
        #result = self.get_results_to_plot(results).get_result(result_index)
        results = [self.get_results_to_plot(results).get_result(result_index) for result_index in result_index_list]
        #self.pm.result = result
        self.pm.results = results
        self.pm.plot(style_name, data_to_plot_index_list, data_labels_index)

    def export_tikz(self, results, result_index, style_name,
                    data_to_plot_index_list=None, data_labels_index=None, filename="tikz_figure.tex"):
        result = self.get_results_to_plot(results).get_result(result_index)
        self.pm.result = result
        if not filename.lower().endswith(".tex"):
            filename += ".tex"
        self.pm.export_tikz(style_name, data_to_plot_index_list, data_labels_index, filename)

    def get_results_from_manip(self, manip):
        if type(manip) == int:
            return self.rm.get_results_from_id_name(self.mm.manips[manip].id_name)
        elif type(manip) == Manip:
            return self.rm.get_results_from_id_name(manip.id_name)
        elif type(manip) == str:
            return self.rm.get_results_from_id_name(manip)
        else:
            return CoreErrors.MANIP_BAD_ARGUMENT
