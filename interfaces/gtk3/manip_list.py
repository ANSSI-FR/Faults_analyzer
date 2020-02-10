import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ManipList(Gtk.ScrolledWindow):
    def __init__(self, manips, DEBUG=False):
        Gtk.ScrolledWindow.__init__(self)
        self.manips = manips
        self.DEBUG = DEBUG
        self.selected_manips = []
        self.list_store = self.init_list_store()
        self.tree_view = self.init_tree_view()
        self.set_vexpand(True)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(self.tree_view)

    def init_list_store(self):
        store = Gtk.ListStore(str, bool)
        for manip in self.manips:
            store.append(manip)
        return store

    def init_tree_view(self):
        tree = Gtk.TreeView(model=self.list_store)
        # Rendered for the name of the manip
        rendered = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Manip", rendered, text=0)
        tree.append_column(column)
        # Rendered for the analysis flag
        rendered = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Analyzed", rendered, text=1)
        tree.append_column(column)
        # Adding on selection function
        select = tree.get_selection()
        select.set_mode(Gtk.SelectionMode.MULTIPLE)
        select.connect("changed", self.on_manip_list_selection_changed)
        return tree

    def on_manip_list_selection_changed(self, selection):
        model, treeiter = selection.get_selected_rows()
        if treeiter != None:
            self.selected_manips = [model[tree][0] for tree in treeiter]
        else:
            self.selected_manips = []
        if self.DEBUG:
            print(self.selected_manips)

if __name__ == "__main__":
    manips = [
        ["Manip1", True],
        ["Manip2", True],
        ["Manip3", False],
        ["Manip4", True],
        ["Manip5", False],
        ["Manip6", False],
        ["Manip7", True],
    ]

    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    win.set_default_size(200,200)

    ml = ManipList(manips, DEBUG=True)

    win.add(ml)
    win.show_all()
    Gtk.main()
