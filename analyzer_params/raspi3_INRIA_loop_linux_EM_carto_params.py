NB_REGISTERS = 3
params = {
    "obs_names": ["i", "j", "cnt"],
    "default_values": [50, 50, 2500],
    "to_test": [True for i in range(NB_REGISTERS)],
    "power_name": "injector_P",
    "delay_name": "injector_D",
    "done_name": "plan_done",
    "fault_name": "fault",
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ":",
    "data_format": "0x{:08x}",
    "nb_bits": 32,
    "executed_instructions": [],
    "coordinates": ["plan_ygrid", "plan_xgrid"],
    "stage_coordinates": ["stage_y", "stage_x"]
}

