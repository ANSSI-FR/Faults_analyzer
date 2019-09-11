def safe_numpy_to_native(num):
    try:
        return num.item()
    except:
        return num

def numpy_to_native_list(np_list):
    ret = []
    for val in np_list:
        ret.append(safe_numpy_to_native(val))
    return ret

def in_range(table, index):
    if index > len(table):
        print("Error: index out of range")
        return False
    if index < 0:
        print("Error: negative index")
        return False
    return True

def intable(int_str):
    try:
        int(int_str)
        return True
    except:
        return False

def str2index_convertible(index_str):
    if "," in index_str:
        index_str = index_str.split(",")
        for i in index_str:
            if not intable(i):
                return False
    elif "-" in index_str:
        index_str = index_str.split("-")
        if len(index_str) != 2:
            return False
        if (not intable(index_str[0])) or not (intable(index_str[1])):
            return False
        if index_str[0] > index_str[1]:
            return False
    else:
        if not intable(index_str):
            return False
    return True

def str_to_index_list(index_str):
    if str2index_convertible(index_str):
        index_list = []
        if "," in index_str:
            index_str = index_str.split(",")
            for index in index_str:
                index_list.append(int(index))
        elif "-" in index_str:
            index_str = index_str.split("-")
            if len(index_str) == 2:
                start = int(index_str[0])
                end = int(index_str[1])
                for index in range(start, end+1):
                    index_list.append(int(index))
        else:
            index_list = [int(index_str)]
        return index_list
    else:
        print("Error: wrong index list formatting")
        return None

def print_list(l):
    for elem in l:
        print(elem)

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
