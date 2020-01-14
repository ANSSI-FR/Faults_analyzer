import pandas as pd

class Manip():
    """A class containing the information about an experimental manipulation.

    """
    def __init__(self, result_file, analysis_params, id_name, carto=False, aes=False):
        """Constructor of the class.

        :param str result_file: the file containing the results of the experiment. For the moment, only .csv file can be read.
        :param dict analysis_params: the parameters needed by the Analyzer class.
        :param str id_name: an unique identification name for the experiment.

        """
        self.result_file = result_file
        self.analysis_params = analysis_params
        self.id_name = id_name
        self.analyzed = False
        self.carto = carto
        self.aes = aes

    def get_dataframe(self):
        """Extract the dataframe from the result file.

        :returns: a pandas dataframe object containing all the results of the experiment.

        """
        return pd.read_csv(self.result_file, error_bad_lines=False)

    def get_params(self):
        """Format the parameters for being used for creating an Analyzer class.

        :returns: a dictionary usable for creating an Analyzer class.

        """
        self.analysis_params.update({"dataframe": self.get_dataframe()})
        return self.analysis_params

    def __str__(self):
        """:returns: the identification name of the experiment.

        """
        return self.id_name
