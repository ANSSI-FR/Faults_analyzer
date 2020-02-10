import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def on_manip_list_selection_changed(selection):
    model, treeiter = selection.get_selected_rows()
    if treeiter != None:
        for tree in treeiter:
            print(model[tree][0])

# Create the list store
store = Gtk.ListStore(str, bool)
store.append(["Manip1", True])
store.append(["Manip2", False])
store.append(["Manip3", False])
store.append(["Manip4", False])
store.append(["Manip5", False])

# Create the view for rendering the list
tree = Gtk.TreeView(model=store)
manip_rendered = Gtk.CellRendererText()
analyzed_rendered = Gtk.CellRendererText()
column = Gtk.TreeViewColumn("Manip", manip_rendered, text=0)
tree.append_column(column)
column = Gtk.TreeViewColumn("Analyzed", manip_rendered, text=1)
tree.append_column(column)

# Add on selection
select = tree.get_selection()
select.set_mode(Gtk.SelectionMode.MULTIPLE)
select.connect("changed", on_manip_list_selection_changed)

# Test on window
win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
win.add(tree)
win.show_all()
Gtk.main()
