import pandas as pd

NB_REGISTERS = 14

RESULT_FILE = "/media/nas/projects/Fault_attacks/EM/Intel_Core_i3/results_good/intel_core_i3_fix/main.csv"

PARAMS = {
    "dataframe": pd.read_csv(RESULT_FILE, error_bad_lines=False),
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
    "nb_bits": 64
}
