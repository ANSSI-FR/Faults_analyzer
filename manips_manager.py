from manip import ManipInfoMaker

class ManipsManager():

    manips = []

    def __init__(self, base_dir, manips=[]):
        self.manips = manips
        self.base_dir = base_dir
        self.done = False

    def add_manip(self):
        mim = ManipInfoMaker(self.base_dir)
        manip = mim.make_manip_info()
        self.manips.append(manip)

    def print_manips(self):
        for i, manip in enumerate(self.manips):
            to_print = "[{}]\n{}".format(i, manip)
            print(to_print)

    def remove_manip(self, manip):
        self.manips.pop(manip)

    def print_help(self):
        help_str = """Commands:
        a, add : add a new manip via the manip maker

        r, remove <index> : remove the corresponding manip

        p, print : print the manips

        d, e, q, done, exit, quit : leave the interface

        h, help : print this help
        """
        print(help_str)

    def eval_cmd(self, cmd):
        parsed_cmd = cmd.split(" ")
        if parsed_cmd[0] in ["a", "add"]:
            self.add_manip()
        elif parsed_cmd[0] in ["r", "remove"]:
            if len(parsed_cmd) != 2:
                print("Error: wrong number of arguments (expected 2, got {})".format(len(parsed_cmd)-1))
            self.remove_manip(parsed_cmd[1])
        elif parsed_cmd[0] in ["p", "print"]:
            self.print_manips()
        elif parsed_cmd[0] in ["d", "e", "q", "done", "exit", "quit"]:
            self.done = True
        elif parsed_cmd[0] in ["h", "help"]:
            self.print_help()

    def manage_manips(self):
        print("Welcome in the manip manager !")
        self.print_help()
        while not self.done:
            cmd = input("> ")
            self.eval_cmd(cmd)
