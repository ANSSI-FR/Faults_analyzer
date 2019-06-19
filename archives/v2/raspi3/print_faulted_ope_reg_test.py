import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os, sys, inspect

sys.path.insert(0,"/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")
sys.path.insert(0,"/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc_analyzer")

import parser.manage_manip as mm
import manip_utils.bin_utils as bu

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    return parser.parse_args()

args = get_args()
manip_dir = args.manip_dir
if manip_dir[-1] != "/":
    manip_dir += "/"

manip = mm.manage_manip(manip_dir)
nb_fault=0
nb_reboot=0
values = {"r0": [],
          "r1": [],
          "r5": [],
          "r6": [],
          "r7": [],
          "r8": [],
          "r9": [],
}

default_a = {"r0": 0x55,
             "r1": 0x55+1,
             "r5": 0x55+5,
             "r6": 0x55+6,
             "r7": 0x55+7,
             "r8": 0x55+8,
             "r9": 0x55+9,
}

default_b = {"r0": 0x55555555,
             "r1": 0x55555555+4122,
             "r5": 0x55555555+4122*5,
             "r6": 0x55555555+4122*6,
             "r7": 0x55555555+4122*7,
             "r8": 0x55555555+4122*8,
             "r9": 0x55555555+4122*9,
}

default_c = {"r0": 0xaaaaaaaa,
             "r1": 0xaaaaaaaa+4122,
             "r5": 0xaaaaaaaa+4122*5,
             "r6": 0xaaaaaaaa+4122*6,
             "r7": 0xaaaaaaaa+4122*7,
             "r8": 0xaaaaaaaa+4122*8,
             "r9": 0xaaaaaaaa+4122*9,
}

default_values = {"r{}".format(i): (1<<(31-i))+(1<<i) for i in range(10)}
default_values["r3"] = 255
default_values["r9"] = 85
#default_values["r5"] = default_values["r8"]
#default_values["r0"] += 100
#default_values["r1"] = 1
#default_values = {"r{}".format(i): (1<<(31-i))+(1<<i) if i != 0 else 1020 for i in range(10)}
#default_values = {"r{}".format(i): 2497 if i==3 else 2496 if i==9 else ((1<<(31-i))+(1<<i)) for i in range(10)}

for ope in manip:
    if ope.get("plan_done") == True:
        if ope.get("reboot") == True:
            nb_reboot+=1
        for i in range(10):
            reg = "r{}".format(i)
            if bu.to_unsigned(ope.get(reg),32) != default_values[reg] and not np.isnan(ope.get(reg)):
                print("\n\nFault on {}".format(reg))
                print(ope)
                nb_fault+=1
                faulted_val = bu.to_unsigned(int(ope.get(reg)),32)
                print("Default value : 0x{:08x} ({}) ({:032b})".format(default_values[reg],default_values[reg],default_values[reg]))
                print("Faulted value : 0x{:08x} ({}) ({:032b})".format(faulted_val,faulted_val,faulted_val))
                bu.bin_diff(default_values[reg], int(ope.get(reg)), 32)

print("Nb faults = {}".format(nb_fault))
print("Nb reboots = {}".format(nb_reboot))
print("Nb operations = {}".format(manip.get_nb_ope()))
print("Fault probability = {}%".format(nb_fault/float(manip.get_nb_ope())))
