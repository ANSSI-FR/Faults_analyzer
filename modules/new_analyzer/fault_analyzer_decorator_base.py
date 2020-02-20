from ..utils import format_table, norm_percent, are_all

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerBase(FaultAnalyzerDecorator):

    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.nb_faults = 0
        self.nb_faulted_obs = 0
        self.nb_faults_per_obs = [0]*len(self.obs)

        self.faulted_values = []
        self.faulted_values_occurrence = []

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
        self.nb_faulted_obs += len(faults)
        for f in faults:
            self.nb_faults_per_obs[f.faulted_obs] += 1
            self.update_faulted_values(f.faulted_value)

    def post_analysis(self):
        """

        """
        super().post_analysis()

        # Generic information about the results
        self.results.append(
            {
                "title": "Faults general information",
                "data": [
                    ["Number of faults", "Fault probability (%)", "Average number of faulted observed per fault"],
                    [self.nb_faults, self.nb_faults/self.nb_operations*100, self.nb_faulted_obs/self.nb_faults]
                ],
                "labels": ["Information", "Values"]
            }
        )

        if are_all(self.values_type, int):
            default_values = format_table(self.default_values, self.data_format)
        else:
            default_values = self.default_values
        self.results.append(
            {
                "title": "Observed statistics",
                "data": [self.obs, default_values, self.to_test, norm_percent(self.nb_faults_per_obs)],
                "labels": ["Names", "Default values", "Tested", "Fault probability (%)"]
            }
        )

        if are_all(self.values_type, int):
            faulted_values = format_table(self.faulted_values, self.data_format)
        else:
            faulted_values = self.faulted_values
        self.results.append(
            {
                "title": "Faulted values statistics",
                "data": [faulted_values, norm_percent(self.faulted_values_occurrence)],
                "labels": ["Values", "Probability of appearance (%)"]
            }
        )
