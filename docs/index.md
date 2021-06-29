---
layout: home
title: Home
nav_order: 0
---

# Fault Analyzer documentation
{: .no_toc}

- TOC
{:toc}

The fault analyzer software aims at providing an interface for analyzing
perturbation experiments.

- **Current maintaner:** Thomas Trouchkine ([thomas.trouchkine@ssi.gouv.fr](mailto:thomas.trouchkine@ssi.gouv.fr))

## Requirements
- python (tested with version 3.8.6)

### Python packages
All the needed packages are listed in the `requirements.txt` file and are
automatically install in the `virtualenv` via the `make init` command.
- pandas
- prettytable
- matplotlib
- plotter
- tikzplotlib
- termcolor
- PyGObject

# Quick start
## Setting up the configuration file
The `config.py` stores the pathes where the experiments, their parameters and
their results are stored.

By default the `config.py` file looks like this:
```python
# config.py

CONFIG = {
    "main_dir": "./tests/",
    "results_dir": "results/",
    "manips_dir": "manips/",
    "parameters_dir": "parameters/"
}
```

- `main_dir` is the directory containing the other directories. You may want to
  change it to match your system.
- `results_dir` is the directory where the results of the analysis are stored.
- `manips_dir` is the directory where the manips, _i.e._ the non analyzed results coming from the experiments are stored.
- `parameters_dir` is the directory where the specific to manips parameters
  (such as initial values for instance) are stored.

### Optional parameters
There are some optional parameters available:

- `latex`: a boolean to use for setting the Latex mode for
  plotting figures.
  ```python
  CONFIG = {
      "latex": True
  }
  ```

## The `manips`
The `manips` files are `.csv` files storing the results of each experiments, but
not analyzed.

### Mandatory fields
The minimal parameters to have in a `manips` file are `log` and `reboot`.

### Filename format
The name format of a `manips` file must mathc the following:
`{component}_{target}_{iv}_{anything}.csv` where:

- `{component}` is the name of the component.
- `{target}` is the tageted implementation running on the component.
- `{iv}` is a code that helps in identifying the used initial values.
- `{anything}` can be anything you want.

This nomenclature is a proposed way to manage your experiments. In practice it
is only needed to have, at least, three underscores `_` in the file name as the
analyzer will parse the name of the manip based on them and load the matching
parameters. For instance `bcm2837_aes_iv1_carto.csv` matches the
`bcm2837_aes_iv1.py` parameters file.
{: .info}

### Minimal example
```sh
# test_base_0.csv

,log,reboot
0,FlagBegin;-131071;FlagEnd,False
1,FlagBegin;-131070;FlagEnd,False
```

## The parameters
The parameters file are `.py` files the parameters needed for the analysis in a
`params` variable. This `params` variable is a dictionnary containing the
parameters for analyzing the experiments.

The mandatory parameters are:
- `obs_names`: a list containing the names of the observed. The order given in
  this list must match the order of the `log` field in the `manip` file.
- `default_values`: a list containing the expected values of the observed.
- `to_test`: a list containing booleans. If the boolean at index `i` is set to
  `True` then the observed at the same index will be taken into account during
  the analysis, otherwise it will be ignored.
- `reboot_name`: the name of the field in the `manip` file storing the
  information if there was a reboot or not during the experiment.
- `log_name`: the name of the field in the `manip` file storing the log of the
  experiment.
- `log_separator`: the sequence used for separing the different fields of the
  log.
- `nb_bits`: the number of bits the observed values are on.
- `log_flag_begin`: the sequence at the index `0` in the log.
- `log_flag_end`: the sequence at the last index in the log.

### Optional parameters
There are some parameters that are not mandatory but may be useful regarding the
situation.

- `result_base`: this parameter is an `int` describing the base in which the
  result values are stored in the manip `.csv` file. By default it is set to
  `10` but it is possible to set it to `16` in the case the values are stored in
  hexadecimal.

### Minimal example
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
}
```

## Starting the analyzer
The analyzer can be started by simply running the following command:
```sh
make run
```

and the following interface should appear:
```sh
Welcome! Type ? to list commands
fa> 
```

From this point, you can use [the available commands]({{site.baseurl}}/cmds/) to
manipulate your experiments.

For instance, you can display the available manips using the `print` command:
```sh
fa> print

 Manips
========
[0]  test_base_0
```

Then you can analyze a manip using the `analyze` command and the index of the
manip you want to analyze:
```sh
fa> analyze 0
Analyzing test_base_0
Loading Analyzer
Analysis progress: |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100.0% Complete
```

When the analysis is over you can see an asteriks next to the analyzed manip
when using the `print` command.

You can display the available results of the analysis of a manip using the
`print` command and the index of the manip you want to see the results:
```sh
fa> print 0

 test_base_0 available results
===============================
[0] Faults general information
[1] Observed statistics
[2] Faulted values statistics
[3] Fault model statistics
[4] Unknown fault model values
```

Finally, you can display the results using the `print` command and both the
index of the manip and the index of the result you want to see:
```sh
fa> print 0 0

 test_base_0 results
=====================
Faults general information
+----------------------------------------------+---------+
|                 Information                  |  Values |
+----------------------------------------------+---------+
|               Number of faults               |    1    |
|            Fault probability (%)             | 50.0000 |
| Average number of faulted observed per fault |  1.0000 |
+----------------------------------------------+---------+
```
