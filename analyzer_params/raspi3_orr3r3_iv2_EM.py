NB_REGISTERS = 10

DEFAULT_VALUES = [0x80000001,
                  0xc0000003,
                  0xe0000007,
                  0xf000000f,
                  0x08000010,
                  0x0c000030,
                  0x0e000070,
                  0x0f0000f0,
                  0x00800100,
                  0x00c00300]

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
