import numpy as np

from .analyzer import Analyzer

class CartoAnalyzer(Analyzer):
    """Class doing the analysis of fault attacks cartography experiments. Inherit from the Analyzer class.

    """

    def get_map_size(self):
        """Extract the map size of the cartography from the dataframe.

        :return: a list of integer representing the size of the cartography on the X-axis and on the Y-axis.

        """
        map_size = []
        for coord in self.coordinates:
            # Extract the maximum coordinate and add 1 to have the size
            size = max(list(self.df[coord].unique())) + 1
            map_size.append(size)
        return map_size

    def __init__(self,
                 coordinates,
                 stage_coordinates,
                 **kwargs):
        """Constructor of the class. Initialize all the needed parameters.

        Arguments:

        coordinates - the key names for the coordinates of the grid over the chip.

        stage_coordinates - the key names for the real position of the stage arms
        during the experiment.

        """
        super().__init__(**kwargs)

        self.coordinates = coordinates
        self.stage_coord_keys = stage_coordinates

        self.map_size = self.get_map_size()
        self.grid_coordinates = []
        for i in range(len(self.map_size)):
            self.grid_coordinates.append([])

        if len(self.stage_coord_keys) is len(self.map_size):
            self.stage_coordinates = []
            for i in range(len(self.stage_coord_keys)):
                self.stage_coordinates.append([])
        else:
            self.logger.warning("Stage and Grid don't have the same dimensions.")

        self.clear_matrix()

    def clear_reboot_powers_matrix(self):
        self.reboot_powers_matrix = []
        for i in range(len(self.powers)):
            self.reboot_powers_matrix.append(np.zeros(self.map_size))

    def update_reboot_powers_matrix(self, ope):
        if not np.isnan(ope[self.power_name]):
            i = self.powers.index(ope[self.power_name])
            self.update_matrix(ope, self.reboot_powers_matrix[i])

    def get_reboot_powers_matrix(self):
        return self.reboot_powers_matrix

    def clear_matrix(self):
        self.reboot_matrix = np.zeros(self.map_size)
        self.fault_matrix = np.zeros(self.map_size)
        self.done_matrix = np.zeros(self.map_size)
        self.response_bad_formated_matrix = np.zeros(self.map_size)
        self.clear_reboot_powers_matrix()

    def update_matrix(self, ope, mat):
        """Update the matrix with the coordinates of the operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        ope_coord = []
        for coord in self.coordinates:
            if np.isnan(ope[coord]):
                return
            ope_coord.append(int(ope[coord]))
        mat[tuple(ope_coord)] += 1

    def update_response_bad_formated_matrix(self, ope):
        """Update the response bad formated matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.update_matrix(ope, self.response_bad_formated_matrix)

    def update_done_matrix(self, ope):
        """Update the done matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.update_matrix(ope, self.done_matrix)

    def update_fault_matrix(self, ope):
        """Update the fault matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.update_matrix(ope, self.fault_matrix)

    def update_reboot_matrix(self, ope):
        """Update the reboot matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.update_matrix(ope, self.reboot_matrix)

    def is_done_analysis(self, ope):
        """Do the analysis routine in the case the operation is done. Override the
        method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super().is_done_analysis(ope)
        self.update_done_matrix(ope)

    def is_reboot_analysis(self, ope):
        """Do the analysis routine in the case the operation has led to a reboot.
        Override the method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super().is_reboot_analysis(ope)
        self.update_reboot_matrix(ope)
        self.update_reboot_powers_matrix(ope)

    def is_faulted_analysis(self, ope):
        """Do the analysis routine in the case the operation has led to a fault.
        Override the method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super().is_faulted_analysis(ope)
        self.update_fault_matrix(ope)
    
    def update_coordinates_correspondance(self, ope):
        """Update the coordinates correspondance of the operation between the grid
        coordinates and the stage coordinates.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        for i, coord in enumerate(self.coordinates):
            if not ope[coord] in self.grid_coordinates[i]:
                self.grid_coordinates[i].append(ope[coord])
                self.stage_coordinates[i].append(ope[self.stage_coord_keys[i]])

    def analysis(self, ope):
        """Run the analysis on a given operation. Override the method from Analyzer
        class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super().analysis(ope)
        self.update_coordinates_correspondance(ope)

    
    def get_coordinates_correspondance(self):
        """Return the grid coordinates and their correspondance as positions for the
        stage arms.

        """
        self.check_analysis_done()
        return [self.grid_coordinates, self.stage_coordinates]

    def get_reboot_matrix(self):
        """Return the reboot matrix.

        """
        self.check_analysis_done()
        return self.reboot_matrix

    def get_fault_matrix(self):
        """Return the fault matrix.

        """
        self.check_analysis_done()
        return self.fault_matrix

    def get_done_matrix(self):
        """Return the done matrix.

        """
        self.check_analysis_done()
        return self.done_matrix

    def get_response_bad_formated_matrix(self):
        """Return the response bad formated matrix.

        """
        self.check_analysis_done()
        return self.response_bad_formated_matrix

    def get_matrices(self):
        ret = [
            {
                "title": "Reboots matrix",
                "data": self.reboot_matrix,
                "label": "Number of reboots per positions"
            },
            {
                "title": "Done matrix",
                "data": self.done_matrix,
                "label": "Number of operations done per positions"
            },
            {
                "title": "Faults matrix",
                "data": self.fault_matrix,
                "label": "Number of faults per positions"
            },
            {
                "title": "Response bad formated matrix",
                "data": self.response_bad_formated_matrix,
                "label": "Number of responses bad formated per positions"
            },
        ]
        for i, power in enumerate(self.powers):
            ret.append({
                "title": "Reboots matrix at {}V".format(power),
                "data": self.reboot_powers_matrix[i],
                "label": "Number of reboot per position"
            })
        return ret

    def run_analysis(self):
        self.clear_matrix()
        super().run_analysis()

    def get_coordinates_correspondance_result(self, axe):
        coord = "unknown"
        if axe == 0:
            coord = "y"
        elif axe == 1:
            coord = "x"
        else:
            return None
        ret = {
            "title": "Coordinates correspondance on {} axis".format(coord),
            "labels": [self.coordinates[axe], self.stage_coord_keys[axe]],
            "data": [self.grid_coordinates[axe], self.stage_coordinates[axe]]
        }
        return ret

    def get_results(self):
        results = super().get_results()
        results.append(self.get_coordinates_correspondance_result(0))
        results.append(self.get_coordinates_correspondance_result(1))
        results += self.get_matrices()
        return results

    def is_response_bad_formated_analysis(self, ope):
        super().is_response_bad_formated_analysis(ope)
        self.update_response_bad_formated_matrix(ope)
