def are_all(data, value):
    for d in data:
        if d != value:
            return False
    return True

def safe_numpy_to_native(num):
    """Safely convert a numpy object to a native Python object.

    :param num: the numpy object to convert.

    :returns: the native Python object corresponding to the numpy object.

    """
    try:
        return num.item()
    except:
        return num

def numpy_to_native_list(np_list):
    """Safely convert a list of numpy objects to a list of native Python objects.

    :param list np_list: the list of numpy objects.

    :returns: a list of native Python objects corresponding to the numpy objects.

    """
    ret = []
    for val in np_list:
        ret.append(safe_numpy_to_native(val))
    return ret

def in_range(table, index):
    """Check if the index is in the range of the table.

    :param list table: the list to test.
    :param int index: the index to test.

    :returns: True if the index is in range of the table, False in the other case. Negative indexes return False.

    """
    if index > len(table):
        print("Error: index out of range")
        return False
    if index < 0:
        print("Error: negative index")
        return False
    return True

def intable(int_str, base=10):
    """Safely check if a string is convertible to int.

    :param str int_str: the string to convert into int.

    :returns: True if the string is convertible, False if not.

    """
    try:
        int(int_str, base)
        return True
    except:
        return False

def str2index_convertible(index_str):
    """Check if a string is convertible to a list of integers.

    :param str index_str: the string to convert into a list of integers.

    :returns: True if the string is convertible, False in the other case.

    """
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
        if int(index_str[0]) > int(index_str[1]):
            return False
    else:
        if not intable(index_str):
            return False
    return True

def str_to_index_list(index_str):
    """Check if the string is convertible into a list of integers.

    >>> str_to_index_list("2")
    [2]
    >>> str_to_index_list("2-5")
    [2,3,4,5]
    >>> str_to_index_list("2,5")
    [2,5]

    :param str index_str: the string to convert into a list of integers.

    :returns: the list of integers if possible, None in the other case.

    """
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
    """Vertically print a list.

    :param list l: the list to print.

    """
    for elem in l:
        print(elem)

def print_progress_bar(iteration,
                       total,
                       prefix="",
                       suffix="",
                       decimals=1,
                       length=100,
                       fill=u"\u25A0"):
    """Print a progress bar.

    :param int iteration: the number of iteration of the task, drive the completed part of the progress bar.
    :param int total: the total number of iteration to do, when iteration == total, the progress bar is full.
    :param str prefix: a text to add at the left of the progress bar.
    :param str suffix: a text to add at the right of the progress bar.
    :param int decimals: the number of decimals for the print of the percentage of completion.
    :param int length: the length in number of characters of the progress bar.
    :param str fill: the character to use for filling the progress bar.

    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    if iteration == total:
        print()

def norm_percent(raw):
    """Normalize a list in a percentage format. If the sum of all the elements in the list is 0, returns a list of the size of the input full of 0.

    >>> norm_percent([2,5,3])
    [20.0,50.0,30.0]
    >>> norm_percent([0,0,0])
    [0,0,0]
    >>> norm_percent([2,3,-5])
    [0,0,0]

    :param list raw: the list to normalize in percentage.

    :returns: the percentage equivalent of the input list.

    """
    if sum(raw) != 0:
        return [float(i)/sum(raw)*100 for i in raw]
    else:
        return [0 for i in raw]

def format_table(table, format_str):
    """Format a list of strings with a specific format. Recursively apply on lists within lists.

    :param list table: the list of string to format.
    :param str format_str: the format to use for the strings.

    :returns: the formatted list.

    """
    ret = []
    for t in table:
        if type(t) is list:
            ret.append(format_table(t, format_str))
        else:
            ret.append(format_str.format(t))
    return ret
