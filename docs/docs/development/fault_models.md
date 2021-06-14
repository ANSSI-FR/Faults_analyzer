---
layout: home
title: Fault models
permalink: /dev/fault_models/
nav_order: 0
parent: Development
---

# Adding a new fault model
{: .no_toc}

- TOC
{:toc}

## File location
The fault models are defined in the `modules/analyzer/fault_models.py` file.

## Inheritance
Currently, there are two fault models classes `InstructionFaultModel` and `DataFaultModel` which both inherit from the `FaultModel` class.

```python
class FaultModel():
    def __init__(self, name, faulted_obs):
        self.name = name
        self.faulted_obs = faulted_obs
```

```python
class InstructionFaultModel(FaultModel):
    def __init__(self, name, faulted_obs, origin):
        super().__init__(name, faulted_obs)
        self.origin = origin
```

```python
class DataFaultModel(FaultModel):
    def __init__(self, name, faulted_obs):
        super().__init__(name, faulted_obs)
```

Every fault model has two attributes:
- `name`: the name of the fault model.
- `faulted_obs`: the index of the faulted observed.

The `InstructionFaultModel` has a special attribute:
- `origin`: the index(es) of the fault origin. For instance, when the observed
  faulted value is the logical `OR` between the faulted register and another
  register, it is the index of the second register. In the case the faulted
  value is computed from different registers, it can be the list of the involved
  registers (`(1,2)` for instance).

## Create a new fault model
To create a new fault model you must define two things:
- the name of the fault model.
- the test function of this fault model.

Both must be set either in the `data_fault_models` or in the
`instruction_fault_models` variables in the
`modules/analyzer/fault_models.py` file.

For instance:
```python
data_fault_models = [
    {
        "name": "Bit reset",
        "test": is_bit_reset
    },
    {
        "name": "Bit set",
        "test": is_bit_set
    }
]
```

```python
instr_fault_models = [
    {
        "name": "Other observed value",
        "test": is_other_obs_fault_model
    },
    {
        "name": "Other observed complementary value",
        "test": is_other_obs_comp_fault_model
    }
]
```

### Develop a test function
The test function must have the following prototype:
```python
def my_test_function(fault, default_values, nb_bits):
    # the core of the function
    return val
```

- the `fault` parameter is a `Fault` class defined in
  `modules/analyzer/fault.py` and has the following definition:
  ```python
  class Fault():
    def __init__(self, faulted_obs, faulted_value):
        self.faulted_obs = faulted_obs
        self.faulted_value = faulted_value
  ```
  It stores the index of the faulted observed in `faulted_obs` and the faulted
  value in `faulted_value`.
  
#### Arguments
- the `default_values` parameter is the list of the observed default values
  defined in the parameter file of the experiments.
- the `nb_bits` parameter is the number of bits to consider the values on as
  defined in the parameter file of the experiments.
  
#### Returned value
The test function either return a boolean in the case of a `DataFaultModel`
flagging if the faulted value matches the tested fault model, or it returns the
origin(s) of the faulted value when it could be determined. In the case there
are multiple origins, the returned value can be a tuple.

#### Examples
You can see examples in the `modules/analyzer/fault_models.py` file.