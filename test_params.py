import pandas as pd

from plotter import PlotterType

NB_REGISTERS = 14

MANIP_DIR = "/media/nas/projects/fault_attacks_test/devices/intel_core_i3/manips/mov_rbxrbx_fix/"

RESULTS_FILES = [
    MANIP_DIR + "results/intel_core_i3_fix_20190701_1640/main.csv",
    MANIP_DIR + "results/intel_core_i3_fix/main.csv",
]

PARAMS = [{
    "dataframe": pd.read_csv(result_file, error_bad_lines=False),
    "obs_names": ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"],
    "default_values": [((1 << (63 - i)) + (1 << i)) for i in range(NB_REGISTERS)],
    "to_test": [False,True,False,False,False,False,True,True,False,False,True,True,True,True],
    "power_name": "injector_P",
    "delay_name": "injector_D",
    "done_name": "plan_done",
    "fault_name": "fault",
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ":",
    "data_format": "0x{:016x}",
    "nb_bits": 64,
    "executed_instructions": [0x4889db]
} for result_file in RESULTS_FILES]

TO_PLOT = [
    [{
        "result_index": 7,
        "plot_type": PlotterType.PIE,
    }],
    []
]

TO_ANALYZE = [{
    "file": RESULTS_FILES[i],
    "params": param,
    "to_plot": TO_PLOT[i]
} for i, param in enumerate(PARAMS)]
