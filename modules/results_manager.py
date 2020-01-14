import json

from .results import Results

class ResultsManager():
    """Class used for managing a list of Results.

    """
    def __init__(self, results_list=[], result_dir="."):
        """Constructor of the class.

        :param list results_list: the list of Results to manage.
        :param str result_dir: the directory storing the Results files.

        """
        super().__init__()
        self.results_list = results_list
        """The list of managed Results."""
        self.result_dir = result_dir
        """The directory storing the Results files."""

    def get_results_index(self, results):
        """:param Results results: the Results to get the index.

        :returns: the index of the Results.

        """
        return self.results_list.index(results)

    def add_results(self, results):
        """Add a Results to the Results list.

        :param Results results: the Results to add.

        """
        self.results_list.append(results)

    def get_result_titles(self, results_index):
        """Get the titles of a Results.

        :param int results_index: the index of the results to get the titles.

        :returns: a string containing the titles of the results.

        :TODO: return a list containing the titles.

        """
        if results_index < len(self.results_list):
            return self.results_list[results_index].get_results_titles_str()

    def get_all_result_str(self, results_index):
        """Get the string representation of a Results.

        :param int results_index: the index of the Results to get the string.

        :returns: a string representing the Results.

        """
        if results_index < len(self.results_list):
            return str(self.results_list[results_index])

    def get_result_str(self, results_index, result_index_list):
        """Get the string representation of a set of Result from a Results.

        :param index results_index: the index of the Results.
        :param list result_index_list: the indexes of the Result to have the string.

        :returns: a string containing the asking Result.

        """
        ret = ""
        if results_index < len(self.results_list):
            for i in result_index_list:
                if i < self.results_list[results_index].nb_results:
                    ret += str(self.results_list[results_index].get_result(i)) + "\n"
            return ret

    def get_result_var_str(self, results_index, result_index_list):
        ret = ""
        if results_index < len(self.results_list):
            for i in result_index_list:
                if i < self.results_list[results_index].nb_results:
                    labels = self.results_list[results_index].get_result(i).labels
                    data = self.results_list[results_index].get_result(i).data
                    for i, label in enumerate(labels):
                        ret += "{} = {}\n".format(label.replace(" ", "_"), data[i])
        return ret

    def save(self, results_index, filename):
        """Save a Results in a file.

        :param int results_index: the index of the Results.
        :param str filename: the name of the file to store the Results in.

        """
        if results_index < len(self.results_list):
            self.results_list[results_index].save(filename)

    def load(self, filename):
        """Load a Results from a file.

        :param str filename: the name of the file to load the Results from.

        """
        fp = open(self.result_dir + "/" + filename, "r")
        results_dict = json.loads(fp.read())
        self.results_list.append(Results(**results_dict))

    def get_results_from_id_name(self, id_name):
        """Get a Results from its identification name.

        :param str id_name: the identification name of the Results.

        :returns: a Results with a matching identification name.

        """
        for results in self.results_list:
            if results.id_name == id_name:
                return results

    def get_results_index_from_id_name(self, id_name):
        """Get the Results index from its identification name.

        :param str id_name: the identification name of the Results.

        :returns: an integer which is the index of the Results in the list.

        """
        results = self.get_results_from_id_name(id_name)
        return self.results_list.index(results)
