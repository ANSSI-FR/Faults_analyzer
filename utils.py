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
