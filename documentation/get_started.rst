Get started
===========

Quick start
___________

Configure the list of experiments in ``config/manip_info_list.py``. This file contains the list of experiment, an experiment is a dictionary containing the inputs for a Manip object (the path to the result file, a dictionary containing the parameters for the analysis and a identification name).

Start the software:

>>> cd fault_analyzer
>>> ./main.py

A command line interface appears:

>>> fa>

Print the available experiments:

>>> fa> print

The list of the experiments appears:

>>> [0] ( ) Intel Core i3 Linux [mov rbx,rbx] EM
>>> [1] ( ) Intel Core i3 Linux [mov rbx,rbx] EM 2
>>> [2] ( ) Intel Core i3 Linux [orr rbx,rbx] EM

Select the experiment to analyze using its index:

>>> fa> select 0

The experiment must be set as selected ``(S)``:

>>> [0] (S) Intel Core i3 Linux [mov rbx,rbx] EM
>>> [1] ( ) Intel Core i3 Linux [mov rbx,rbx] EM 2
>>> [2] ( ) Intel Core i3 Linux [orr rbx,rbx] EM

Start the analysis:

>>> fa> analyze

The experiment must be set as analyzed ``(A)``:

>>> [0] (A) Intel Core i3 Linux [mov rbx,rbx] EM
>>> [1] ( ) Intel Core i3 Linux [mov rbx,rbx] EM 2
>>> [2] ( ) Intel Core i3 Linux [orr rbx,rbx] EM

Print the available results of the analyzed experiment using its index:

>>> fa> print 0

This displays at least:

>>> [0] General statistics
>>> [1] Effect of the power value
>>> [2] Effect of the delay
>>> [3] Observed statistics
>>> [4] Faulted values statistics
>>> [5] Fault model statistics

Print a result from the available results of the analyzed experiment using the experiment index and the result index:

>>> fa> print 0 0

This displays:

>>> +------------------------------------------+---------------------+
>>> |                Statistic                 |        Value        |
>>> +------------------------------------------+---------------------+
>>> |        Number of operations to do        |        50000        |
>>> |         Number of operation done         |         7336        |
>>> |           Percentage done (%)            |        14.672       |
>>> |            Number of reboots             |         1088        |
>>> |        Percentage of reboots (%)         |  14.830970556161397 |
>>> |     Number of responses bad formated     |         1065        |
>>> | Percentage of responses bad formated (%) |  14.517448200654307 |
>>> |             Number of faults             |          23         |
>>> |         Percentage of faults (%)         | 0.31352235550708835 |
>>> |          Number of faulted obs           |          23         |
>>> |      Average faulted obs per fault       |         1.0         |
>>> +------------------------------------------+---------------------+

