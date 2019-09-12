from prettytable import PrettyTable

class Result():

    title = ""
    data = ""
    labels = ""

    def __init__(self, title, data, labels):
        self.title = title
        self.data = data
        self.labels = labels
        self.table = self.create_prettytable()

    def create_prettytable(self):
        t = PrettyTable()
        for i, col in enumerate(self.data):
            if len(col) > 0:
                t.add_column(self.labels[i], col)
        return t

    def get_str(self):
        return "{}\n{}".format(self.title, self.table.get_string())

    def __str__(self):
        return self.get_str()

    def get_html_str(self):
        return "<h2>{}</h2>\n{}".format(self.title, self.table.get_html_string())

    def get_latex_str(self):
        ret = "{}\n\\caption".format(self.table.get_latex_string())
        ret += "{" + self.title + "}"
        return ret
