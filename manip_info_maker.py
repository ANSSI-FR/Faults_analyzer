
class ManipInfoMaker():

    def __init__(self, base_dir):
        self.manip_info = {
            "base_dir": base_dir,
            "device": "",
            "manip_name": "",
            "result_name": "",
            "params_file": ""
        }
        self.done = False

    def print_help(self):
        help_str = """Commands:
        s, set <key> <value> : set the key element at the given value

        l, list <key> : list the available keys regarding the manip information

        p, print : print the current manip information

        h, help : display this help

        d, e, q, done, exit, quit : leave this interface
        """
        print(help_str)

    def list_key(self, key):
        dir_to_print = "{}/devices".format(self.manip_info["base_dir"])
        if key == "device":
            pass
        elif key == "manip_name":
            print(self.manip_info["device"])
            dir_to_print += "/{}/manips".format(self.manip_info["device"])
        elif key == "result_name":
            dir_to_print += "/{}/manips/{}/results".format(self.manip_info["device"], self.manip_info["manip_name"])
        elif key == "params_file":
            dir_to_print += "/{}/manips/{}".format(self.manip_info["device"], self.manip_info["manip_name"])
        else:
            print("Key {} does not exists".format(key))
            return
        dir_list = os.listdir(dir_to_print)
        print_list(dir_list)

    def print_manip_info(self):
        for info in self.manip_info:
            print("{}: {}".format(info, self.manip_info[info]))

    def update_manip_info(self, key, value):
        if key in self.manip_info:
            self.manip_info.update({key: value})
        else:
            print("Key {} does not exists".format(key))

    def eval_cmd(self, cmd):
        parsed_cmd = cmd.split(" ")
        if parsed_cmd[0] in ["s", "set"]:
            if len(parsed_cmd) != 3:
                print("Error: wrong number of arguments (expected 2, got {})".format(len(parsed_cmd)-1))
                return
            self.update_manip_info(parsed_cmd[1], parsed_cmd[2])
        elif parsed_cmd[0] in ["p", "print"]:
            self.print_manip_info()
        elif parsed_cmd[0] in ["h", "help"]:
            self.print_help()
        elif parsed_cmd[0] in ["d", "e", "q", "done", "exit", "quit"]:
            self.done = True
        elif parsed_cmd[0] in ["l", "list"]:
            if len(parsed_cmd) != 2:
                print("Error: wrong number of arguments (expected 1, got {})".format(len(parsed_cmd)-1))
                return
            self.list_key(parsed_cmd[1])

    def make_manip_info(self):
        print("Welcome in the manip maker !")
        self.print_help()
        while not self.done:
            cmd = input("> ")
            self.eval_cmd(cmd)
        return format_manip_info(self.manip_info)

    def set_manip_info(self, manip_info):
        self.manip_info = manip_info
