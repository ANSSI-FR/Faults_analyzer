from .arg_init import init_arg

from .fault_analyzer_component import FaultAnalyzerComponent

class FaultAnalyzer(FaultAnalyzerComponent):
    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results

    def analyze(self, ope):
        pass

    def post_analysis(self):
        pass
