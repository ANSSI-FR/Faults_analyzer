NB_REGISTERS = 10

DEFAULT_VALUES = [0xc3d0c220,
                  0x72b8ccd6,
                  0xf25f29b9,
                  0x22c7271d,
                  0xd3f8f3b1,
                  0x3ba81d04,
                  0x7c22b133,
                  0xcc302f01,
                  0xafa42878,
                  0xdd4c70ca]

params = {
    "obs_names": ["r{}".format(i) for i in range(NB_REGISTERS)],
    "default_values": DEFAULT_VALUES,
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
}
