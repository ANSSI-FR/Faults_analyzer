import numpy as np

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerCarto(FaultAnalyzerDecorator):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.coord_name = init_arg("coordinates_name", kwargs)
        if "carto_resolution" in kwargs:
            self.resolution = init_arg("carto_resolution", kwargs)
        else:
            self.resolution = self.compute_resolution()

        self.clear_matrix()
        self.add_matrix_to_results()

    def compute_resolution(self):
        resolution = []
        for coord in self.coord_name:
            size = max(list(self.df[coord].unique)) + 1
            resolution.append(size)
        return resolution

    def add_matrix_to_results(self):
        fault_matrix_res = {
            "title": "Fault matrix",
            "data": self.fault_matrix,
            "label": "Number of fault per position"
        }
        self.results.append(fault_matrix_res)

    def clear_matrix(self):
        self.fault_matrix = np.zeros(self.resolution)

    def analyze(self, ope):
        super().analyze(ope)
        self.update_matrix(ope, self.fault_matrix)

    def update_matrix(self, ope, mat):
        """Update the matrix with the coordinates of the operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        ope_coord = []
        for coord in self.coord_name:
            if np.isnan(ope[coord]):
                return
            ope_coord.append(int(ope[coord]))
        mat[tuple(ope_coord)] += 1

