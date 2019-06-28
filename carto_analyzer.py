import logging

import numpy as np

from analyzer import Analyzer

class CartoAnalyzer(Analyzer):
    """Class doing the analysis of fault attacks experiments.

    This class must be given several parameters which help to do the experiments:

    dataframe - the dataframe object from the pandas library containing the
    results of the experiments.

    obs_names - the name of the observed items as named in the dataframe.

    default_values - the default values of the observed.

    to_test - a boolean array determining if an observed must be tested or not
    during the analysis.

    power_name - the key name for accessing the power value in the dataframe
    lines.

    delay_name - the key name for accessing the delay value in the dataframe
    lines.

    done_name - the key name for accessing if a line has been done or not.

    fault_name - the key name for checking if a line has been faulted or not.

    reboot_name - the key name for checking if a line has made a system reboot
    or not.

    log_name - the key name for getting the log in the dataframe line.

    log_separator - the symbol used for splitting the values in the log.

    data_format - the format string for displaying integer values (for example:
    0x{:08x}).

    nb_bits - the number of bits the integers must be considered encoded on.

    executed_instructions - a list containing the integer value of the executed
    instructions.

    coordinates - a list containing the key names for getting the coordinates
    over the chip.

    stage_coordinates - a list containing the key names for getting the
    position of the stage arms.

    """

    def _get_map_size(self):
        """Return the size of the map of the experiment.

        It needs two parameters:

        coordinates - a list containing the key names for getting the
        coordinates over the chip.

        dataframe - the dataframe object from the pandas library containing the
        results of the experiments.

        """
        map_size = []
        for coord in self.coordinates:
            # Extract the maximum coordinate and add 1 to have the size
            size = max(list(self.df[coord].unique())) + 1
            map_size.append(size)
        return map_size

    def __init__(self,
                 dataframe,
                 obs_names,
                 default_values,
                 to_test,
                 power_name,
                 delay_name,
                 done_name,
                 fault_name,
                 reboot_name,
                 log_name,
                 log_separator,
                 data_format,
                 nb_bits,
                 executed_instructions,
                 coordinates, # argument needed by the daughter class
                 stage_coordinates, # argument needed by the daughter class
                 log_level=logging.WARNING):
        """Constructor of the class. Initialize all the needed parameters.

        Arguments:

        dataframe - the dataframe object from the pandas library containing the
        results of the experiments.

        obs_names - the name of the observed items as named in the dataframe.

        default_values - the default values of the observed.

        to_test - a boolean array determining if an observed must be tested or not
        during the analysis.

        power_name - the key name for accessing the power value in the dataframe
        lines.

        delay_name - the key name for accessing the delay value in the dataframe
        lines.

        done_name - the key name for accessing if a line has been done or not.

        fault_name - the key name for checking if a line has been faulted or not.

        reboot_name - the key name for checking if a line has made a system reboot
        or not.

        log_name - the key name for getting the log in the dataframe line.

        log_separator - the symbol used for splitting the values in the log.

        data_format - the format string for displaying integer values (for example:
        0x{:08x}).

        nb_bits - the number of bits the integers must be considered encoded on.

        executed_instructions - a list containing the integer value of the executed
        instructions.

        coordinates - the key names for the coordinates of the grid over the chip.

        stage_coordinates - the key names for the real position of the stage arms
        during the experiment.

        """
        super().__init__(dataframe,
                         obs_names,
                         default_values,
                         to_test,
                         power_name,
                         delay_name,
                         done_name,
                         fault_name,
                         reboot_name,
                         log_name,
                         log_separator,
                         data_format,
                         nb_bits,
                         executed_instructions,
                         log_level)

        self.coordinates = coordinates
        self.stage_coord_keys = stage_coordinates

        self.map_size = self._get_map_size()
        self.grid_coordinates = []
        for i in range(len(self.map_size)):
            self.grid_coordinates.append([])

        if len(self.stage_coord_keys) is len(self.map_size):
            self.stage_coordinates = []
            for i in range(len(self.stage_coord_keys)):
                self.stage_coordinates.append([])
        else:
            self.logger.warning("Stage and Grid don't have the same dimensions.")

        # Matrix
        self.reboot_matrix = np.zeros(self.map_size)
        self.fault_matrix = np.zeros(self.map_size)
        self.done_matrix = np.zeros(self.map_size)

    def _update_matrix(self, ope, mat):
        """Update the matrix with the coordinates of the operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.
        
        """
        ope_coord = []
        for coord in self.coordinates:
            ope_coord.append(ope[coord])
        mat[tuple(ope_coord)] += 1

    def _update_done_matrix(self, ope):
        """Update the done matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self._update_matrix(ope, self.done_matrix)

    def _update_fault_matrix(self, ope):
        """Update the fault matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self._update_matrix(ope, self.fault_matrix)

    def _update_reboot_matrix(self, ope):
        """Update the reboot matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self._update_matrix(ope, self.reboot_matrix)

    def _is_done_analysis(self, ope):
        """Do the analysis routine in the case the operation is done. Override the
        method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super()._is_done_analysis(ope)
        self._update_done_matrix(ope)

    def _is_reboot_analysis(self, ope):
        """Do the analysis routine in the case the operation has led to a reboot.
        Override the method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super()._is_reboot_analysis(ope)
        self._update_reboot_matrix(ope)

    def _is_faulted_analysis(self, ope):
        """Do the analysis routine in the case the operation has led to a fault.
        Override the method from Analyzer class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super()._is_faulted_analysis(ope)
        self._update_fault_matrix(ope)
    
    def _update_coordinates_correspondance(self, ope):
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

    def _analysis(self, ope):
        """Run the analysis on a given operation. Override the method from Analyzer
        class.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        super()._analysis(ope)
        self._update_coordinates_correspondance(ope)

    
    def get_coordinates_correspondance(self):
        """Return the grid coordinates and their correspondance as positions for the
        stage arms.

        """
        self._check_analysis_done()
        return [self.grid_coordinates, self.stage_coordinates]

    def get_reboot_matrix(self):
        """Return the reboot matrix.

        """
        self._check_analysis_done()
        return self.reboot_matrix

    def get_fault_matrix(self):
        """Return the fault matrix.

        """
        self._check_analysis_done()
        return self.fault_matrix

    def get_done_matrix(self):
        """Return the done matrix.

        """
        self._check_analysis_done()
        return self.done_matrix
