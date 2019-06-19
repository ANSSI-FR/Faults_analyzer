import pandas as pd

NB_REGISTERS = 10

RESULT_FILE = "/media/nas/projects/Fault_attacks/EM/Raspi3/raspi3_manip_liblsc_NEW/liblsc/results/rasp_altmovallreg_20190611_1631/main.csv"

PARAMS = {
    "dataframe": pd.read_csv(RESULT_FILE, error_bad_lines=False),
    "obs_names": ["r{}".format(i) for i in range(NB_REGISTERS)],
    "default_values": [((1 << (31 - i)) + (1 << i)) for i in range(NB_REGISTERS)],
    "to_test": [True for i in range(NB_REGISTERS)],
    "power_name": "injector_P",
    "delay_name": "injector_D",
    "done_name": "plan_done",
    "fault_name": "fault",
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ";",
    "data_format": "0x{:08x}",
    "nb_bits": 32
}
