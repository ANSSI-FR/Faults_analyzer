from cmd import Cmd

from .utils import *

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


def format_title(txt, style="str"):
    if style == "html":
        return "<h1>" + txt + "</h1>\n"
    elif style == "latex":
        return "\section{" + txt + "}\n"
    else:
        return "\n " + txt + "\n" + "="*(len(txt)+2) + "\n"

class Cmdline(Cmd):

    prompt = "fa> "
    """The string that is printed at the head of the command line."""
    intro = "Welcome! Type ? to list commands"
    """The introduction message printed when the interface is started."""
    exit_msg = "Closing command line interface."
    """The exit message printed when the interface is closed."""

    def __init__(self, core):
        """The constructor of the class. Initialize the ManipsManager and ResultsManager.

        :param Core core: the core to interface with.

        """
        super().__init__()
        self.core = core
        self.float_format = ".4"
        self.progress = True
        self.force = True

    def do_exit(self, inp):
        """Exit the interface after printing the exit message.

        :param str inp: an unused argument string, implemented only for compatibility purpose with Cmd.

        :returns: True

        """
        print(self.exit_msg)
        return True

    def format_manips(self, manips):
        ret_str = format_title("Manips")
        for i, manip in enumerate(manips):
            if manip.analyzed:
                ret_str += "[{}]* {}\n".format(i, manip)
            else:
                ret_str += "[{}]  {}\n".format(i, manip)
        return ret_str

    def format_results_list_titles(self, manip_index_list):
        ret_str = ""
        manips_list = self.core.get_manips()
        for manip_index in manip_index_list:
            if manip_index < len(manips_list):
                manip = manips_list[manip_index]
                ret_str += format_title("{} available results".format(manip.id_name))
                if manip.analyzed:
                    results = self.core.get_results_from_manip(manip)
                    for i, result in enumerate(results):
                        ret_str += "[{}] {}\n".format(i, result.title)
                else:
                    ret_str += "Manip not analyzed. Type \"analyze {}\" to start the analysis.\n".format(manip_index)
            else:
                print("Error: list index out of range")
        return ret_str

    def format_result_list(self, manip_index_list, result_index_list, style="str"):
        ret_str = ""
        manips_list = self.core.get_manips()
        for manip_index in manip_index_list:
            if manip_index < len(manips_list):
                manip = manips_list[manip_index]
                ret_str += format_title("{} results".format(manip.id_name), style)
                if manip.analyzed:
                    results = self.core.get_results_from_manip(manip)
                    for result_index in result_index_list:
                        if style == "html":
                            ret_str += results[result_index].get_html_str() + "\n"
                        elif style == "latex":
                            ret_str += results[result_index].get_latex_str() + "\n"
                        else:
                            ret_str += str(results[result_index]) + "\n"
                else:
                    ret_str += "Manip not analyzed. Type \"analyze {}\" to start the analysis.\n".format(manip_index)
            else:
                print("Error: list index out of range")
        return ret_str

    def get_to_print(self, inp):
        to_print = ""
        # In the case the argument is empty, we print the available manips
        if (len(inp) == 1) and (inp[0] == ""):
            to_print = self.format_manips(self.core.get_manips())
        # In the case the argument is not empty, we print the available results
        # of the corresponding manips
        elif len(inp) == 1:
            manip_index_list = str_to_index_list(inp[0])
            if manip_index_list != None:
                to_print = self.format_results_list_titles(manip_index_list)
        # In the case there are two arguments, we print the corresponding
        # results and manips
        elif len(inp) == 2:
            manip_index_list = str_to_index_list(inp[0])
            result_index_list = str_to_index_list(inp[1])
            if (manip_index_list != None) and (result_index_list != None):
                to_print = self.format_result_list(manip_index_list, result_index_list)
        # In the case there are three arguments, we do the same as with two
        # arguments but add the style of the printingx
        elif len(inp) == 3:
            manip_index_list = str_to_index_list(inp[0])
            result_index_list = str_to_index_list(inp[1])
            style = inp[2]
            if (manip_index_list != None) and (result_index_list != None):
                to_print = self.format_result_list(manip_index_list,
                                                   result_index_list, style)
        return to_print

    def do_print(self, inp):
        """Split the arguments from a print command line and realize the print of data.

        :param str inp: the spaced separated arguments.

        """
        inp = inp.rstrip().split(" ")
        to_print = self.get_to_print(inp)
        print(to_print)

    def do_analyze(self, inp):
        inp = inp.rstrip().split(" ")
        if (len(inp) == 1) and (inp[0] != ""):
            manips_to_analyze = str_to_index_list(inp[0])
            self.core.analyze_manips(manips_to_analyze, progress=self.progress,
                                     force=self.force)

    def do_merge(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) >= 4:
            manips_to_merge = str_to_index_list(inp[0])
            result_to_merge = int(inp[1])
            columns_to_merge = str_to_index_list(inp[2])
            columns_in_common = str_to_index_list(inp[3])
            if len(inp) == 5:
                name = inp[4]
                self.core.merge(manips_to_merge, result_to_merge,
                                columns_to_merge, columns_in_common, name)
            else:
                self.core.merge(manips_to_merge, result_to_merge,
                                columns_to_merge, columns_in_common)
        else:
            print("Error: missing arguments")

    def do_save(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) == 2:
            if intable(inp[0]):
                results_to_save = int(inp[0])
                filename = inp[1]
                self.core.save(results_to_save, filename)
            else:
                print("Error: wrong argument, expected an integer as first argument")
        else:
            print("Error: missing arguments")

    def do_plot(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) == 3:
            if intable(inp[0]) and intable(inp[1]):
                manip_to_plot = int(inp[0])
                result_to_plot = int(inp[1])
                style_name = inp[2]
                self.core.plot(manip_to_plot, result_to_plot, style_name)
            else:
                print("Error: wrong argument")
                print("Usage: plot [manip index] [result_index] [style_name]")
        elif len(inp) == 5:
            if intable(inp[0]) and intable(inp[1]) and intable(inp[4]):
                manip_to_plot = int(inp[0])
                result_to_plot = int(inp[1])
                style_name = inp[2]
                data_to_plot_index_list = str_to_index_list(inp[3])
                data_labels_index = int(inp[4])
                self.core.plot(manip_to_plot, result_to_plot, style_name,
                               data_to_plot_index_list, data_labels_index)
            else:
                print("Error: wrong argument")
                print("Usage: plot [manip_index] [result_index] [style_name] <data_to_plot_index_list> <data_labels_index>")
        else:
            print("Error: wrong argument")

