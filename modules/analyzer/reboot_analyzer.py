import numpy as np

from .arg_init import init_arg

from .analyzer_component import AnalyzerComponent

class RebootAnalyzer(AnalyzerComponent):
    """The reboot analyzer essentially create the reboot matrix.

    """
    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results
        self.coord_name = init_arg("coordinates_name", kwargs)
        if "carto_resolution" in kwargs:
            self.resolution = init_arg("carto_resolution", kwargs)
        else:
            self.resolution = self.compute_resolution()
        self.reboot_matrix = np.zeros(self.resolution)

    def compute_resolution(self):
        resolution = []
        for coord in self.coord_name:
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

    def analyze(self, ope):
        self.update_matrix(ope, self.reboot_matrix)

    def post_analysis(self):
        reboot_matrix_res = {
            "title": "Reboot matrix",
            "data": self.reboot_matrix,
            "label": "Number of reboots per position"
        }
        self.results.append(reboot_matrix_res)
