from .arg_init import init_arg

from .analyzer_component import AnalyzerComponent

class FaultAnalyzerComponent(AnalyzerComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def analyze(self):
        pass

    def post_analysis(self):
        pass
