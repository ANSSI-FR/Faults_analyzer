import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .manip_list import ManipList
from .results import ResultsDisplayer

class Gtk3FaultAnalyzer(Gtk.Window):
    def __init__(self, core):
        super().__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(200,200)
        self.core = core

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.manip_list = self.init_manip_list()
        self.box.pack_start(self.manip_list, True, True, 0)

        self.results_displayers = []
        self.btn = None

    def init_manip_list(self):
        manips = [[manip.id_name, manip.analyzed] for manip in self.core.get_manips()]
        ml = ManipList(manips)
        ml.on_manip_selection_changed_hooks.append((self.on_manip_list_selection_changed, {}))
        return ml

    def remove_results_displayers(self):
        for rd in self.results_displayers:
            self.box.remove(rd)

    def remove_analyze_btn(self):
        if self.btn != None:
            self.box.remove(self.btn)
            self.btn = None

    def analyze_manips(self, widget):
        self.core.analyze_manips(self.manip_list.selected_manips)
        self.box.remove(self.manip_list)
        self.manip_list = self.init_manip_list()
        self.box.pack_start(self.manip_list, True, True, 0)
        self.update_results_displayers()
        self.show_all()

    def on_manip_list_selection_changed(self):
        self.update_results_displayers()

    def update_results_displayers(self):
        self.remove_results_displayers()
        self.remove_analyze_btn()
        for manip in self.manip_list.selected_manips:
            res = self.core.get_results_from_manip(manip)
            if res != None:
                rd = ResultsDisplayer(res.id_name, res.results)
                self.results_displayers.append(rd)
                self.box.pack_start(rd, True, True, 0)
            else:
                if self.btn == None:
                    self.btn = Gtk.Button(label="Analyze manip")
                    self.btn.connect("clicked", self.analyze_manips)
                    self.box.pack_start(self.btn, True, True, 0)
        self.show_all()

    def start_interface(self):
        self.show_all()
        Gtk.main()
