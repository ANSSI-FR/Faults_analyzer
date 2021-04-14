import numpy as np

from .arg_init import init_arg

from .fault_analyzer_decorator import FaultAnalyzerDecorator

class FaultAnalyzerCartoBase(FaultAnalyzerDecorator):
    def __init__(self, comp, **kwargs):
        super().__init__(comp, **kwargs)

        self.coord_name = init_arg("coordinates_name", kwargs)
        if "carto_resolution" in kwargs:
            self.resolution = init_arg("carto_resolution", kwargs)
        else:
            self.resolution = self.compute_resolution()

    def compute_resolution(self):
        resolution = []
        for coord in self.coord_name:
            #size = max(list(self.df[coord].unique)) + 1 # can't remember why I used this once
            size = max(list(self.df[coord])) + 1
            resolution.append(size)
        return resolution

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
