NB_REGISTERS = 10

OBS_NAMES = ["r{}".format(i) for i in range(NB_REGISTERS)]
DEFAULT_VALUES = [((1 << (31 - i)) + (1 << i)) for i in range(NB_REGISTERS)]
OBS_NAMES.append("main_faulted")
DEFAULT_VALUES.append(0)

params = {
    "obs_names": OBS_NAMES,
    "default_values": DEFAULT_VALUES,
    "to_test": [True for i in range(NB_REGISTERS+1)],
    "power_name": "injector_P",
    "delay_name": "injector_D",
    "done_name": "plan_done",
    "fault_name": "fault",
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ";",
    "data_format": "0x{:08x}",
    "nb_bits": 32,
    "executed_instructions": [],
    "coordinates": ["plan_ygrid", "plan_xgrid"],
    "stage_coordinates": ["stage_y", "stage_x"]
}

