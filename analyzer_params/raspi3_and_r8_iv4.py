NB_REGISTERS = 10

DEFAULT_VALUES = [0xfffe0001,
                  0xfffd0002,
                  0xfffb0004,
                  0xfff70008,
                  0xffef0010,
                  0xffdf0020,
                  0xffbf0040,
                  0xff7f0080,
                  0xfeff0100,
                  0xfdff0200]

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
