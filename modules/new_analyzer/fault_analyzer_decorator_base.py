from ..utils import format_table, norm_percent, are_all

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerBase(FaultAnalyzerDecorator):

    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.nb_faults = 0
        self.general_data = []

        self.nb_faults_per_obs = [0]*len(self.obs)
        if are_all(self.values_type, int):
            self.obs_data = [self.obs, format_table(self.default_values, self.data_format), self.to_test]
        else:
            self.obs_data = [self.obs, self.default_values, self.to_test]

        self.faulted_values = []
        self.faulted_values_occurrence = []
        self.faulted_values_data = []

        self.results += [
            {
                "title": "Faults general information",
                "data": [
                    ["Number of faults", "Fault probability (%)"],
                    self.general_data
                ],
                "labels": ["Information", "Values"]
            },
            {
                "title": "Observed statistics",
                "data": self.obs_data,
                "labels": ["Names", "Default values", "Tested", "Fault probability (%)"]
            },
            {
                "title": "Faulted values statistics",
                "data": self.faulted_values_data,
                "labels": ["Values", "Probability of appearance (%)"]
            }
        ]

    def update_faulted_values(self, fv):
        if fv in self.faulted_values:
            i = self.faulted_values.index(fv)
            self.faulted_values_occurrence[i] += 1
        else:
            self.faulted_values.append(fv)
            self.faulted_values_occurrence.append(1)

    def analyze(self, ope):
        super().analyze(ope)
        self.nb_faults += 1
        faults = self.get_faults(ope)
        for f in faults:
            self.nb_faults_per_obs[f.faulted_obs] += 1
            self.update_faulted_values(f.faulted_value)

    def post_analysis(self):
        """We need to set the result data in a post analysis function as we can't
        access array elements via their reference.

        For instance:
        > a = 5
        > b = [a]
        > b
        > [5]
        > a = 6
        > b
        > [5]

        """
        super().post_analysis()

        self.general_data.append(self.nb_faults)
        self.general_data.append(self.nb_faults/self.nb_operations*100)

        self.obs_data.append(norm_percent(self.nb_faults_per_obs))

        if are_all(self.values_type, int):
            self.faulted_values_data.append(format_table(self.faulted_values, self.data_format))
        else:
            self.faulted_values_data.append(self.faulted_values)
        self.faulted_values_data.append(norm_percent(self.faulted_values_occurrence))
