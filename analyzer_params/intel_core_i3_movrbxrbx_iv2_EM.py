NB_REGISTERS = 14

DEFAULT_VALUES = [((1 << (63 - i)) + (1 << i)) for i in range(NB_REGISTERS)]
DEFAULT_VALUES[1] = 0xa5a5a5a5a5a5a5a5

params = {
    "obs_names": ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"],
    "default_values": DEFAULT_VALUES,
    "to_test": [False,True,False,False,False,False,True,True,True,False,True,True,True,True],
    "power_name": "injector_P",
    "delay_name": "injector_D",
    "done_name": "plan_done",
    "fault_name": "fault",
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ":",
    "data_format": "0x{:016x}",
    "nb_bits": 64,
    "executed_instructions": [0x4809db]
}

