import numpy as np

from .fault_models import fault_models, InstructionFaultModel, DataFaultModel, get_fault_model
from .fault_analyzer_decorator_carto_base import FaultAnalyzerCartoBase

class FaultAnalyzerFaultModelsCarto(FaultAnalyzerCartoBase):

    title_format = "{} fault model matrix"

    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)
        self.matrices = [np.zeros(self.resolution)]
        self.fault_model_names = ["Unknown"]

    def post_analysis(self):
        super().post_analysis()
        for i, fm_name in enumerate(self.fault_model_names):
            res = {
                "title": self.title_format.format(fm_name),
                "data": self.matrices[i],
                "label": "Number of faults per position"
            }
            self.results.append(res)

    def update_fault_model_unknown_matrix(self, ope):
        self.update_matrix(ope, self.matrices[0])

    def analyze(self, ope):
        super().analyze(ope)
        faults = self.get_faults(ope)
        for fault in faults:
            fault_model = get_fault_model(fault, self.default_values, self.nb_bits)
            if fault_model == None:
                self.update_fault_model_unknown_matrix(ope)
            else:
                self.update_fault_model_matrix(fault_model, ope)

    def update_fault_model_matrix(self, fault_model, ope):
        if fault_model.name in self.fault_model_names:
            ind = self.fault_model_names.index(fault_model.name)
            self.update_matrix(ope, self.matrices[ind])
        else:
            self.fault_model_names.append(fault_model.name)
            self.matrices.append(np.zeros(self.resolution))
            self.update_matrix(ope, self.matrices[-1])
