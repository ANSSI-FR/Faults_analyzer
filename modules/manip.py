import pandas as pd

class Manip():
    """A class containing the information about an experimental manipulation.

    """
    def __init__(self, result_file, analysis_params, id_name):
        """Constructor of the class.

        :param str result_file: the file containing the results of the experiment. For the moment, only .csv file can be read.
        :param dict analysis_params: the parameters needed by the Analyzer class.
        :param str id_name: an unique identification name for the experiment.

        """
        self.result_file = result_file
        self.analysis_params = analysis_params
        self.id_name = id_name
        self.analyzed = False
        self.carto = False
        if "carto" in self.analysis_params:
            self.carto = self.analysis_params["carto"]
            self.analysis_params.pop("carto")
        self.aes = False
        if "AES" in analysis_params:
            self.aes = analysis_params["AES"]
        self.CEA = False
        if "CEA" in analysis_params:
            self.CEA = analysis_params["CEA"]

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

    def print_info(self):
        to_print = "result_file: {}\n".format(self.result_file)
        to_print += "analysis_params: {}\n".format(self.analysis_params)
        to_print += "id_name: {}\n".format(self.id_name)
        to_print += "analyzed: {}\n".format(self.analyzed)
        to_print += "carto: {}\n".format(self.carto)
        to_print += "aes: {}\n".format(self.aes)
        print(to_print)
