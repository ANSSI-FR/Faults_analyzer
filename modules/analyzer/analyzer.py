import os, sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from ..utils import intable, print_progress_bar, are_all

from .arg_init import init_arg

from .analyzer_component import AnalyzerComponent

from .fault_analyzer import FaultAnalyzer
from .fault_analyzer_decorator_base import FaultAnalyzerBase
from .fault_analyzer_decorator_delay import FaultAnalyzerDelay
from .fault_analyzer_decorator_carto import FaultAnalyzerCarto
from .fault_analyzer_decorator_fault_models import FaultAnalyzerFaultModels
from .fault_analyzer_decorator_fault_models_carto import FaultAnalyzerFaultModelsCarto

from .reboot_analyzer import RebootAnalyzer

class Analyzer(AnalyzerComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = []
        self.fault_analyzer = self.init_fault_analyzer(**kwargs)
        self.reboot_analyzer = RebootAnalyzer(self.results, **kwargs)

    def init_fault_analyzer(self, **kwargs):
        fa = FaultAnalyzer(self.results, **kwargs)
        fa = FaultAnalyzerBase(fa, **kwargs)
        if are_all(self.values_type, int):
            fa = FaultAnalyzerFaultModels(fa, **kwargs)
        if "carto" in kwargs:
            if kwargs["carto"]:
                fa = FaultAnalyzerCarto(fa, **kwargs)
                fa = FaultAnalyzerFaultModelsCarto(fa, **kwargs)
        if ("delay_name" in kwargs):
            if kwargs["delay_name"] in fa.df:
                fa = FaultAnalyzerDelay(fa, **kwargs)
        return fa

    def get_results(self):
        self.run()
        return self.results

    def run(self):
        i = 0
        for _, ope in self.df.iterrows():
            self.analyze(ope)
            print_progress_bar(i, self.nb_operations, prefix = "Analysis progress:", suffix = "Complete", length=50)
            i += 1
        print_progress_bar(self.nb_operations, self.nb_operations, prefix =
                           "Analysis progress:", suffix = "Complete", length=50)
        self.post_analysis()

    def post_analysis(self):
        self.fault_analyzer.post_analysis()
        self.reboot_analyzer.post_analysis()

    def is_done(self, ope):
        if self.done_name == None:
            return True
        else:
            return ope[self.done_name]

    def analyze(self, ope):
        if self.is_done(ope):
            if self.is_reboot(ope):
                self.reboot_analyzer.analyze(ope)
            if self.is_log_bad_formated(ope):
                pass
            elif self.is_faulted(ope):
                self.fault_analyzer.analyze(ope)

    def is_log_bad_formated(self, ope):
        try:
            log = ope[self.log_name]
            log = log.split(self.log_sep)
            # Check the begin flag
            if log[0] != self.log_begin:
                return True
            else:
                log = log[1:]
            # Check the end flag
            if log[-1] != self.log_end:
                return True
            else:
                log = log[:-1]
            # Check the number of values
            if len(log) != len(self.obs):
                return True
            # Check values can be converted to their expected type
            for v, v_type, base in zip(log, self.values_type, self.result_base):
                if v_type == int:
                    if not intable(v, base):
                        return True
            return False
        except:
            return True

    def is_reboot(self, ope):
        if self.reboot_name in ope:
            return ope[self.reboot_name]
        else:
            return False

    def is_faulted(self, ope):
        faults = self.get_faults(ope)
        if len(faults) > 0:
            return True
        else:
            return False
