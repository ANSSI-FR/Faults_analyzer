MAX_SHIFT = 8

def get_or_with_other_obs_right_shift_check_func(shift):
    def is_or_with_other_obs_right_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv >> shift) | default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_or_with_other_obs_right_shift

def get_other_obs_right_shift_check_func(shift):
    def is_other_obs_right_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs) and ((dv >> shift) == fault.faulted_value):
                return i
    return is_other_obs_right_shift

def get_and_with_other_obs_right_shift_check_func(shift):
    def is_and_with_other_obs_right_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv >> shift) & default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_and_with_other_obs_right_shift

def get_xor_with_other_obs_right_shift_check_func(shift):
    def is_xor_with_other_obs_right_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv >> shift) ^ default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_xor_with_other_obs_right_shift

def get_or_with_other_obs_left_shift_check_func(shift):
    def is_or_with_other_obs_left_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv << shift) | default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_or_with_other_obs_left_shift

def get_other_obs_left_shift_check_func(shift):
    def is_other_obs_left_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs) and ((dv << shift) == fault.faulted_value):
                return i
    return is_other_obs_left_shift

def get_and_with_other_obs_left_shift_check_func(shift):
    def is_and_with_other_obs_left_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv << shift) & default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_and_with_other_obs_left_shift

def get_xor_with_other_obs_left_shift_check_func(shift):
    def is_xor_with_other_obs_left_shift(fault, default_values, nb_bits):
        for i, dv in enumerate(default_values):
            if (i != fault.faulted_obs):
                if((dv << shift) ^ default_values[fault.faulted_obs] == fault.faulted_value):
                    return i
    return is_xor_with_other_obs_left_shift

instr_fault_model_shift = [
    {
        "name": "Or with other observed right shift {}".format(i),
        "test": get_or_with_other_obs_right_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "Other observed right shift {}".format(i),
        "test": get_other_obs_right_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "And with other observed right shift {}".format(i),
        "test": get_and_with_other_obs_right_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "Xor with other observed right shift {}".format(i),
        "test": get_xor_with_other_obs_right_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "Or with other observed left shift {}".format(i),
        "test": get_or_with_other_obs_left_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "Other observed left shift {}".format(i),
        "test": get_other_obs_left_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "And with other observed left shift {}".format(i),
        "test": get_and_with_other_obs_left_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
] + [
    {
        "name": "Xor with other observed left shift {}".format(i),
        "test": get_xor_with_other_obs_left_shift_check_func(i)
    } for i in range(1,MAX_SHIFT+1)
]