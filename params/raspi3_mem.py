import pandas as pd

NB_REG = 10

RESULT_FILE = "/media/nas/projects/Fault_attacks/EM/Raspi3/raspi3_manip_liblsc_NEW/liblsc/results/rasp_mem_20190618_1641/main.csv"

DEFAULT_VALUES = [0 for i in range(NB_REG)]
DEFAULT_VALUES[8] = 0x020100ff

OBS_NAMES = ["r{}".format(i) for i in range(NB_REG)]

TO_TEST = [False for i in range(NB_REG)]
TO_TEST[8] = True

PARAMS = {
    "dataframe": pd.read_csv(RESULT_FILE, error_bad_lines=False),
    "obs_names": OBS_NAMES,
    "default_values": DEFAULT_VALUES,
    "to_test": TO_TEST,
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
