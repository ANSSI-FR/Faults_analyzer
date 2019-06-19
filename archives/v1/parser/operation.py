class operation:
    """
    Initialize the operation elements with values and keys corresponding to values
    The self.values element is a dictionary of the values indexed with the keys

    If the values and keys are not matching in size, the operation will be "broken", this has been done in order to not break the program instantiating operations if there is a formatting error in the file
    """
    def __init__(self, values, keys):
        self.broken = 0
        if len(values) != len(keys):
            print("Error: number of values and number of keys are not matching for entry {}".format(values[0]))
            self.broken = 1
        if not self.broken:
            self.values = {}
            for i in range(len(values)):
                self.values[keys[i]] = values[i]

    """
    String format for the operation
    """
    def __str__(self):
        if self.broken:
            return "broken"
        ret = "{\n"
        for v in self.values:
            ret += "\t{:25s} -> {}\n".format(v, self.values[v])
        ret += "}"
        return ret

    """
    Return the values of the key value if it exists
    TODO: Uniform returned value (ie: sometimes it's "False" string and sometimes it's False boolean value) seems to depend on Python version used or when we read the file ?
    """
    def get(self, key):
        if self.broken:
            return "broken"
        return self.values[key]

    """
    Check if an operation is broken
    This means the given values and keys we're not matching in size at the creation of this operation
    """
    def is_broken(self):
        return self.broken

