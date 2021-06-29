from ..utils import norm_percent, format_table

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

from .fault_models import get_fault_model, DataFaultModel, InstructionFaultModel

class FaultAnalyzerFaultModels(FaultAnalyzerDecorator):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.my_result_data = []

        self.data_fault_model_names = []
        self.data_fault_model_occurrences = []
        self.data_fault_model_destinations = []

        self.unknown_fault_model_occurrence = 0
        self.unknown_fault_model_values = []
        self.unknown_fault_model_destinations = [0]*len(self.obs)

        self.inst_fault_model_names = []
        self.inst_fault_model_occurrences = []
        self.inst_fault_model_destinations = []
        self.inst_fault_model_origins = []
        self.inst_fault_model_origins_occurrence = []

        self.suffix = "" # This suffix can be used in child class to identify
                         # it. Used in the fault model after execution module.

    def get_values_after_execution_from_log(self, ope):
        """Get the values of the registers from the log.

        """
        log = ope[self.log_name]
        log = log.split(self.log_sep)[1:-1]
        values = [int(v,b) for v,b in zip(log,self.result_base)]
        return values

    def analyze(self, ope):
        super().analyze(ope)
        faults = self.get_faults(ope)
        for fault in faults:
            fault_model = get_fault_model(fault, self.default_values, self.nb_bits)
            if fault_model == None: # If we don't get a suitable fault model, we try with values after execution
                values_after_exec = self.get_values_after_execution_from_log(ope)
                fault_model = get_fault_model(fault, values_after_exec, self.nb_bits, suffix=" after execution")
            if type(fault_model) == DataFaultModel:
                self.update_data_fault_model(fault, fault_model)
            elif type(fault_model) == InstructionFaultModel:
                self.update_inst_fault_model(fault, fault_model)
            else:
                self.unknown_fault_model_occurrence += 1
                self.unknown_fault_model_destinations[fault.faulted_obs] += 1
                if fault.faulted_value not in self.unknown_fault_model_values:
                    self.unknown_fault_model_values.append(fault.faulted_value)

    def get_origin_name(self, fault_model):
            if type(fault_model.origin) == int:
                origin_name = str(self.obs[fault_model.origin])
            else:
                origin_names = [self.obs[i] for i in fault_model.origin]
                origin_name = "(" + ", ".join(origin_names) + ")"
            return origin_name

    def update_inst_fault_model(self, fault, fault_model):
        if (fault_model.name + self.suffix) in self.inst_fault_model_names:
            i = self.inst_fault_model_names.index(fault_model.name + self.suffix)
            self.inst_fault_model_occurrences[i] += 1
            self.inst_fault_model_destinations[i][fault.faulted_obs] += 1
            origin_name = self.get_origin_name(fault_model)
        else:
            self.inst_fault_model_names.append(fault_model.name + self.suffix)
            self.inst_fault_model_occurrences.append(1)
            self.inst_fault_model_destinations.append([0]*len(self.obs))
            self.inst_fault_model_destinations[-1][fault.faulted_obs] += 1
            origin_name = self.get_origin_name(fault_model)
            self.inst_fault_model_origins.append([])
            self.inst_fault_model_origins[-1].append(origin_name)
            self.inst_fault_model_origins_occurrence.append([])
            self.inst_fault_model_origins_occurrence[-1].append(1)

    def update_fault_model_origins(self, fault_model_index, origin_name):
        i = fault_model_index
        if origin_name in self.inst_fault_model_origins[i]:
            self.inst_fault_model_origins_occurrence[i] += 1
        else:
            self.inst_fault_model_origins[i].append(origin_name)
            self.inst_fault_model_origins_occurrence[i].append(1)

    def update_data_fault_model(self, fault, fault_model):
        if fault_model.name in self.data_fault_model_names:
            i = self.data_fault_model_names.index(fault_model.name)
            self.data_fault_model_occurrences[i] += 1
            self.data_fault_model_destinations[i][fault.faulted_obs] += 1
        else:
            self.data_fault_model_names.append(fault_model.name)
            self.data_fault_model_occurrences.append(1)
            self.data_fault_model_destinations.append([0]*len(self.obs))
            self.data_fault_model_destinations[-1][fault.faulted_obs] += 1

    def post_analysis(self):
        super().post_analysis()

        fault_model_names = ["Unknown"] + self.data_fault_model_names + self.inst_fault_model_names
        fault_model_occurrences = [self.unknown_fault_model_occurrence] + self.data_fault_model_occurrences + self.inst_fault_model_occurrences
        res = {
            "title": "Fault model statistics",
            "data": [fault_model_names, fault_model_occurrences, norm_percent(fault_model_occurrences)],
            "labels": ["Names", "Occurrences (#)", "Occurrences (%)"]
        }
        self.results.append(res)

        res = {
            "title": "Unknown fault model values",
            "data": [format_table(self.unknown_fault_model_values, self.data_format)],
            "labels": ["Values"]
        }
        self.results.append(res)

        for i, fault_model in enumerate(self.data_fault_model_names):
            res = {
                "title": fault_model + " destination occurrence",
                "data": [self.obs, norm_percent(self.data_fault_model_destinations[i])],
                "labels": ["Names", "Occurrence (%)"]
            }
            self.results.append(res)

        for i, fault_model in enumerate(self.inst_fault_model_names):
            res = {
                "title": fault_model + " destination occurrence",
                "data": [self.obs, norm_percent(self.inst_fault_model_destinations[i])],
                "labels": ["Names", "Occurrence (%)"]
            }
            self.results.append(res)

        for i, fault_model in enumerate(self.inst_fault_model_names):
            res = {
                "title": fault_model + " origin occurrence",
                "data": [self.inst_fault_model_origins[i], norm_percent(self.inst_fault_model_origins_occurrence[i])],
                "labels": ["Names", "Occurrence (%)"]
            }
            self.results.append(res)
