from importlib import import_module
from prettytable import PrettyTable

def import_params(param_file="params"):
    MODULE_NAME = param_file
    MODULE = import_module(MODULE_NAME)
    PARAMS = MODULE.PARAMS
    return PARAMS

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
    return [float(i)/sum(raw)*100 for i in raw]

def format_table(table, format_str):
    return [format_str.format(i) for i in table]

def print_result(values, results, titles=[]):
    t = PrettyTable(titles)
    for i in range(len(values)):
        line = [values[i]]
        for j in range(len(results)):
            line.append(results[j][i])
        t.add_row(line)
    t.align = "r"
    t.float_format = "3.2"
    print(t)
