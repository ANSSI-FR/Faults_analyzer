from .utils import in_range
from .manip import Manip

class ManipsManager():
    """A class dedicated to the management of several Manip instances.

    """
    def __init__(self, manips=[]):
        """Constructor of the class.

        :param list manips: a list of Manip object to manage.

        """
        super().__init__()
        self.manips = manips
        """The list of the managed manips."""
        self.selected_manips = []
        """A list containing selected manips. Can be used for working on a reduce numbe rof the managed manips."""

    def exist(self, id_name):
        """Check if a manip with the given identification name exists.

        :param str id_name: the identification name of the Manip to check.

        :returns: True if there is a manip with a matching identification name, False in the other case.

        """
        for manip in self.manips:
            if manip.id_name == id_name:
                return True
        return False

    def get_manip_from_id_name(self, id_name):
        """Check if a Manip with the given identification name exists and gives it.

        :param str id_name: the identification name of the Manip to get.

        :returns: a Manip object which is the one matching the given identification name, None if there is no matching manip.

        """
        for manip in self.manips:
            if manip.id_name == id_name:
                return manip
        return None

    def get_str(self, manip, index):
        """Format a string of a Manip, this string gives the identification name of the Manip, its index and its state (Selected, Analyzed or Nothing).

        :param Manip manip: the Manip to string format.
        :param int index: the index of the Manip.

        :returns: a string containing the index, the identification name and the state of the manip.

        """
        format_str = "{:" + str(len(str(len(self.manips)))+3) + "}"
        ret = format_str.format("[{}]".format(index))
        if manip.analyzed:
            ret += "(A)"
        elif manip in self.selected_manips:
            ret += "(S)"
        else:
            ret += "( )"
        ret += " {}".format(manip)
        return ret

    def add_manip(self, result_file, analysis_params, id_name):
        """Create a new Manip object and add it to the manips list.

        :param str result_file: the name of the result file of the manip.
        :param dict analysis_params: the dictionary containing the parameters needed by the Analyzer.
        :param str id_name: the identification name of the manip.

        """
        self.manips.append(Manip(result_file, analysis_params, id_name))

    def get_manips_str(self):
        """:returns: a string containing the index, the state and the identification name of all the manips.

        """
        to_print = ""
        for i, manip in enumerate(self.manips):
            to_print += self.get_str(manip, i) +"\n"
        return to_print

    def select_manips(self, index_list):
        """Add manips into the selected manips list.

        :param list index_list: the list containing the index of the manips to add to the selected manips.

        """
        if in_range(self.manips, max(index_list)):
            for i in index_list:
                if not self.manips[i] in self.selected_manips:
                    self.selected_manips.append(self.manips[i])

    def remove_manips(self, index_list):
        """Remove manips from the selected manips list.

        :param list index_list: the list containing the index, in the manips list, of the manips to remove from the selected manips.

        """
        if in_range(self.manips, max(index_list)):
            for i in index_list:
                if self.manips[i] in self.selected_manips:
                    selected_index = self.selected_manips.index(self.manips[i])
                    self.selected_manips.pop(selected_index)

    def get_manip_index(self, manip):
        """:param Manip manip: the manip to get the index.

        :returns: the index of the manip.

        """
        return self.manips.index(manip)

    def select_all_manips(self):
        """Add all the manips in the selected manips.

        """
        self.selected_manips = self.manips

    def remove_all_manips(self):
        """Clean the selected manips.

        """
        self.selected_manips = []
