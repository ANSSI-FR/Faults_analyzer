#!/usr/bin/env python3
import argparse

from modules.core import Core
from interfaces.cmdline import Cmdline
from interfaces.gtk3.gtk3_fault_analyzer import Gtk3FaultAnalyzer

from config import CONFIG

if __name__ == "__main__":
    c = Core(**CONFIG)

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Run with graphical interface", action="store_true")
    args = parser.parse_args()

    if args.gui:
        interface = Gtk3FaultAnalyzer(c)
        interface.start_interface()
    else:
        interface = Cmdline(c)
        interface.cmdloop()
