NB_REGISTERS = 10
params = {
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
    "nb_bits": 32,
    "executed_instructions": [],
    "coordinates": ["plan_ygrid", "plan_xgrid"],
    "stage_coordinates": ["stage_y", "stage_x"]
}

