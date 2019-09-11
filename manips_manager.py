from utils import in_range
from manip import Manip

class ManipsManager():
    def __init__(self, manips):
        super().__init__()
        self.manips = manips
        self.selected_manips = []

    def get_manip_from_id_name(self, id_name):
        for manip in self.manips:
            if manip.id_name == id_name:
                return manip

    def get_str(self, manip, index):
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
        self.manips.append(Manip(result_file, analysis_params, id_name))

    def get_manips_str(self):
        to_print = ""
        for i, manip in enumerate(self.manips):
            to_print += self.get_str(manip, i) +"\n"
        return to_print

    def select_manips(self, index_list):
        if in_range(self.manips, max(index_list)):
            for i in index_list:
                if not self.manips[i] in self.selected_manips:
                    self.selected_manips.append(self.manips[i])

    def remove_manips(self, index_list):
        if in_range(self.manips, max(index_list)):
            for i in index_list:
                if self.manips[i] in self.selected_manips:
                    selected_index = self.selected_manips.index(self.manips[i])
                    self.selected_manips.pop(selected_index)

    def get_selected_manips(self):
        return self.selected_manips

    def get_manip_index(self, manip):
        return self.manips.index(manip)

    def select_all_manips(self):
        self.selected_manips = self.manips

    def remove_all_manips(self):
        self.selected_manips = []
