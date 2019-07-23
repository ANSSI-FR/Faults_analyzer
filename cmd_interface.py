class CmdInterface():

    welcome_msg = "Welcome !"
    help_msg = """Commands:
    d, e, q, done, exit, quit : leave the interface

    h, help : print this help
    """

    def __init__(self):
        self.done = False

    def eval_cmd(self, cmd):
        if cmd in ["d", "e", "q", "done", "exit", "quit"]:
            self.done = True
        elif cmd in ["h", "help"]:
            print(self.help_msg)

    def start_interface(self):
        print(self.welcome_msg)
        print(self.help_msg)
        while not self.done:
            cmd = input("> ")
            self.eval_cmd(cmd)

