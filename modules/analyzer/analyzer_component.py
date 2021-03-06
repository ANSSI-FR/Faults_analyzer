from ..bin_utils import s2u

from .arg_init import init_arg
from .fault import Fault

class AnalyzerComponent():
    def __init__(self, **kwargs):
        self.df = init_arg("dataframe", kwargs)
        self.default_values = init_arg("default_values", kwargs)
        self.values_type = [type(v) for v in self.default_values]
        self.obs = init_arg("obs_names", kwargs)
        self.to_test = init_arg("to_test", kwargs)
        self.reboot_name = init_arg("reboot_name", kwargs)
        self.log_name = init_arg("log_name", kwargs)
        self.log_sep = init_arg("log_separator", kwargs)
        self.log_begin = init_arg("log_flag_begin", kwargs)
        self.log_end = init_arg("log_flag_end", kwargs)
        self.nb_bits = init_arg("nb_bits", kwargs)
        self.data_format = "0x{:0" + str(int(self.nb_bits/4)) + "x}"
        if "nb_operations" in kwargs:
            self.nb_operations = init_arg("nb_operations", kwargs)
        else:
            self.nb_operations = len(self.df.index)
        if "result_base" in kwargs:
            base = init_arg("result_base", kwargs)
        else:
            base = 10
        # If only one base is given we assume all results are displayed in the
        # same base
        if type(base) == int:
            self.result_base = [base]*len(self.obs)
        else:
            self.result_base = base
        self.done_name = None
        if "done_name" in kwargs:
            self.done_name = init_arg("done_name", kwargs)

    def get_faults(self, ope):
        faulted_obs = []
        log = ope[self.log_name]
        log = log.split(self.log_sep)
        log = log[1:-1]
        log_values = []
        for v, v_type, base in zip(log, self.values_type, self.result_base):
            # int values are converted as unsigned values considering the
            # number of bits
            if v_type == int:
                log_values.append(s2u(int(v, base), self.nb_bits))
            else:
                log_values.append(v)

        # We check for fault
        for i, (lv, dv) in enumerate(zip(log_values, self.default_values)):
            if self.to_test[i]:
                if lv != dv:
                    faulted_obs.append(Fault(i,lv))

        return faulted_obs
