import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import parser.manage_manip as mm

#access to unallocated memory page
KERNEL_PAGING_REQUEST_ERROR = "Unable to handle kernel paging request at virtual address"

#NULL pointer dereferencing
KERNEL_NULL_POINTER_ERROR = "Unable to handle kernel NULL pointer dereference at virtual address"

#unsupported instruction
UNDEFINED_INSTRUCTION_HANDLER_BAD_MODE = "Bad mode in undefined instruction handler detected"

#bad address in the STL Library
DATA_ABORT_HANDLER_BAD_MODE = "Bad mode in data abort handler detected"

UNEXPECTED_IRQ_TRAP_ERROR = "unexpected IRQ trap at vector"
UNHANDLED_PREFETCH_ABORT_ERROR = "Unhandled prefetch abort: page domain fault"
ALIGNMENT_TRAP_ERROR = "Alignment trap: not handling instruction"
SEGMENTATION_FAULT = "Segmentation fault"

"""Arguments parser"""
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("manip_dir", help="directory which stores the results of the manip")
    parser.add_argument("--no-reboot", help="if the flag is set, only non rebooting effects will appear on the cartography", action="store_true")
    return parser.parse_args()

def build_matrix(manip, no_reboot):
    matrix = np.zeros(manip.get_size())
    nb_effects = 0
    nb_effects_without_reboot = 0
    nb_paging_request_error = 0
    nb_null_pointer_error = 0
    nb_internal_oops_error = 0
    nb_undefined_instruction_handler_bad_mode = 0
    nb_data_abort_handler_bad_mode = 0
    nb_unexpected_irq_trap_error = 0
    nb_unhandled_prefetch_abort_error = 0
    nb_alignment_trap_error = 0
    nb_segmentation_fault = 0

    for ope in manip:
        if ope.is_broken() == 0:
            if ope.get("plan.done") == "True":
                log = ope.get("log")
                if log.find("i=50 j=50 cnt=2500") == -1:
                    nb_effects += 1

                    if log.find("reboot") == -1:
                        nb_effects_without_reboot += 1

                    if log.find("reboot") != -1 and no_reboot:
                        pass
                    else:
                        x_grid = int(ope.get("x_grid"))
                        y_grid = int(ope.get("y_grid"))
                        matrix[y_grid, x_grid] += 1

                        if log.find(KERNEL_PAGING_REQUEST_ERROR) != -1:
                            nb_paging_request_error += 1

                        if log.find(KERNEL_NULL_POINTER_ERROR) != -1:
                            nb_null_pointer_error += 1

                        if log.find(UNDEFINED_INSTRUCTION_HANDLER_BAD_MODE) != -1:
                            nb_undefined_instruction_handler_bad_mode += 1

                        if log.find(DATA_ABORT_HANDLER_BAD_MODE) != -1:
                            nb_data_abort_handler_bad_mode += 1

                        if log.find(UNEXPECTED_IRQ_TRAP_ERROR) != -1:
                            nb_unexpected_irq_trap_error += 1

                        if log.find(UNHANDLED_PREFETCH_ABORT_ERROR) != -1:
                            nb_unhandled_prefetch_abort_error += 1

                        if log.find(ALIGNMENT_TRAP_ERROR) != -1:
                            nb_alignment_trap_error += 1

                        if log.find(SEGMENTATION_FAULT) != -1:
                            nb_segmentation_fault += 1

                        print(ope)

    ret = {"matrix": matrix,
           "nb_effects": nb_effects,
           "nb_effects_without_reboot": nb_effects_without_reboot,
           "nb_paging_request_error": nb_paging_request_error,
           "nb_null_pointer_error": nb_null_pointer_error,
           "nb_data_abort_handler_bad_mode": nb_data_abort_handler_bad_mode,
           "nb_unexpected_irq_trap_error": nb_unexpected_irq_trap_error,
           "nb_unhandled_prefetch_abort_error": nb_unhandled_prefetch_abort_error,
           "nb_alignment_trap_error": nb_alignment_trap_error,
           "nb_segmentation_fault": nb_segmentation_fault,
           "nb_undefined_instruction_handler_bad_mode": nb_undefined_instruction_handler_bad_mode}

    return ret

def plot_matrix(matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #colorbar
    bounds = np.linspace(int(matrix.min()), int(matrix.max()), int(matrix.max()-matrix.min()+1))
    cmap = plt.cm.jet
    norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5, matrix.max()+1+0.5, 1), cmap.N)
    cax = ax.matshow(matrix, cmap=cmap, norm=norm)
    fig.colorbar(cax, ticks=bounds)
    plt.show()

args = get_args()
manip_dir = args.manip_dir
if manip_dir[-1] != "/":
    manip_dir += "/"

manip = mm.manage_manip(manip_dir)
res = build_matrix(manip, args.no_reboot)
print("Nb effects = {}".format(res["nb_effects"]))
print("Nb effects without reboots = {}".format(res["nb_effects_without_reboot"]))
print("Nb paging request error = {}".format(res["nb_paging_request_error"]))
print("Nb null pointer error = {}".format(res["nb_null_pointer_error"]))
print("Nb undefined instruction handler bad mode = {}".format(res["nb_undefined_instruction_handler_bad_mode"]))
print("Nb data abort handler bad mode = {}".format(res["nb_data_abort_handler_bad_mode"]))
print("Nb unexpected IRQ trap error = {}".format(res["nb_unexpected_irq_trap_error"]))
print("Nb unhandled prefetch abort error = {}".format(res["nb_unhandled_prefetch_abort_error"]))
print("Nb alignment trap error = {}".format(res["nb_alignment_trap_error"]))
print("Nb segmentation fault = {}".format(res["nb_segmentation_fault"]))
print("Nb unhandled prefetch abort error = {}".format(res["nb_unhandled_prefetch_abort_error"]))
plot_matrix(res["matrix"])
