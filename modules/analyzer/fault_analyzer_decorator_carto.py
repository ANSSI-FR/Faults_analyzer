import numpy as np

from .fault_analyzer_decorator_carto_base import FaultAnalyzerCartoBase

class FaultAnalyzerCarto(FaultAnalyzerCartoBase):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)
        self.fault_matrix = np.zeros(self.resolution)

    def post_analysis(self):
        super().post_analysis()
        fault_matrix_res = {
            "title": "Fault matrix",
            "data": self.fault_matrix,
            "label": "Number of faults per position"
        }
        self.results.append(fault_matrix_res)

    def analyze(self, ope):
        super().analyze(ope)
        self.update_matrix(ope, self.fault_matrix)

