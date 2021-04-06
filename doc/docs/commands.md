---
layout: home
title: Commands
nav_order: 1
permalink: /cmds/
---

# Fault Analyzer commands
{: .no_toc}

*Last update: {% last_modified_at %}*

Using the fault analyzer, the documentation of the different commands is
available using the `?` or `help` command.

**List of commands:**
- TOC
{:toc}

---
## `analyze`
Analyze manips.

### Usage
{: .no_toc}
```sh
analyze [manip_index_list]
```

### Arguments
{: .no_toc}
- `manip_index_list`: the index list of the manips to analyze.

### Examples
{: .no_toc}
- `analyze 2` start the analysis of the manip with index 2
- `analyze 2,5` start the analysis of the manips with index 2 and 5
- `analyze 2-4` start the analysis of the manips with index 2 to 4

---
## `edit`
Able the edition of different parameters.

### Usage
{: .no_toc}
```sh
edit [parameter]
```

### Arguments
{: .no_toc}
- `parameter`: the parameter to edit.

### Available parameters:
{: .no_toc}
- `plot_tmp_style`: use this parameter to add temporary styles for the plots.

---
## `exit`
Exit the application.

### Shorthands
{: .no_toc}
`Ctrl+D`

---
## `help`
List available commands with `help` or detailed help with `help cmd`.

### Shorthands
{: .no_toc}
`?`

---
## `merge`
Merge results from different manip into a new manip.

### Usage
{: .no_toc}
```sh
merge [manip_index_list] [result_to_merge] [columns_to_merge] [columns_in_common] <name>
```

### Arguments
{: .no_toc}
- `manip_index_list`: the index list of the manips to analyze.
- `result_to_merge`: the result to merge. The same index will be used for all given manip.
- `columns_to_merge`: the columns to copy in the merged result. The merged result will contain the given column for every given manips.
- `columns_in_common`: the columns to not duplicate in the new result. Most of the time, a column that all results have in common. These columns must be a subpart of `columns_to_merge`.
- `name`: the name to give to the merged manip.

### Examples:
{: .no_toc}
- `merge 0-2 3 4-5 4`: merge all the 5th column of the 3rd result of manip with index 0 to 2 and add the 4th column once in a new result.
- `merge 0-2 3 4-5 4 new_merge`: merge all the 5th column of the 3rd result of manip with index 0 to 2 and add the 4th column once in a new result name "new_merge".

### Detailed example:
{: .no_toc}

I have two manips with a common result I want to compare.
```sh
fa> print 0 3

 bcm2837_andR8_iv4_EM_fix_20200127 results
===========================================
Observed statistics
+----------+---------------+-----------------------+-----------+--------+
| Observed | Default value | Value after execution | Fault (%) | Tested |
+----------+---------------+-----------------------+-----------+--------+
|    r0    |   0xfffe0001  |       0xfffe0001      |  22.6190  |  True  |
|    r1    |   0xfffd0002  |       0xfffd0002      |   1.1905  |  True  |
|    r2    |   0xfffb0004  |       0xfffb0004      |   1.1905  |  True  |
|    r3    |   0xfff70008  |       0xfff70008      |   1.1905  |  True  |
|    r4    |   0xffef0010  |       0xffef0010      |   1.1905  |  True  |
|    r5    |   0xffdf0020  |       0xffdf0020      |   1.1905  |  True  |
|    r6    |   0xffbf0040  |       0xffbf0040      |   1.1905  |  True  |
|    r7    |   0xff7f0080  |       0xff7f0080      |   1.1905  |  True  |
|    r8    |   0xfeff0100  |       0xfeff0100      |  67.8571  |  True  |
|    r9    |   0xfdff0200  |       0xfdff0200      |   1.1905  |  True  |
+----------+---------------+-----------------------+-----------+--------+

fa> print 1 3

 bcm2837_orrR5_iv3_EM_fix_20200124 results
===========================================
Observed statistics
+----------+---------------+-----------------------+-----------+--------+
| Observed | Default value | Value after execution | Fault (%) | Tested |
+----------+---------------+-----------------------+-----------+--------+
|    r0    |   0xc3d0c220  |       0xc3d0c220      |  10.4294  |  True  |
|    r1    |   0x72b8ccd6  |       0x72b8ccd6      |   0.0000  |  True  |
|    r2    |   0xf25f29b9  |       0xf25f29b9      |   0.2045  |  True  |
|    r3    |   0x22c7271d  |       0x22c7271d      |   0.0000  |  True  |
|    r4    |   0xd3f8f3b1  |       0xd3f8f3b1      |   1.4315  |  True  |
|    r5    |   0x3ba81d04  |       0x3ba81d04      |  87.7301  |  True  |
|    r6    |   0x7c22b133  |       0x7c22b133      |   0.0000  |  True  |
|    r7    |   0xcc302f01  |       0xcc302f01      |   0.0000  |  True  |
|    r8    |   0xafa42878  |       0xafa42878      |   0.2045  |  True  |
|    r9    |   0xdd4c70ca  |       0xdd4c70ca      |   0.0000  |  True  |
+----------+---------------+-----------------------+-----------+--------+
```

I want to merge the result 3 of the manips 0 and 1 into a new result which
contains the information from both original manips. The columns to merge are the
first one with the observed (index 0) and the 4th one with their fault
probability(index 3). The "Observed" column is in common.

I use the following `merge` function:

```sh
fa> merge 0-1 3 0,3 0
fa> print

Manips
========
[0]* bcm2837_andR8_iv4_EM_fix_20200127
[1]* bcm2837_orrR5_iv3_EM_fix_20200124
[2]* Merged results
```

It has created a new manip named "Merged results". I can manipulated it as a
classical result:

```sh
fa> print 2

 Merged results available results
==================================
[0] Merged Observed statistics

fa> print 2 0

 Merged results results
========================
Merged Observed statistics
+----------+---------------------------------------------+---------------------------------------------+
| Observed | bcm2837_andR8_iv4_EM_fix_20200127 Fault (%) | bcm2837_orrR5_iv3_EM_fix_20200124 Fault (%) |
+----------+---------------------------------------------+---------------------------------------------+
|    r0    |                   22.6190                   |                   10.4294                   |
|    r1    |                    1.1905                   |                    0.0000                   |
|    r2    |                    1.1905                   |                    0.2045                   |
|    r3    |                    1.1905                   |                    0.0000                   |
|    r4    |                    1.1905                   |                    1.4315                   |
|    r5    |                    1.1905                   |                   87.7301                   |
|    r6    |                    1.1905                   |                    0.0000                   |
|    r7    |                    1.1905                   |                    0.0000                   |
|    r8    |                   67.8571                   |                    0.2045                   |
|    r9    |                    1.1905                   |                    0.0000                   |
+----------+---------------------------------------------+---------------------------------------------+
```

---
## `plot`
Plot a result.

### Usage
{: .no_toc}
```sh
plot [manip_index] [result_index] [plot_style] <data_to_plot_index_list> <data_labels_index>
```

### Arguments
{: .no_toc}
- `manip_index`: the index of the manip containing the result to plot.
- `result_index`: the index of the result to plot.
- `plot_style`: the style to apply for the plot.
- `data_to_plot_index_list`: the index of the data to plot from the result.
- `data_labels_index`: the index of the data to use as index for the plot.

The `data_to_plot_index_list` and `data_labels_index` arguments are not
necessary for plotting matrices and pies.
{: .info}

### Styles
{: .no_toc}
See the [plot section]().

---
## `print`
Display the available manips and their results.

### Usage
{: .no_toc}
```sh
print <manip_index_list> <result_index_list>
```

### Arguments
{: .no_toc}
- `manip_index_list`: the index list of the manips to print.
- `result_index_list`: the index list of the results to print.

When displaying manips. There is an asterisk (*) next to the index if the manip
has already been analyzed (_i.e._ results are available for printing or
plotting). 
{: .info}

### Examples
{: .no_toc}
- `print` print the available manips.
- `print 4` print the available results of the manip with index 4
- `print 0,3` print the available results of the manips with index 0 and 3 
- `print 0,3 1-5` print the results with index 1 to 5 of the manips 0 and 3

---
## `save`
Save the manip results into a `.json` file.

### Usage
{: .no_toc}
```sh
save [manip_index] [filename]
```

### Arguments
{: .no_toc}
- `manip_index`: the index of the manip to save the results from.
- `filename`: the name of the file to save the results in.

### Examples
{: .no_toc}
- `save 3 new_results` save the results of the manip with index 3 in the file
  `new_results.json`.

The results are saved in the directory mentioned by the `results_dir` variable
in the `config.py`. Moreover, any result available in this directory is
automatically loaded at the startup of the analyzer (and therefore available as
an analyzed result).
{: .info}

---
## `tikz`
Export a plot into a tikz figure. It has the same syntax as the `plot` command
but you can add a `filename` at the end of the command.

### Usage
{: .no_toc}
```sh
tikz [manip_index] [result_index] [plot_style] <data_to_plot_index_list> <data_labels_index> <filename>
```

### Arguments
{: .no_toc}
- `manip_index`: the index of the manip containing the result to plot.
- `result_index`: the index of the result to plot.
- `plot_style`: the style to apply for the plot.
- `data_to_plot_index_list`: the index of the data to plot from the result.
- `data_labels_index`: the index of the data to use as index for the plot.
- `filename`: the file where to save the tikz code.
