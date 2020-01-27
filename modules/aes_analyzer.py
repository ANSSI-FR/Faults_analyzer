from .analyzer import Analyzer
from .bin_utils import int2byte_tab, get_diff
from .utils import norm_percent, format_table

DIAGONALS = [[0,7,10,13],[1,4,11,14],[2,5,8,15],[3,6,9,12]]
"""The indexes of the diagonals of an AES state."""
AES_BLOCK_BIT_SIZE = 128
"""The size in bits of an AES block."""
AES_BLOCK_BYTE_SIZE = AES_BLOCK_BIT_SIZE//8
"""The size in bytes of an AES block."""

def test_diag_fully_faulted(aes_tab):
    """Test if diagonals of an AES state are fully faulted.

    :param list aes_tab: the AES state to test.

    :returns: the diagonals that are fully faulted as a boolean list.
    :rtype: list

    """
    diag_faulted = []
    for diag in DIAGONALS:
        is_faulted = True
        for i in diag:
            is_faulted = is_faulted and aes_tab[i]
        diag_faulted.append(is_faulted)
    return diag_faulted

def get_nb_val(tab, value):
    """Get the number of a value in a list.

    :param list tab: the list to check the number of value in.
    :param value: the value to look for.

    :returns: the number of time the value is in the list.
    :rtype: int

    """
    nb_val = 0
    for v in tab:
        if v == value:
            nb_val += 1
    return nb_val

def get_aes_nb_fully_faulted_diag(faulted_value, default_value):
    """Get the number of fully faulted diagonals of a faulted AES state compared to its expected value.

    :param int faulted_value: the faulted state of the AES.
    :param int default_value: the expected state of the AES.

    :returns: the number of diagonals fully faulted in the faulted AES state.
    :rtype: int

    """
    nb_faulted_diag = 0
    faulted_value = int2byte_tab(faulted_value)
    default_value = int2byte_tab(default_value)
    if len(faulted_value) == len(default_value):
        diff = get_diff(faulted_value, default_value)
        diag_faulted = test_diag_fully_faulted(diff)
        nb_faulted_diag = get_nb_val(diag_faulted, True)
    return nb_faulted_diag

def get_nb_faulted_bytes(faulted_value, default_value):
    """Get the number of faulted bytes of a faulted AES state.

    :param int faulted_value: the faulted state of the AES.
    :param int default_value: the expected state of the AES.

    :returns: the number of faulted bytes in the AES state.
    :rtype: int

    """
    nb_faulted_bytes = 0
    faulted_value = int2byte_tab(faulted_value)
    default_value = int2byte_tab(default_value)
    if len(faulted_value) == len(default_value):
        diff = get_diff(faulted_value, default_value)
        for d in diff:
            if d == True:
                nb_faulted_bytes += 1
    return nb_faulted_bytes

class AESAnalyzer(Analyzer):
    """A class for doing the analysis of a fault campaign focused on AES fault characteristics.
    """
    def __init__(self, **kwargs):
        """Constructor of the class."""
        super().__init__(**kwargs)
        self.nb_faulted_diag_dist = [0]*5
        """The distribution of the number of faulted diagonals."""
        self.truncated_ciphers = 0
        """The number of ciphers with a size different from the AES state size."""
        self.nb_faulted_bytes_per_delay = [[0]*(AES_BLOCK_BYTE_SIZE+1) for i in range(len(self.delays))]
        """The distribution of the number of faulted bytes for each tested delays."""
        self.nb_faulted_diag_per_delay = [[0]*(AES_BLOCK_BYTE_SIZE//4+1) for i in range(len(self.delays))]
        """The distribution of the number of faulted diagonals for each tested delays."""
        self.one_fully_faulted_diag_values = []
        """The faulted values with only one fully faulted diagonal."""
        self.one_fully_faulted_diag_values_diff = []
        """The differential of the faulted values with only one fully faulted diagonal."""

    def update_fault_models(self, faulted):
        """Update the fault models. Add the AES oriented analysis.

        :param list faulted: the faulted obs and the faulted value.

        """
        super().update_fault_models(faulted)
        self.aes_analysis(faulted)

    def aes_analysis(self, faulted):
        """Realize the AES oriented analysis.

        :param list faulted: the faulted obs and the faulted value.

        """
        faulted_obs = faulted[0]
        faulted_value = faulted[1]
        default_value = self.default_values[faulted_obs]
        if len(int2byte_tab(faulted_value)) == AES_BLOCK_BYTE_SIZE:
            self.update_faulted_diag(faulted_value, default_value)
        else:
            self.truncated_ciphers += 1

    def update_faulted_diag(self, faulted_value, default_value):
        """Update the number of faulted diagonals distribution.

        :param int faulted_value: the faulted AES state.
        :param int default_value: the expected AES state.

        """
        nb_faulted_diag = get_aes_nb_fully_faulted_diag(faulted_value, default_value)
        self.nb_faulted_diag_dist[nb_faulted_diag] += 1

    def get_aes_statistics(self):
        """Format the AES general statistics result.

        :returns: the AES general statistics result.
        :rtype: dict

        """
        ret = {
            "title": "AES statistics",
            "labels": ["Information", "Value", "Percentage"],
            "data": [["Number of truncated ciphers","Percentage of truncated ciphers (%)"],
                     [self.truncated_ciphers,float(self.truncated_ciphers)/float(self.nb_faults)*100]]
        }
        return ret

    def get_nb_faulted_diag_dist_result(self):
        """Format the number of faulted diagonals distribution result.

        :returns: the number of faulted diagonals distribution result.
        :rtype: dict

        """
        ret = {
            "title": "Number of faulted diagonals distribution",
            "labels": ["Number of faulted diagonals", "Occurrence", "Percentage (%)"],
            "data": [[0,1,2,3,4],
                     self.nb_faulted_diag_dist,
                     norm_percent(self.nb_faulted_diag_dist)]
        }
        return ret

    def get_nb_faulted_bytes_per_delay_sorted_per_bytes(self):
        """Sort the number of faulted bytes per delay as the number of time a delay faulted the number of bytes.

        :returns: the number of time a delay led to a specific number of faulted bytes.
        :rtype: list

        """
        ret = [[] for i in range(AES_BLOCK_BYTE_SIZE)]
        for i in range(AES_BLOCK_BYTE_SIZE):
            for d in range(len(self.delays)):
                ret[i].append(self.nb_faulted_bytes_per_delay[d][i])
        return ret

    def get_nb_faulted_diag_per_delay_sorted_per_bytes(self):
        """Sort the number of faulted delays per delay as the number of time a delay faulted the number of diagonals.

        :returns: the number of time a delay led to a specific number of faulted diagonals.
        :rtype: list

        """
        ret = [[] for i in range(AES_BLOCK_BYTE_SIZE//4+1)]
        for i in range(AES_BLOCK_BYTE_SIZE//4+1):
            for d in range(len(self.delays)):
                ret[i].append(self.nb_faulted_diag_per_delay[d][i])
        return ret

    def get_nb_faulted_bytes_result(self):
        """Format the number of faulted bytes per delay result.

        :returns: the number of faulted bytes per delay result.
        :rtype: dict

        """
        ret = {
            "title": "Number of faulted bytes per delay",
            "labels": ["Delay (s)"] + ["{}".format(i+1) for i in range(AES_BLOCK_BYTE_SIZE)],
            "data": [self.delays] + self.get_nb_faulted_bytes_per_delay_sorted_per_bytes()
        }
        return ret

    def get_nb_faulted_diag_result(self):
        """Format the number of faulted diagonals per delay result.

        :returns: the number of faulted diagonals result.
        :rtype: dict

        """
        ret = {
            "title": "Number of faulted diagonals per delay",
            "labels": ["Delay (s)", "0", "1", "2", "3", "4"],
            "data": [[float(d) for d in self.delays]] + self.get_nb_faulted_diag_per_delay_sorted_per_bytes()
        }
        return ret

    def get_results(self):
        """Create the results list.

        :returns: the results of the analysis.
        :rtype: list

        """
        results = super().get_results()
        results.append(self.get_aes_statistics())
        results.append(self.get_nb_faulted_diag_dist_result())
        results.append(self.get_nb_faulted_bytes_result())
        results.append(self.get_nb_faulted_diag_result())
        results.append(self.get_1_fully_faulted_diag_values_result())
        return results

    def update_nb_faulted_bytes_per_delay(self, faulted_value, default_value, ope):
        """Update the number of faulted bytes per delay.

        :param int faulted_value: the faulted AES state.
        :param int default_value: the expected AES state.

        """
        delay = ope[self.delay_name]
        nb_faulted_bytes = get_nb_faulted_bytes(faulted_value, default_value)
        delay_index = self.delays.index(delay)
        self.nb_faulted_bytes_per_delay[delay_index][nb_faulted_bytes] += 1

    def update_nb_faulted_diag_per_delay(self, faulted_value, default_value, ope):
        delay = ope[self.delay_name]
        nb_faulted_diag = get_aes_nb_fully_faulted_diag(faulted_value, default_value)
        delay_index = self.delays.index(delay)
        self.nb_faulted_diag_per_delay[delay_index][nb_faulted_diag] += 1

    def update_faulted_values_stats(self, ope):
        ope_faulted_obs = self.get_faulted_obs(ope)
        if not ope_faulted_obs is None:
            for faulted in ope_faulted_obs:
                default_value = self.default_values[faulted[0]]
                self.update_nb_faulted_bytes_per_delay(faulted[1], default_value, ope)
                self.update_nb_faulted_diag_per_delay(faulted[1], default_value, ope)
                self.update_1_fully_faulted_diag_values(faulted[1], default_value)

    def get_1_fully_faulted_diag_values_result(self):
        ret = {
            "title": "One fully faulted diagonal values",
            "labels": ["Faulted values", "Faulted values differential"],
            "data": [format_table(self.one_fully_faulted_diag_values, self.data_format),
                     format_table(self.one_fully_faulted_diag_values_diff, self.data_format)]
        }
        return ret

    def update_1_fully_faulted_diag_values(self, faulted_value, default_value):
        nb_faulted_diag = get_aes_nb_fully_faulted_diag(faulted_value, default_value)
        if nb_faulted_diag == 1:
            self.one_fully_faulted_diag_values.append(faulted_value)
            self.one_fully_faulted_diag_values_diff.append(faulted_value ^ default_value)

    def is_faulted_analysis(self, ope):
        super().is_faulted_analysis(ope)
        self.update_faulted_values_stats(ope)
