from cmd import Cmd

def pretty_dict_print(d, indent=0):
    print("\t" * indent + "{")
    for key, value in d.items():
        print('\t' * indent + "  " + str(key) + " => ", end="")
        if isinstance(value, dict):
            pretty_dict_print(value, indent+1)
        else:
            print(str(value))
    print("\t" * indent + "}")

def intable(v):
    try:
        int(v)
        return True
    except:
        return False

def floatable(v):
    try:
        float(v)
        return True
    except:
        return False

def listable(s):
    if (s[0] == "[") and (s[-1] == "]"):
        return True
    else:
        return False

def convert_str(s):
    if intable(s):
        return int(s)
    if floatable(s):
        return float(s)
    if listable(s):
        s = s[1:-1].split(",")
        return [e.replace("\,",",") for e in s]

class DictEditor(Cmd):
    prompt = "de> "
    intro = "Welcome in the Dictionnary Editor ! Type ? to list commands"
    exit_msg = "Exiting Dictionnary Editor..."

    def __init__(self, d):
        super().__init__()
        self.d = d

    def do_exit(self, inp):
        print(self.exit_msg)
        return True

    def do_print(self, inp):
        pretty_dict_print(self.d)

    def do_remove(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) != 1:
            print("Error: no key given.")
        else:
            if inp[0] in self.d:
                del self.d[inp[0]]
            else:
                print("Error: key not in dictionary.")

    def do_add(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) != 2:
            print("Error: missing key or value.")
        else:
            val = convert_str(inp[1])
            self.d.update({inp[0]: val})

    def do_typeof(self, inp):
        inp = inp.rstrip().split(" ")
        if len(inp) != 1:
            print("Error: no key given.")
        else:
            print(type(self.d[inp[0]]))

if __name__ == "__main__":
    d = {
        "test": 1,
        "tf": "fgfg",
        "foo": 2,
        "d": {
            "f": 54,
            "ff": "lo"
        }
    }
    de = DictEditor(d)
    de.cmdloop()
