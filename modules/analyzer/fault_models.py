from ..bin_utils import a2_comp

from .instr_fault_models_shift import instr_fault_model_shift

class FaultModel():
    def __init__(self, name, faulted_obs):
        self.name = name
        self.faulted_obs = faulted_obs

class InstructionFaultModel(FaultModel):
    def __init__(self, name, faulted_obs, origin):
        super().__init__(name, faulted_obs)
        self.origin = origin

class DataFaultModel(FaultModel):
    def __init__(self, name, faulted_obs):
        super().__init__(name, faulted_obs)

def is_other_obs_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs) and (dv == fault.faulted_value):
            return i

def is_other_obs_comp_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs) and (a2_comp(dv, nb_bits) == fault.faulted_value):
            return i

def is_or_with_other_obs_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs):
            if(dv | default_values[fault.faulted_obs] == fault.faulted_value):
                return i

def is_and_with_other_obs_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs):
            if(dv & default_values[fault.faulted_obs] == fault.faulted_value):
                return i

def is_xor_with_other_obs_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs):
            if(dv ^ default_values[fault.faulted_obs] == fault.faulted_value):
                return i

def fixed_size_add(v1, v2, nb_bits):
    return (v1 + v2) & ((2**nb_bits)-1)

def is_add_with_other_obs_fault_model(fault, default_values, nb_bits):
    for i, dv in enumerate(default_values):
        if (i != fault.faulted_obs):
            if( fixed_size_add(dv, default_values[fault.faulted_obs], nb_bits) == fault.faulted_value):
                return i

def is_or_between_two_other_obs_fault_model(fault, default_values, nb_bits):
    for i1, dv1 in enumerate(default_values):
        if (i1 != fault.faulted_obs):
            for i2, dv2 in enumerate(default_values):
                if (i2 != fault.faulted_obs):
                    if fault.faulted_value == dv1 | dv2:
                        return (i1, i2)

def is_bit_reset(fault, default_values, nb_bits):
    if fault.faulted_value == 0:
        return True
    return False

def is_bit_set(fault, default_values, nb_bits):
    if fault.faulted_value == (2**nb_bits)-1:
        return True
    return False

def is_bit_flip(fault, default_values, nb_bits):
    if fault.faulted_value == default_values[fault.faulted_obs] ^ (2**nb_bits)-1:
        return True
    return False

data_fault_models = [
    {
        "name": "Bit reset",
        "test": is_bit_reset
    },
    {
        "name": "Bit set",
        "test": is_bit_set
    },
    {
        "name": "Bit flip",
        "test": is_bit_flip
    }
]

instr_fault_models = [
    {
        "name": "Other observed value",
        "test": is_other_obs_fault_model
    },
    {
        "name": "Other observed complementary value",
        "test": is_other_obs_comp_fault_model
    },
    {
        "name": "And with other observed",
        "test": is_and_with_other_obs_fault_model
    },
    {
        "name": "Or with other observed",
        "test": is_or_with_other_obs_fault_model
    },
    {
        "name": "Xor with other observed",
        "test": is_xor_with_other_obs_fault_model
    },
    {
        "name": "Add with other observed",
        "test": is_add_with_other_obs_fault_model
    },
    {
        "name": "Or between two other observed",
        "test": is_or_between_two_other_obs_fault_model
    }
]

# We add the instruction fault models with shift in the instruction fault models
instr_fault_models += instr_fault_model_shift

fault_models = data_fault_models + instr_fault_models

def get_fault_model(fault, default_values, nb_bits):
    for data_fault_model in data_fault_models:
        if data_fault_model["test"](fault, default_values, nb_bits):
            return DataFaultModel(data_fault_model["name"], fault.faulted_obs)
    for instr_fault_model in instr_fault_models:
        origin = instr_fault_model["test"](fault, default_values, nb_bits)
        if origin != None:
            return InstructionFaultModel(instr_fault_model["name"], fault.faulted_obs, origin)
