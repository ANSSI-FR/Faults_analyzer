import threading

class MyThread(threading.Thread):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args)
