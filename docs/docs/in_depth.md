---
layout: home
title: In depth analysis
nav_order: 2
permalink: /depth/
---

# In depth analysis
{: .no_toc}

- TOC
{:toc}

## Modularity of the analyzer
When an experiment is analyzed using the `analyze` command, the analyzer is
built to match the manip to analyze. This is done thanks to the modularity of
the analyzer. 

## Modules
In this section we will go through the various available modules of the analyzer
and when they are loaded.

### Base
This module is the base of the fault analyzer, it is loaded all the time. It
able to have the following information about the manip:
- **The fault general information**: this result contains the number of faults, the
  fault probability and the number of faulted observed per fault.
- **The observed statistics**: this result contains the fault probability for every
  observed with their name, initial values and if they are tested or not.
- **The faulted values statistics**: this result contains the distribution of the
  faulted values and their probability of occurrence.
  
### Fault Models
This module able the analyzer to identify various fault models. It is loaded
when the `type` of every initial values (defined in the parameters file) is an
`int`.

It able to have the following information about the manip:
- **Fault model statistics**: this result contains the distribution of the
  identified fault models and their probability of occurrence.
- **Unknown fault model values**: this result contains all the faulted values
  for which the analyzer could not determine a fault model explaining its
  appearance.
- **{FAULT MODEL} destination occurrence**: this result contains the probability
  for each register to be faulted for every `{FAULT MODEL}`. This is add if the
  corresponding `{FAULT MODEL}` appears at least once.
- **{FAULT MODEL} origin occurrence**: in the case the determined `{FAULT
  MODEL}` involves a known value, and the origin of this value has been
  determined, this result contains the probability for each source to be
  involved in the corresponding `{FAULT MODEL}`. For instance, the probability
  for each register to be the origin of the `XORed` value in the case the
  analyzer determine the fault model is `XOR with other observed`.

#### Adding a new fault model

See [how to add a new fault model]({{site.baseurl}}/dev/fault_models/).

### Carto
This module able to analyze cartography manips and generate matrices from them.
This module is loaded if the sequence `"carto"` is in the name of the manip
file. For instance, `bcm2837_aes_iv1_carto.csv` will automatically load the
carto module.

It able to have the following information about the manip:

#### Specific parameters
To work properly, the carto module requires a new parameter to be set in the
parameters file:
- `coordinates_name`: a list containing the names of the coordinates used in the
  manip file.
  
In some cases, the manip `.csv` file only stores the experiments where a fault
occurs. In this case the carto module cannot parse the matrix dimension from the
manip file. Therefore, to have to correct matrix size, it is possible to add the
dimensions used during the experiment with the `carto_resolution` parameter.

- `carto_resolution`: the resolution used during the experiment for the
  cartography. It is a couple which will be used for defining the size of all
  the matrices set by the carto module.
  
#### Manip and parameters file examples
```sh
# test_base_0_carto.csv

,log,reboot,x,y
0,FlagBegin;-131071;FlagEnd,False,1,3
1,FlagBegin;-131070;FlagEnd,False,2,3
```

```python
# test_base_0.py

params = {
    "log_flag_begin": "FlagBegin",
    "log_flag_end": "FlagEnd",
    "obs_names": ["My register"],
    "default_values": [0xfffe0001],
    "to_test": [True],
    "reboot_name": "reboot",
    "log_name": "log",
    "log_separator": ";",
    "nb_bits": 32,
    "coordinates_name": ["x", "y"]
}
```

The values corresponding to the fields mentioned by the `coordinates_name`
parameters must contain **integers**. These values will be used to build the
matrices.
{: .danger}

It able to have the following information about the manip:
- **Fault matrix**: the matrix giving the number of fault for every position.

### Fault Model Carto
This module is a mix between the carto and the fault model modules. It generate
a matrix of the positions a fault model has been observed for every fault model.
To work properly, the parameter and manip files must match the requirements of
the carto module.

Currently, it is automatically loaded with the carto module. However, due to its
need in memory space, it might be smart to disable it by default.

The auto-saving of results was disabled because this module generated to big
files. 
{: .info}

It able to have the following information about the manip:
- **Unknown fault model matrix**: the matrix giving the number of fault for
  which no fault model has been determined for every position.
- **{FAULT MODEL} matrix**: the matrix giving the number of fault matching the
  `{FAULT MODEL}` fault model for every position.

### Delay
This module able to have information about the manip when a delay parameter is
set during the manip. It able to have the following information:
- **Number of faults per delay**: this results stores the number of fault for
  every tested delays.

#### Specific parameters
The delay module requires specific parameters to work properly:
- `delay_name`: the name of the field containing the delay information for each
  experiment.
  
This way the module will automatically extract the delay from the manip file and
create the list of tested delays. However, in some cases, the manip file does
not store all the tested experiments but only the ones that ended up in a fault.
Therefore, it is possible to gives the module more parameters for it to be able
to know all the tested delays:

- `delay_start`: the first tested delay.
- `delay_end`: the last tested delay.
- `delay_step`: the step used to increment the tested delays.

These parameters are optional, but if they are given, the analyzer will
calculate all the tested delays as the linear space defined by these parameters.

## Adding a new module
See [how to add a new analyzer module]({{site.baseurl}}/dev/analyzer_modules/).
