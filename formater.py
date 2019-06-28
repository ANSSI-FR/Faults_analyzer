from prettytable import PrettyTable

class Formater():

    def __init__(self, results):
        self.results = results
        self.to_print = [True] * len(self.results)

    def _create_table(self, labels, data):
        t = PrettyTable()
        for i, col in enumerate(data):
            t.add_column(labels[i], col)
        return t

    def toggle_to_print(self, i):
        self.to_print[i] = not self.to_print[i]

    def get_printable_str(self): 
        ret_str = ""
        for i, result in enumerate(self.results):
            if self.to_print[i]:
                title = result.pop("title")
                t = self._create_table(**result)
                ret_str += "\n" + title + "\n"
                ret_str += t.get_string() + "\n"
        return ret_str

    def get_html_str(self):
        ret_str = ""
        for i, result in enumerate(self.results):
            if self.to_print[i]:
                title = result.pop("title")
                t = self._create_table(**result)
                ret_str += "<h2>" + title + "</h2>"
                ret_str += t.get_html_string() + "<br>"
