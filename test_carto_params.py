import pandas as pd

NB_REGISTERS = 14

RESULT_FILE = "/media/nas/projects/fault_attacks_test/devices/intel_core_i3/manips/mov_rbxrbx_carto_die_40x40/results/intel_core_i3_mov_rbxrbx_carto_die_40x40_20190624_1229/main.csv"

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
    "nb_bits": 64,
    "executed_instructions": [0x4889db],
    "coordinates": ["plan_ygrid", "plan_xgrid"],
    "stage_coordinates": ["stage_y", "stage_x"]
}
