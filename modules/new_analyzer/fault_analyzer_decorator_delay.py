import numpy as np

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerDelay(FaultAnalyzerDecorator):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        # Initialize needed parameters
        self.delay_name = init_arg("delay_name", kwargs)
        if ("delay_start" in kwargs) and ("delay_end" in kwargs) and ("delay_step" in kwargs):
            self.delays = list(np.arange(kwargs["delay_start"], kwargs["delay_end"], kwargs["delay_step"]))
        else:
            self.delays = list(self.df[self.delay_name].unique())

        # Initialize the fault data
        self.nb_faults_per_delay = [0]*len(self.delays)

        self.nb_faults_per_delay_data = [self.delays]

        # Create the result
        self.results += [
            {
                "title": "Number of faults per delay",
                "data": self.nb_faults_per_delay_data,
                "labels": ["Delays", "Number of faults"]
            }
        ]

    def analyze(self, ope):
        super().analyze(ope)
        delay = ope[self.delay_name]
        index = self.delays.index(delay)
        self.nb_faults_per_delay[index] += 1

    def post_analysis(self):
        super().post_analysis()

        self.nb_faults_per_delay_data.append(self.nb_faults_per_delay)
