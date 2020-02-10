import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)

lb = Gtk.ListBox()
lbr = Gtk.ListBoxRow()
lb.add(lbr)

win.add(lb)
win.show_all()
Gtk.main()
