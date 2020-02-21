import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

NB_ROWS_MAX = 50
NB_COLS_MAX = 50

def get_result_table(res):
    data = res.data

    if len(res.data) > NB_COLS_MAX:
        data = res.data[:NB_COLS_MAX]
    for i, data_set in enumerate(data):
        if len(data_set) > NB_ROWS_MAX:
            data[i] = data_set[:NB_ROWS_MAX]

    nb_cols = len(data)
    nb_rows = len(data[0])

    table = Gtk.Table(n_columns=nb_cols, n_rows=nb_rows, homogeneous=True)
    table.set_border_width(3)

    for i,label in enumerate(res.labels):
        lab = Gtk.Label(label=label)
        lab.set_markup("<b>" + label + "</b>")
        lab.set_hexpand(True)
        table.attach(lab, left_attach=i, right_attach=i+1, top_attach=0, bottom_attach=1)

    for i,d_list in enumerate(data):
        for j,d in enumerate(d_list):
            lab = Gtk.Label(label=d)
            table.attach(lab, left_attach=i, right_attach=i+1, top_attach=j+1, bottom_attach=j+2)

    return table

class ResultsDisplayer(Gtk.Grid):
    def __init__(self, title, results):
        super().__init__()
        self.results = results

        self.hb = Gtk.HeaderBar()
        self.hb.props.title = title
        self.hb.set_hexpand(True)
        self.add(self.hb)

        self.res_combo = Gtk.ComboBoxText()
        self.res_combo.connect("changed", self.on_res_combo_changed)
        for res in self.results:
            self.res_combo.append_text(res.title)
        self.attach_next_to(self.res_combo, self.hb, Gtk.PositionType.BOTTOM, 1, 1)
        self.res_combo.set_active(0)

    def on_res_combo_changed(self, combo):
        text = combo.get_active_text()
        if text != None:
            res = self.get_result_from_name(text)
            if res != None:
                table = get_result_table(res)
                self.remove_row(2)
                self.attach_next_to(table, self.res_combo, Gtk.PositionType.BOTTOM, 1, 1)
                table.show_all()

    def get_result_from_name(self, name):
        for res in self.results:
            if res.title == name:
                return res

if __name__ == "__main__":

    grid = None

    class Res():
        def __init__(self, title, data, labels):
            self.title = title
            self.data = data
            self.labels = labels

    results = [
        Res("First result", [["A", "B", "C", "D", "E", "F"],[1,5,4,8,9,6]], ["Names", "Power"]),
        Res("Second result", [["A", "B", "C", "D", "E", "F"],[1,5,4,8,9,6]], ["LETTERS !!", "Power"])
    ]

    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    rd = ResultsDisplayer("Test", results)
    win.add(rd)
    win.show_all()
    Gtk.main()
