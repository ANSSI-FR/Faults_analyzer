from cmd import Cmd
from .manips_manager import ManipsManager
from .utils import str_to_index_list, intable
from .analyzer import Analyzer
from .results import Results, merge_results
from .results_manager import ResultsManager
from .carto_analyzer import CartoAnalyzer
from .plot_manager import PlotManager
from .aes_printer import AESPrinter
from .aes_analyzer import AESAnalyzer
from .dict_editor import DictEditor

def check_nb_args(cmd, maxi=None, mini=1):
    """Check if the number of arguments from a list.

    :param list cmd: the list of arguments to check.
    :param int maxi: the maximum number of arguments, can be None if there is no maximum.
    :param int mini: the minimum number of arguments.

    :returns: True if the length of the cmd list is in the bounds, False in the other case.

    """
    if len(cmd) < mini:
        print("Error: wrong number of arguments")
        return False
    if maxi != None:
        if len(cmd) > maxi:
            print("Error: wrong number of arguments")
            return False
    return True

class Prompt(Cmd):

    prompt = "fa> "
    """The string that is printed at the head of the command line."""
    intro = "Welcome! Type ? to list commands"
    """The introduction message printed when the interface is started."""
    exit_msg = "I hope to see you soon !"
    """The exit message printed when the interface is closed."""

    def __init__(self, manips):
        """The constructor of the class. Initialize the ManipsManager and ResultsManager.

        :param list manips: A list of Manip object.

        """
        super().__init__()
        self.mm = ManipsManager(manips)
        """The ManipsManager used for managing the manips."""
        self.rm = ResultsManager()
        """The ResultsManager used for managing the results."""
        self.analyze_flags = []
        """The flags for the analyze() function."""
        self.pm = PlotManager(None)
        """The PlotManager used for managing the plots."""

    def get_manip_results(self, manip_index):
        """Get the Results of a Manip if it has been analyzed.

        :param int manip_index: the index of the Manip to get the results.

        :returns: the Results of the Manip it has been analyzed, None in the other case.

        """
        if self.mm.manips[manip_index].analyzed:
            id_name = self.mm.manips[manip_index].id_name
            return self.rm.get_results_from_id_name(id_name)

    def get_manip_results_index(self, manip_index):
        """Get the index of the Results of a Manip if it has been analyzed.

        :param int manip_index: the index of the Manip to get the results.

        :returns: the index of the Results of the Manip it has been analyzed, None in the other case.

        """
        if self.mm.manips[manip_index].analyzed:
            id_name = self.mm.manips[manip_index].id_name
            return self.rm.get_results_index_from_id_name(id_name)

    def default(self, inp):
        """Called by default if a command is not implemented. Used for implementing shortcuts.

        :param str inp: the command line to evaluate.

        :returns: the usual return of the implemented commands functions.

        """
        inp_split = inp.split(" ")
        cmd = inp_split[0]
        args = inp_split[1:]
        if cmd == "a":
            return self.analyze(args)
        elif cmd == "e":
            return self.do_exit(args)
        elif cmd == "p":
            return self.print_data(args)
        elif cmd == "r":
            return self.remove(args)
        elif cmd == "s":
            return self.select(args)
        elif cmd == "m":
            return self.merge(args)
        else:
            super().default(inp)

    def get_results_from_manips_index_list(self, index_list):
        """Get the Results for different Manips.

        :param list index_list: the list of the Manip index to get the Results.

        :returns: the list of the Results of the given Manips.

        """
        results_list = []
        for manip_index in index_list:
            results_index = self.get_manip_results_index(manip_index)
            results_list.append(self.rm.results_list[results_index])
        return results_list

    def merge(self, args):
        """Parse the arguments from a command line and realize the merge between several Results. The merged Results will be add in the ResultsManager and a dedicated analyzed Manip will be add in the ManipsManager.

        :param list args: the arguments to use for the merge.

        """
        if check_nb_args(args, maxi=4, mini=4):
            manips_index_list = str_to_index_list(args[0])
            results_list = self.get_results_from_manips_index_list(manips_index_list)
            result_to_merge = int(args[1])
            columns_to_merge = str_to_index_list(args[2])
            columns_in_common = str_to_index_list(args[3])
            merged_result = merge_results(results_list, result_to_merge,
                                          columns_to_merge, columns_in_common)
            if not self.mm.exist("Merged results"): # First merge
                merged_results = Results([merged_result], "Merged results")
                self.rm.add_results(merged_results)
                self.mm.add_manip("",{},"Merged results")
                self.mm.get_manip_from_id_name("Merged results").analyzed = True
            else:
                self.rm.get_results_from_id_name("Merged results").add_result(**merged_result)

    def do_merge(self, inp):
        """Receive the arguments from the merge command line and realize the merge.

        :param str inp: the command line arguments.

        """
        inp = inp.rstrip().split(" ")
        self.merge(inp)

    def plot_result(self, results_index, result_index, style_name,
                    data_to_plot_index_list=None, data_labels_index=None):
        """Get the Result to plot, initialize the PlotManager for this Result and plot it.

        :param int results_index: the index of the Results storing the Result to plot.
        :param int result_index: the index of the Result to plot.
        :param str style_name: the name of the style to plot the result with.
        :param str data_to_plot_index_list: the index of the data from the result to plot.
        :param str data_labels_index: the index of the data to use as labels for the plot.

        """
        result = self.rm.results_list[results_index].get_result(result_index)
        self.pm.result = result
        self.pm.plot(style_name, data_to_plot_index_list, data_labels_index)

    def plot(self, args):
        """Check the number of arguments and plot the data.

        :param list args: the arguments to use for plotting the data.

        """
        if check_nb_args(args, maxi=5, mini=3):
            manip_index = int(args[0])
            results_index = self.get_manip_results_index(manip_index)
            result_index = int(args[1])
            style_name = args[2]
            if len(args) == 5:
                data_to_plot_index_list = str_to_index_list(args[3])
                data_labels = int(args[4])
                self.plot_result(results_index, result_index, style_name,
                                    data_to_plot_index_list, data_labels)
            elif len(args) == 4:
                print("Error: data labels index is missing")
            else:
                self.plot_result(results_index, result_index, style_name)

    def do_plot(self, inp):
        """Split the arguments of a plot command line and realize the plot.

        :param str inp: the arguments to use for the plot.

        """
        inp = inp.rstrip().split(" ")
        self.plot(inp)

    def save(self, args):
        """Check the number of arguments and save the Results.

        :param list args: the space separated arguments to use for saving the Results.

        """
        if check_nb_args(args, maxi=2, mini=2):
            manip_index = int(args[0])
            filename = args[1]
            results_index = self.get_manip_results_index(manip_index)
            self.rm.save(results_index, filename)

    def do_save(self, inp):
        """Split the arguments of a save command line and realize the plot.

        :param str inp: the space separated arguments to use.

        """
        inp = inp.rstrip().split(" ")
        self.save(inp)

    def load(self, args):
        """Check the number of arguments and load Results from a file. Set the corresponding Manip as analyzed. Only one argument, the file name to load the Results from.

        :param list args: the arguments to use for the load.

        """
        if check_nb_args(args, maxi=1, mini=1):
            filename = args[0]
            self.rm.load(filename)
            id_name = self.rm.results_list[-1].id_name
            manip = self.mm.get_manip_from_id_name(id_name)
            if manip != None:
                manip.analyzed = True
            else:
                #Create new manip for storing the loaded result
                self.mm.add_manip(None, None, id_name)
                self.mm.get_manip_from_id_name(id_name).analyzed = True

    def do_load(self, inp):
        """Split the arguments from a load command line and load the corresponding Results.

        :param str inp: the space separated arguments.

        """
        inp = inp.rstrip().split(" ")
        self.load(inp)

    def check_flags_analyze(self, args):
        if "-f" in args:
            self.analyze_flags.append("-f")
            args.remove("-f")
        return args

    def clean_flags_analyze(self):
        self.analyze_flags = []

    def analyze(self, args):
        """Realize the analysis of the selected Manip. If a index is given, select the corresponding Manip and analyze them.

        :param list args: the arguments to consider for the analysis.

        """
        args = self.check_flags_analyze(args)
        if check_nb_args(args, maxi=1, mini=0):
            if len(args) == 0:
                manips_to_analyze = self.mm.selected_manips
                for manip in manips_to_analyze:
                    if (not manip.analyzed) or ("-f" in self.analyze_flags):
                        params = manip.get_params()
                        if manip.carto:
                            anal = CartoAnalyzer(progress=True, **params)
                        elif manip.aes:
                            anal = AESAnalyzer(progress=True, **params)
                        else:
                            anal = Analyzer(progress=True, **params)
                        results = Results(anal.get_results(), manip.id_name)
                        self.rm.add_results(results)
                        manip.analyzed = True
                        self.clean_flags_analyze()
                    else:
                        print("Error: manip {} already analyzed\nUse -f to force new analysis.".format(manip.id_name))
            else:
                self.mm.remove_all_manips()
                self.select(args)
                self.analyze([])

    def do_analyze(self, inp):
        """Split the arguments from a analyze command line and realize the analysis.

        :param str inp: the space separated index of the Manip to analyze.

        """
        inp = inp.rstrip().split(" ")
        self.analyze(inp)

    def do_exit(self, inp):
        """Exit the interface after printing the exit message.

        :param str inp: an unused argument string, implemented only for compatibility purpose with Cmd.

        :returns: True

        """
        print(self.exit_msg)
        return True

    def check_arg_and_get_result_titles(self, manip_index):
        """Check if the given index is an int. If so get the titles of the Results of the corresponding Manip.

        :param str manip_index: the integer compliant index of the Manip.

        :returns: the titles of the Results of the Manip. None if the Manip index is not integer compliant.

        """
        if intable(manip_index):
            manip_index = int(manip_index)
            return self.get_result_titles(manip_index)
        else:
            print("Error: wrong argument")

    def get_result_titles(self, manip_index):
        """Get the titles of the Results of the Manip.

        :param int manip_index: the index of the Manip to get the Result titles from.

        """
        results_index = self.get_manip_results_index(manip_index)
        if results_index == None:
            print("Error: analysis not done")
            return
        return self.rm.get_result_titles(results_index)

    def check_args_and_get_result(self, manip_index, result_index_list, style="prettytable"):
        """Check if the Manip index is an int. If so get the Results of the Manip.

        :param str manip_index: the index of the Manip.
        :param str result_index_list: the index of the Result to get.

        """
        if intable(manip_index):
            manip_index = int(manip_index)
            results_index = self.get_manip_results_index(manip_index)
            if results_index == None:
                print("Error: analysis not done")
                return
            if result_index_list in ["a", "all"]:
                return self.rm.get_all_result_str(results_index)
            else:
                result_index_list = str_to_index_list(result_index_list)
                if not result_index_list == None:
                    if style=="prettytable":
                        return self.rm.get_result_str(results_index, result_index_list)
                    if style=="var":
                        return self.rm.get_result_var_str(results_index, result_index_list)

    def get_to_print(self, args):
        """Get the string to print from arguments.

        :param list args: the arguments for the print.

        :returns: the string to print, it can be the Manips, the titles of the Results of a Manip of specifics Results of a Manip.

        """
        if len(args) == 0:
            return self.mm.get_manips_str()
        elif len(args) == 1:
            return self.check_arg_and_get_result_titles(args[0])
        elif len(args) == 2:
            return self.check_args_and_get_result(args[0], args[1])
        elif len(args) == 3:
            return self.check_args_and_get_result(args[0], args[1], args[2])
        else:
            return "Error: wrong number of arguments"

    def print_data(self, args):
        """Print the data corresponding to the arguments.

        :param list args: the arguments for the print.

        """
        to_print = self.get_to_print(args)
        if to_print != None:
            print(to_print)

    def do_print(self, inp):
        """Split the arguments from a print command line and realize the print of data.

        :param str inp: the spaced separated arguments.

        """
        if len(inp) > 0:
            inp = inp.rstrip().split(" ")
        self.print_data(inp)

    def select(self, args):
        """Check the number of arguments and set the Manips as selected for analysis.

        :param list args: the arguments, "a" for all or a list of index.

        """
        if check_nb_args(args, maxi=1, mini=1):
            if args[0] in ["a", "all"]:
                self.mm.select_all_manips()
            else:
                index_list = str_to_index_list(args[0])
                if not index_list == None:
                    self.mm.select_manips(index_list)

    def do_select(self, inp):
        """Split the arguments from a select command line and do the selection.

        :param str inp: the space separated arguments.

        """
        inp = inp.rstrip().split(" ")
        self.select(inp)

    def remove(self, args):
        """Check the number of arguments and remove a Manip from the selected ones.

        :param list args: the arguments, "a" for all or a list of index.

        """
        if check_nb_args(args, maxi=1, mini=1):
            if args[0] in ["a", "all"]:
                self.mm.remove_all_manips()
            else:
                index_list = str_to_index_list(args[0])
                if not index_list == None:
                    self.mm.remove_manips(index_list)

    def do_remove(self, inp):
        """Split the arguments from a remove command line and realize the removal.

        :param str inp: the space separated arguments.

        """
        inp = inp.rstrip().split(" ")
        self.remove(inp)

    def edit(self, args):
        if check_nb_args(args, maxi=1, mini=1):
            if args[0] == "tmp_plot_style":
                de = DictEditor(self.pm.tmp_style)
                de.intro = "Editing the temporary style plot dictionary. Type ? to list commands"
                de.exit_msg = "Temporary style plot dictionary edition over."
                de.cmdloop()
            else:
                print("Error: unknown parameter to edit.")

    def do_edit(self, inp):
        """Split the arguments from an edit command and start the editing of parameters.

        :param str inp: the space separated arguments.

        """
        inp = inp.rstrip().split(" ")
        self.edit(inp)

    def do_aes(self, inp):
        """Split the arguments from an aes command and realize the AES printing.

        :param str inp: the space separated arguments.

        """
        inp = inp.rstrip().split(" ")
        self.aes_analysis(inp)

    def aes_analysis(self, args):
        """Print the faulted value in an AES state way to simplify the analysis in this case.

        :param list args: the arguments to consider for the AES analysis.

        """
        manip_index = int(args[0])
        results = self.get_manip_results(manip_index)
        faulted_values_result = results.get_result_from_title("Faulted values statistics")
        faulted_values = [int(fv, 16) for fv in faulted_values_result.data[0]]
        expected_value_result = results.get_result_from_title("Observed statistics")
        expected_value = int(expected_value_result.data[1][0], 16)
        ap = AESPrinter(faulted_values, expected_value)
        if len(args) > 1:
            if args[1] in ["p", "print"]:
                for i, fv in enumerate(faulted_values):
                    print("[{}] 0x{:016x}".format(i, fv))
            elif args[1] in ["h", "hex"]:
                if len(args) > 2:
                    index_list = str_to_index_list(args[2])
                    ap.print_list_hex_diff(index_list)
                else:
                    ap.print_all_hex_diff()
            elif args[1] in ["m", "matrix"]:
                if len(args) > 2:
                    index_list = str_to_index_list(args[2])
                    ap.print_list_mat_diff(index_list)
                else:
                    ap.print_all_mat_diff()
            elif args[1] in ["d", "diag", "diagonal"]:
                if len(args) > 2:
                    nb_faulted_diag = int(args[2])
                    faulted_values = ap.print_diag_faulted_values(nb_faulted_diag)
                else:
                    print("Missing arguments: number of faulted diagonals.")
            elif args[1] in ["dd", "diag_diff", "diagonal_difference"]:
                if len(args) > 2:
                    nb_faulted_diag = int(args[2])
                    faulted_values = ap.print_diag_faulted_values_diff(nb_faulted_diag)
