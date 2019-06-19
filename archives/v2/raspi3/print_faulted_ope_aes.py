import sys
import pandas as pd
import numpy as np
import argparse

sys.path.append("/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")

from ManipUtils import bin_utils as bu

default_cipher = 0x69c4e0d86a7b0430d8cdb78070b4c55a

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    args = parser.parse_args()
    manip_dir = args.manip_dir + "/"
    return manip_dir

manip_dir = get_args()
res_file = manip_dir + "main.csv"

df = pd.read_csv(res_file, error_bad_lines=False)

nb_faults = 0

for _, ope in df.iterrows():
    if ope["fault"]:
        print(ope)
        print("\n")
        bu.hex_diff(default_cipher, int(ope["cipher"],16))
        print("\n")
        c_tab = bu.int2byte_tab(int(ope["cipher"], 16))
        d_tab = bu.int2byte_tab(default_cipher)
        bu.mat_diff(c_tab, 4, d_tab)
        print("\n\n")
        nb_faults += 1

print("{} faults".format(nb_faults))
