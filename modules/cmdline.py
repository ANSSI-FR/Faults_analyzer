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


def format_title(txt):
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
            ret_str += "[{}] {}\n".format(i, manip)
        return ret_str

    def format_results_list_titles(self, manip_index):
        ret_str = ""
        results_list = self.core.get_results_list()
        if manip_index < len(results_list):
            results = results_list[manip_index]
            ret_str = format_title(results.id_name + " results")
            for i, result in enumerate(results):
                ret_str += "[{}] {}\n".format(i, result.title)
        else:
            print("Error: list index out of range")
        return ret_str

    def do_print(self, inp):
        """Split the arguments from a print command line and realize the print of data.

        :param str inp: the spaced separated arguments.

        """
        inp = inp.rstrip().split(" ")
        to_print = ""
        if (len(inp) == 1) and (inp[0] == ""):
            to_print = self.format_manips(self.core.get_manips())
        elif (len(inp) == 1):
            if intable(inp[0]):
                manip_index = int(inp[0])
                to_print = self.format_results_list_titles(manip_index)
            else:
                print("Error: bad argument expecting an integer to use as index")
        print(to_print)
