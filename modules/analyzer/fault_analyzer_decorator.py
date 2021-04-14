from .fault_analyzer_component import FaultAnalyzerComponent

class FaultAnalyzerDecorator(FaultAnalyzerComponent):
    def __init__(self, comp, **kwargs):
        super().__init__(**kwargs)
        self.comp = comp
        self.results = self.comp.results

    def analyze(self, ope):
        self.comp.analyze(ope)

    def post_analysis(self):
        self.comp.post_analysis()
