# Plotter
> Python module for plotting data via descriptive file

## Getting started
Check out the `test_plotter.py` file to get the an overview of what you can do with `Plotter`

## Basic examples
### Static print
```python
from plotter import Plotter

to_plot = the_data_you_want_to_plot()

pl = Plotter(to_plot, figsuptitle="Static test", nb_to_plot=len(to_plot))
pl.init_plot()
pl.show()
```

### Dynamic print
```python
from plotter import Plotter
import time

to_plot = the_data_you_want_to_plot()

pl = Plotter(to_plot, figsuptitle="Dynamic test", nb_to_plot=len(to_plot))
pl.init_plot()
while 1:
    pl.set_to_plot(update_data_to_plot())
    pl.show(blocking=False)
    time.sleep(0.2)
```

The `to_plot` variable is a dictionnary containing the data you want to print and the way you want to print it. The following section describe how to format it.

## Formating data for plotting
### General description
If you want to print data you must give to the `Plotter()` constructor or `set_to_plot()` method a tab containing the description of what you want to print. Everything will be plot on the same figure. If you want to plot on different figures you must create several `Plotter` instances.

Every figure you want to plot is described through a dictionary containing the following fields :  
- Mandatory :
    - "data" : the variable containing the data you want to print (for example a matrix or an array)
    - "type" : the way you want to plot your data. the available types are :
        - "matrix" : print a matrix as a heat map
        - "bar" : print an array as bars
        - "scatter" : print a matrix (or 2 arrays) as a scatter
        - "hist" : print the histogram of an array
        - "trace" : print an array as a discrete function
- Optional :
    - "title" : the title you want to put on the top of the figure
    - "x_label" : the label you want to give on the X axis
    - "y_label" : the label you want to give on the Y axis
    - "legend" : the legend you want to give for your data set (work only with types "hist" and "bar")
    - "x_ticklabels" : the discrete values you want to give on the X axis (only tested with type "bar")
    - "show\_data\_value" : boolean value saying if you want to print the value of you data when doing a bar plotting 
    
### Example
```python
import numpy as np

matrix = np.random.random((100,100))
bar = np.random.random(5)

to_plot = [{
        "title": "Test matrix",
        "type" : "matrix",
        "data" : matrix,
        "x_label": "Abscissa",
        "y_label": "Orderly",
        "legend": ["This is random"]
    },
    {
        "title": "Bars monitoring",
        "type" : "bar",
        "data" : bar,
        "x_label": "X axis",
        "y_label": None,
        "legend": ["Test"],
        "x_ticklabels": ["French", "English", "Spanish", "Chinese", "German"]
    }]
```
