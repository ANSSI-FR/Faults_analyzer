from prettytable import PrettyTable

def get_common_label_from_labels(labels):
    split_labels = []
    ret = ""
    for label in labels:
        split_labels.append(label.split(" "))
    for word in split_labels[0]:
        in_all = True
        for split_label in split_labels:
            if not word in split_label:
                in_all = False
        if in_all:
            for i, label in enumerate(labels):
                labels[i] = label.replace(word, "")
            ret += word + " "
    return ret

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
