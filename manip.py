import pandas as pd

class Manip():

    result_file = ""
    analysis_params = {}
    id_name = ""
    analyzed = False

    def __init__(self, result_file, analysis_params, id_name):
        self.result_file = result_file
        self.analysis_params = analysis_params
        self.id_name = id_name

    def get_dataframe(self):
        return pd.read_csv(self.result_file, error_bad_lines=False)

    def get_params(self):
        self.analysis_params.update({"dataframe": self.get_dataframe()})
        return self.analysis_params

    def __str__(self):
        return self.id_name
