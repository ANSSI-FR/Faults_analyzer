# Fault Analyzer

## Introduction
This software is a development started by Thomas Trouchkine during its PhD.
thesis at the French Cybersecurity Agency (ANSSI). It aims at providing all the
tools needed for analyzing fault experiments regarding the state of the art of
fault models. It also propose a way for plotting results to use them in
scientific papers.

The use of this tool by the community may simplify the understanding and
repeatability of the fault experiments done in the hardware security
laboratories worlwide.

The fault analyzer has been thought to be modular. Moreover, adding analyzer
modules or fault models has been thought to an easy thing. The goal is that the
community can add everything that is specifics to its particular case while
benefiting from others contributions.

## Maintainer
- Thomas Trouchkine (thomas.trouchkine@ssi.gouv.fr)

## Copyright and license

Copyright ANSSI (2017-2021)

This software is licensed under MIT license. See LICENSE file in the root folder of the project.

## Authors
- Thomas Trouchkine (thomas.trouchkine@ssi.gouv.fr)

## Quick start

### Initialize the environment (first time)
```sh
make init
```

### Run the analyzer
```sh
make run
```

## Documentation

### Online
[https://anssi-fr.github.io/Faults_analyzer/](https://anssi-fr.github.io/Faults_analyzer/)

### Build locally
```sh
cd doc && make show
```

## TODO
- Add a reboot analyzer in the `Analyzer` class in the
  `modules/new_analyzer/analyzer.py` file. In particular for having the reboot
  matrix when analyzing carto experiments.
- Add an AES module
- Add a module for testing the faulted values against the values observed in the
  non tested register after the executions. These values might be different from
  the initial values but involved in the fault model.