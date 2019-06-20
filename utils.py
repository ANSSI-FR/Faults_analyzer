from importlib import import_module
from prettytable import PrettyTable

def print_progress_bar(iteration,
                       total,
                       prefix="",
                       suffix="",
                       decimals=1,
                       length=100,
                       fill=u"\u25A0"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    if iteration == total:
        print()

def norm_percent(raw):
    if not sum(raw) is 0:
        return [float(i)/sum(raw)*100 for i in raw]
    else:
        return [0 for i in raw]

def format_table(table, format_str):
    ret = []
    for t in table:
        if type(t) is list:
            ret.append(format_table(t, format_str))
        else:
            ret.append(format_str.format(t))
    return ret

def create_table(values, results, titles=[]):
    t = PrettyTable(titles)
    for i in range(len(values)):
        line = [values[i]]
        for j in range(len(results)):
            line.append(results[j][i])
        t.add_row(line)
    t.align = "r"
    t.float_format = "3.2"
    return t

def print_result(values, results, titles=[]):
    t = create_table(values, results, titles)
    print(t)

def add_to_html_file(file_descriptor, values, results, titles=[]):
    t = create_table(values, results, titles)
    file_descriptor.write(t.get_html_string())
