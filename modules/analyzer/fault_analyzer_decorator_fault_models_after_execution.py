from ..utils import norm_percent, format_table

from .arg_init import init_arg

from .fault_models import get_fault_model

from .fault_analyzer_decorator_fault_models import FaultAnalyzerFaultModels

def get_result(results, result_name):
    return next((res for res in results if res["title"] == result_name), None)

class FaultAnalyzerFaultModelsAfterExecution(FaultAnalyzerFaultModels):
    """This class look for the fault models but considering the values of the
    observed parsed from the log instead of the initial values given in the
    parameters file.

    """
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.suffix = " after execution"

    def get_values_after_execution_from_log(self, ope):
        """Get the values of the registers from the log.

        """
        log = ope[self.log_name]
        log = log.split(self.log_sep)[1:-1]
        values = [int(v,b) for v,b in zip(log,self.result_base)]
        return values

    def get_fault_model(self, fault, ope):
        """We overload the function that get the fault model to use it on the values we
        got from the log.

        """
        values = self.get_values_after_execution_from_log(ope)
        return get_fault_model(fault, values, self.nb_bits)

    def post_analysis(self):
        super().post_analysis()

        # We must remove the old unknow fault model values from the results
        unknown_res = get_result(self.results, "Unknown fault model values")
        self.results.remove(unknown_res)

        # We must remove the old fault model statistics values from the results
        fault_model_res = get_result(self.results, "Fault model statistics")
        self.results.remove(fault_model_res)