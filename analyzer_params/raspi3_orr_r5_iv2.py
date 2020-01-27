NB_REGISTERS = 10

DEFAULT_VALUES = [ 0x7ffffffe,
                   0xbffffffd,
                   0xdffffffb,
                   0xeffffff7,
                   0xf7ffffef,
                   0xfbffffdf,
                   0xfdffffbf,
                   0xfeffff7f,
                   0xff7ffeff,
                   0xffbffdff
]

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
