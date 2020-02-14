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
        self.results.append({
            "title": "My title",
            "data": self.my_result_data,
            "labels": ["My first label", "My second label"]
        })

    # Overwrite the analyze method
    def analyze(self, ope):
        # Call the parent class method
        super().analyze(ope)
        # Update your data
        self.update_data(self.my_result_data)

    def update_data(self, data):
        pass
