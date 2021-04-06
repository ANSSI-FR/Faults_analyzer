import os

from labmanager.manager import SimplePlan

from kernel import Kernel

# Will be used for the output directory
NAME = "MinimalExperiment"

# Allows the manip class to copy the current file (i.e. the parameters) to the
# result folder
FILE = os.path.abspath(__file__)

# Parameters for the experiment
# Kernel and Plan are mandatory
KERNEL = Kernel()
PLAN = SimplePlan(5)

# Drivers for bench equipment
DRIVERS = []

# Utility tools to add
TOOLS = []
