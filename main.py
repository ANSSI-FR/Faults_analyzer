#!/usr/bin/env python3
from modules.core import Core
from modules.cmdline import Cmdline

from config import CONFIG

if __name__ == "__main__":
    c = Core(**CONFIG)
    interface = Cmdline(c)
    interface.cmdloop()
