---
layout: home
title: Analyzer modules
permalink: /dev/analyzer_modules/
nav_order: 0
parent: Development
---

# Adding a new analyzer module
{: .no_toc}

- TOC
{:toc}

## Location
Modules for the analyzer are stored in the `modules/analyzer/` directory.

## Naming convention
Currently every analyzer module is defined in a file with the name
`fault_analyzer_decorator_MODULE_NAME.py`. The reason is that they are all
decorators of the analyzer component defined in `fault_analyzer_component.py`.

The class name of the module is define as `FaultAnalyzerMODULENAME`.

## Loading a module
The modules are loaded in the `modules/analyzer/analyzer.py` file, in the
`init_fault_analyzer()` function.
```python
# modules/analyzer/analyzer.py

def init_fault_analyzer(self, **kwargs):
    fa = FaultAnalyzer(self.results, **kwargs)
    fa = FaultAnalyzerBase(fa, **kwargs)
    if are_all(self.values_type, int):
        fa = FaultAnalyzerFaultModel(fa, **kwargs)
    if "carto" in kwargs:
        if kwargs["carto"]:
            fa = FaultAnalyzerCarto(fa, **kwargs)
            fa = FaultAnalyzerFaultModelsCarto(fa, **kwargs)
    if ("delay_name" in kwargs):
        fa = FaultAnalyzerDelay(fa, **kwargs)
    return fa
```

To load a module, it is only needed to import it:
```python
from .fault_analyzer_MODULE_NAME import FaultAnalyzerMODULENAME
```
and to add the following line to the `init_fault_analyzer()` function:
```python
fa = FaultAnalyzerMODULENAME(fa, **kwargs)
```

`**kwargs` is the `params` dictionary defined in the parameter file. It is
possible to make the loading of a module conditional by adding `if` statements.

## Developping a module
### Inheritance
A module inherit from the `FaultAnalyzerDecorator` class defined in the
`fault_analyzer_decorator` file.

```python
from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerMODULENAME(FaultAnalyzerDecorator):
    # My module
```

### Constructor
The constructor of a module must have the following prototype:
```python
def __init__(self, comp, **kwargs):
    super().__init__(comp, **kwargs)
```
- `comp` is the component we want to decorate with the module.
- `kwargs` is a dictionary of parameters.

To extract the wanted parameters from the dictionary, it is recommended to use
the `init_arg()` function from the `modules/analyzer/arg_init.py` file:
```python
from .arg_init import init_arg

def __init__(self, comp, **kwargs):
    super().__init__(comp, **kwargs)
    
    self.my_param = init_arg("my_param_name", kwargs)
```

Then it is recommended to create the results structure. The results is a list of
dictionary, each dictionary represent a result computed by the module and has
three parameters:
- a title which able to identify the result,
- a data set which stores the result values,
- a set of labels which able to identify the different data sets.
For instance:

```python

# Create result set
self.my_result1_set = []
self.my_result2_set = []

# Create a result data
self.my_result_data = []

# Add the result data to the results object
self.results += [{
    "title": "My title",
    "data": self.my_result_data,
    "labels": ["My first label", "My second label"]
}]
```

### Mandatory functions
There are two mandatory functions.

- `analyze(self, ope)`

  This function is called for every load module. The `ope`
  parameter is a line from the manip file. It is possible to access to the
  different fields of this line by calling `ope["field_name"]`.
  
  This function must always call the `super().analyze(ope)` function before doing
  anything. Otherwise the decorator pattern will not work.
  {: .danger}
  
  For instance:
  ```python
  def analyze(self, ope):
      super().analyze(ope)
      self.my_result1_set.append(ope["param1"])
      self.my_result2_set.append(ope["param2"])
  ```
  
- `post_analysis(self)`

  This function is called after the whole analysis process for every module. It
  is used for setting the actual results once the analysis is done.
  
  This function must always call the `super().post_analysis()` function before
  doing anything. Otherwise the decorator pattern will not work.
  {: .danger}
  
  For instance:
  ```python
  def post_analysis(self):
      super().post_analysis()
      self.my_result_data = [self.my_result1_set, self.my_result2_set]
  ```
  
## Template
A template is available in the
`modules/analyzer/fault_analyzer_decorator_template.py` file:
```python
# modules/analyzer/fault_analyzer_decorator_template.py

from .arg_init import init_arg

# Import the FaultAnalyzerDecorator class for inheritance
from .fault_analyzer_decorator import FaultAnalyzerDecorator

# Create a child class of the FaultAnalyzerDecorator class
class FaultAnalyzerTEMPLATE(FaultAnalyzerDecorator):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        # Initialize the parameters you need
        self.my_param = init_arg("my_param_name", kwargs)

        # Create a result data
        self.my_result_data = []

        # Add the result data to the results object
        self.results += [{
            "title": "My title",
            "data": self.my_result_data,
            "labels": ["My first label", "My second label"]
        }]

    # Overwrite the analyze method
    def analyze(self, ope):
        # Call the parent class method
        super().analyze(ope)
        # Update your data
        self.update_data(self.my_result_data)

    def update_data(self, data):
        pass

    def post_analysis(self):
        super().post_analysis()
        # You can modify the results here
```