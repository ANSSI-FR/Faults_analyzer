class CmdInterface():

    welcome_msg = "Welcome !"
    exit_msg = "Hope you come back soon !"
    help_msg = """Commands:
    d, done : leave the interface and proceed

    e, exit : exit the program

    h, help : print this help

    """

    def __init__(self):
        self.done = False

    def eval_cmd(self, cmd):
        if cmd in ["d", "done"]:
            self.done = True
        elif cmd in ["e", "exit"]:
            print(self.exit_msg)
            exit(0)
        elif cmd in ["h", "help"]:
            print(self.help_msg)

    def start_interface(self):
        print(self.welcome_msg)
        print(self.help_msg)
        while not self.done:
            cmd = input("> ")
            if len(cmd) > 0:
                self.eval_cmd(cmd)

