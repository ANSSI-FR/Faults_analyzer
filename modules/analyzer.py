from .bin_utils import *
from .utils import print_progress_bar, norm_percent, format_table

class Analyzer():
    """
    Class doing the analysis of fault attacks results.
    """

    fault_models = ["Fault model unknown",
                    "Bit set",
                    "Bit reset",
                    "Bit flip",
                    "Other obs value",
                    "Other obs complementary value",
                    "Add with other obs",
                    "And with other obs",
                    "Or with other obs",
                    "Xor with other obs",
                    "Sub with other obs",
                    "Other obs value after execution",
                    "Executed instruction",
                    "Or with two other obs"]

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
                 base_resp=10,
                 progress=False):
        """Constructor of the class. Initialize all the results lists and parameters.

        :param dataframe: the dataframe object from the pandas library containing the results of the experiments

        :param obs_names: the name of the observed items as named in the dataframe

        :param default_values: the default values of the observed

        :param to_test: a boolean array determining if an observed must be tested or not during the analysis

        :param power_name: the key name for accessing the power value in the dataframe lines

        :param delay_name: the key name for accessing the delay value in the dataframe lines

        :param done_name: the key name for accessing if a line has been done or not

        :param fault_name: the key name for checking if a line has been faulted or not

        :param reboot_name: the key name for checking if a line has made a system reboot or not

        :param log_name: the key name for getting the log in the dataframe line

        :param log_separator: the symbol used for splitting the values in the log

        :param data_format: the format string for displaying integer values (for example: 0x{:08x})

        :param nb_bits: the number of bits the integers must be considered encoded on

        :param executed_instructions: a list containing the integer value of the executed instructions

        :param int base_resp: the base of the response (default=10)

        :param progress: a flag that set if the progress bar must be printed

        """

        # Analysis parameters initialization
        self.obs_names = obs_names
        self.nb_obs = len(self.obs_names)
        self.default_values = default_values
        self.to_test = to_test
        self.done_name = done_name
        self.fault_name = fault_name
        self.reboot_name = reboot_name
        self.log_name = log_name
        self.log_separator = log_separator
        self.power_name = power_name
        self.delay_name = delay_name
        self.data_format = data_format
        self.nb_bits = nb_bits
        self.df = dataframe
        self.executed_instructions = executed_instructions
        self.progress = progress
        self.base_resp = base_resp

        # Extract all the power and delay values from the dataframe
        self.powers = list(self.df[self.power_name].unique())
        self.delays = list(self.df[self.delay_name].unique())

        # General information about the experiment initialization
        self.values_after_execution = []
        self.values_after_current_execution = []
        self.nb_done = 0
        self.nb_to_do = len(self.df.index)
        self.nb_reboots = 0
        self.nb_faults = 0
        self.nb_faulted_obs = 0
        self.reboot_powers = [0]*len(self.powers)
        self.reboot_delays = [0]*len(self.delays)
        self.fault_powers = [0]*len(self.powers)
        self.fault_delays = [0]*len(self.delays)
        self.faulted_obs = [0]*self.nb_obs
        self.faulted_values = []
        self.faulted_values_occurrence = []
        self.analysis_done = False

        # Fault models initialization
        self.fault_model_unknown = 0
        self.bit_set = 0
        self.bit_reset = 0
        self.bit_flip = 0
        self.other_obs_value = 0
        self.other_obs_complementary_value = 0
        self.add_with_other_obs = 0
        self.and_with_other_obs = 0
        self.or_with_other_obs = 0
        self.xor_with_other_obs = 0
        self.sub_with_other_obs = 0
        self.other_obs_value_after_execution = 0
        self.nb_responses_bad_format = 0
        self.executed_instruction = 0
        self.or_with_two_other_obs = 0

        # Information about the fault models initialization
        self.other_obs_value_after_execution_origin_occurrence = [0]*self.nb_obs
        self.other_obs_value_origin_occurrence = [0]*self.nb_obs
        self.other_obs_complementary_value_origin_occurrence = [0]*self.nb_obs
        self.add_with_other_obs_origin_occurrence = [0]*self.nb_obs
        self.and_with_other_obs_origin_occurrence = [0]*self.nb_obs
        self.or_with_other_obs_origin_occurrence = [0]*self.nb_obs
        self.xor_with_other_obs_origin_occurrence = [0]*self.nb_obs
        self.sub_with_other_obs_origin_occurrence = [0]*self.nb_obs

        self.other_obs_value_after_execution_destination = [0]*self.nb_obs
        self.other_obs_value_destination = [0]*self.nb_obs
        self.other_obs_complementary_value_destination = [0]*self.nb_obs
        self.add_with_other_obs_destination = [0]*self.nb_obs
        self.and_with_other_obs_destination = [0]*self.nb_obs
        self.or_with_other_obs_destination = [0]*self.nb_obs
        self.xor_with_other_obs_destination = [0]*self.nb_obs
        self.sub_with_other_obs_destination = [0]*self.nb_obs

        self.fault_model_unknown_destination = [0]*self.nb_obs
        self.bit_set_destination = [0]*self.nb_obs
        self.bit_reset_destination = [0]*self.nb_obs
        self.bit_flip_destination = [0]*self.nb_obs

        self.fault_model_unknown_values = []

    def get_faulted_obs(self, ope):
        """Determine the index of the faulted observed and the faulted value it has.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: a list containing the index of the faulted obs and the faulted value

        """
        ret = []
        values = self.get_values_from_log(ope)
        if not values is None:
            for i in range(len(values)):
                if self.to_test[i]:
                    if values[i] != self.default_values[i]:
                        ret.append([i, values[i]])
        return ret

    def update_result_occurrence(self, ope, values, result, param):
        """Update a result list occurrence for corresponding values. The values occurrence are stored in the result list. By analyzing the operation, the occurrence of the corresponding values will be updated.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :param values: list of the values that are analyzed.

        :param result: occurrence of apparition of the corresponding values. A value and its occurrence share the same index in result and values lists.

        :param param: the key name of the parameter to be updated.

        """
        param_value = ope[param]
        try:
            value_index = values.index(param_value)
            result[value_index] += 1
        except:
            print("Error in parameter parsing: ignoring the operation")
        
    def is_done(self, ope):
        """Check if the operation is set as done.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        return ope[self.done_name]

    def is_response_bad_formated(self, ope):
        """Check if the response of receive during the operation is bad formated. This means the number of values from the log is different from the number of observed.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: True if the response is bad formated, False in the other case
        """
        if self.is_done(ope):
            values = self.get_values_from_log(ope)
            if not len(values) is self.nb_obs:
                return True
            return False

    def is_faulted(self, ope):
        """Check if the operation has at least one observed faulted.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: True if one observed in the operation is faulted, False in the other case

        """
        if self.is_done(ope):
            values = self.get_values_from_log(ope)
            for i in range(self.nb_obs):
                if self.to_test[i]:
                    if s2u(values[i], self.nb_bits) != s2u(self.default_values[i], self.nb_bits):
                        return True
        return False

    def is_set_as_faulted(self, ope):
        """Check if the operation is set as faulted.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: the value of the information about the fault stored in the operation, False if the operation is not done
        """
        if self.is_done(ope):
            return ope[self.fault_name]
        return False

    def is_set_as_reboot(self, ope):
        """Check if the operation is set as a reboot.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: the value of the information about the reboot stored in the operation, False if the operation is not done

        """
        if self.is_done(ope):
            return ope[self.reboot_name]
        return False

    def get_values_from_log(self, ope):
        """Check the formatting of the log and extract the values of the observed from it.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: a list containing the unsigned representation of the values from the log of the operation, the list is empty if the values cannot be interpreted as integers

        :TODO: make flags as parameters

        """
        try:
            log = str(ope[self.log_name])
            log = log.split(self.log_separator)
            if log[0] == "FlagBegin":
                log = log[1:]
            if log[-1] == "FlagEnd":
                log = log[:-1]
            print(log)
            values = [s2u(int(v, self.base_resp),self.nb_bits) for v in log]
            return values
        except Exception as e:
            return []

    def get_golden_values_after_execution(self, ope):
        """Extract the values of the observed if the operation is neither set as a reboot nor set as faulted. This should correspond to the expected values of the observed after a normal execution. However, in some cases, these values can be different from an operation to another due to reboot and uncontrolled observed. Take care with this function during the analysis.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        :returns: the values of the observed as stored in the log of the operation

        """
        if not self.is_set_as_reboot(ope) and not self.is_set_as_faulted(ope):
            return self.get_values_from_log(ope)


    def is_done_analysis(self, ope):
        """Do the analysis routine in the case the operation is done.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment

        """
        self.nb_done += 1
        self.values_after_current_execution = self.get_values_from_log(ope)
        if self.values_after_execution == None:
            self.values_after_execution = self.get_golden_values_after_execution(ope)
        elif len(self.values_after_execution) == 0:
            self.values_after_execution = self.get_golden_values_after_execution(ope)

    def is_reboot_analysis(self, ope):
        """Do the analysis routine in the case the operation led to a reboot of the system.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        self.nb_reboots += 1
        self.update_result_occurrence(ope, self.powers, self.reboot_powers, self.power_name)
        self.update_result_occurrence(ope, self.delays, self.reboot_delays, self.delay_name)

    def update_faulted_obs(self, faulted_obs):
        """Update the list of the faulted observed.

        :param faulted_obs: the index of the faulted observed.

        """
        self.faulted_obs[faulted_obs] += 1

    def update_faulted_values(self, faulted_value, ope):
        """Update the faulted values and their occurrence. If the faulted_value is not in the faulted_values list, it will be added.

        :param faulted_value: the value of the faulted observed.
        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        if not faulted_value in self.faulted_values:
            self.faulted_values.append(faulted_value)
            self.faulted_values_occurrence.append(1)
        else:
            for i, v in enumerate(self.faulted_values):
                if v == faulted_value:
                    self.faulted_values_occurrence[i] += 1

    def update_bit_set(self, faulted_obs, faulted_value):
        """Update the bit set fault model. This function only consider a bit set on the WHOLE word.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the bit set fault model, False in the other case.

        """
        max_value = (1 << self.nb_bits) - 1
        if s2u(faulted_value, self.nb_bits) == max_value:
            self.bit_set += 1
            self.bit_set_destination[faulted_obs] += 1
            return True
        return False

    def update_bit_reset(self, faulted_obs, faulted_value):
        """Update the bit reset fault model. This function only consider a bit reset on the WHOLE word.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the bit reset fault model, False in the other case.

        """
        if s2u(faulted_value, self.nb_bits) == 0:
            self.bit_reset += 1
            self.bit_reset_destination[faulted_obs] += 1
            return True
        return False

    def update_bit_flip(self, faulted_obs, faulted_value):
        """Update the bit flip fault model. This function only consider a bit flip on the WHOLE world.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the bit flip fault model, False in the other case.

        """
        if s2u(faulted_value, self.nb_bits) == a2_comp(self.default_values[faulted_obs], self.nb_bits):
            self.bit_flip += 1
            self.bit_flip_destination[faulted_obs] += 1
            return True
        return False

    def update_other_obs_value(self, faulted_obs, faulted_value):
        """Update the other observed value fault model considering the initial state.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if not i is faulted_obs:
                if s2u(faulted_value, self.nb_bits) == s2u(int(val), self.nb_bits):
                    self.other_obs_value += 1
                    self.other_obs_value_origin_occurrence[i] += 1
                    self.other_obs_value_destination[faulted_obs] += 1
                    return True
        return False

    def update_other_obs_value_after_execution(self, faulted_obs, faulted_value):
        """Update the other observed value fault model considering the values of the observed after the execution of the program.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the other observed value after execution fault model, False in the other case.

        """
        for i, val in enumerate(self.values_after_current_execution):
            if not i is faulted_obs:
                if s2u(faulted_value, self.nb_bits) == s2u(int(val), self.nb_bits):
                    self.other_obs_value_after_execution += 1
                    self.other_obs_value_after_execution_origin_occurrence[i] += 1
                    self.other_obs_value_after_execution_destination[faulted_obs] += 1
                    return True
        return False
    
    def update_other_obs_complementary_value(self, faulted_obs, faulted_value):
        """Update the other observed complementary value fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with the other observed complementary value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if not i is faulted_obs:
                if s2u(faulted_value, self.nb_bits) == a2_comp(val, self.nb_bits):
                    self.other_obs_complementary_value += 1
                    self.other_obs_complementary_value_origin_occurrence[i] += 1
                    self.other_obs_complementary_value_destination[faulted_obs] += 1
                    return True
        return False

    def update_add_with_other_obs(self, faulted_obs, faulted_value):
        """Update the add with other observed fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with add with other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] + val, self.nb_bits):
                if i != faulted_obs:
                    self.add_with_other_obs += 1
                    self.add_with_other_obs_origin_occurrence[i] += 1
                    self.add_with_other_obs_destination[faulted_obs] += 1
                    return True
        return False

    def update_and_with_other_obs(self, faulted_obs, faulted_value):
        """Update the and with other observed fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with and with other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] & val, self.nb_bits):
                if i != faulted_obs:
                    self.and_with_other_obs += 1
                    self.and_with_other_obs_origin_occurrence[i] += 1
                    self.and_with_other_obs_destination[faulted_obs] += 1
                    return True
        return False

    def update_or_with_two_other_obs(self, faulted_obs, faulted_value):
        """Update the or with two other observed fault model considering the initial observed values.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with or with two other observed value fault model, False in the other case.

        """
        for i, val1 in enumerate(self.default_values):
            for j, val2 in enumerate(self.default_values):
                if s2u(faulted_value, self.nb_bits) == (s2u(val1, self.nb_bits) | s2u(val2, self.nb_bits)):
                    if (i != faulted_obs) and (j != faulted_obs):
                        self.or_with_two_other_obs += 1
                        return True
        return False

    def update_or_with_other_obs(self, faulted_obs, faulted_value):
        """Update the or with other observed fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with or with other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] | val, self.nb_bits):
                if i != faulted_obs:
                    self.or_with_other_obs += 1
                    self.or_with_other_obs_origin_occurrence[i] += 1
                    self.or_with_other_obs_destination[faulted_obs] += 1
                    return True
        return False
    
    def update_xor_with_other_obs(self, faulted_obs, faulted_value):
        """Update the xor with other observed fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with xor with other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] ^ val, self.nb_bits):
                if i != faulted_obs:
                    self.xor_with_other_obs += 1
                    self.xor_with_other_obs_origin_occurrence[i] += 1
                    self.xor_with_other_obs_destination[faulted_obs] += 1
                    return True
        return False
    
    def update_sub_with_other_obs(self, faulted_obs, faulted_value):
        """Update the sub with other observed fault model considering the initial values of the observed.

        :param faulted_obs: the index of the faulted observed element.
        :param faulted_value: the value of the faulted observed.

        :return: True if the fault match with sub with other observed value fault model, False in the other case.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] - val, self.nb_bits):
                if i != faulted_obs:
                    self.sub_with_other_obs += 1
                    self.sub_with_other_obs_origin_occurrence[i] += 1
                    self.sub_with_other_obs_destination[faulted_obs] += 1
                    return True
        return False

    def update_executed_instruction(self, faulted_value):
        """Update the executed instruction fault model.

        :param faulted_value: the value of the faulted observed.

        :return: True if the fault value is in the executed instructions, False in the other case.

        """
        if s2u(faulted_value, self.nb_bits) in self.executed_instructions:
            self.executed_instruction += 1
            return True
        return False

    def update_fault_models(self, faulted):
        """Update the fault models. This function is not satisfactory as it will stop once a fault explain the faulted value. However, several fault models might explain it. But removing the fault_model_known test will biased the statistics has we would have more fault models than faults...

        :param faulted: a list containing the faulted observed index and the faulted value.

        """
        faulted_obs = faulted[0]
        faulted_value = faulted[1]
        fault_model_known = False
        fault_model_known |= self.update_bit_set(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_bit_reset(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_bit_flip(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_other_obs_value(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_other_obs_complementary_value(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_or_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_add_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_and_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_xor_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_sub_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_other_obs_value_after_execution(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_executed_instruction(faulted_value)
        if not fault_model_known:
            fault_model_known |= self.update_or_with_two_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            self.fault_model_unknown += 1
            self.fault_model_unknown_destination[faulted_obs] += 1
            if not faulted_value in self.fault_model_unknown_values:
                self.fault_model_unknown_values.append(faulted_value)

    def update_faulted_obs_and_values(self, ope):
        """Update the number of faulted observed, the faulted observed, the faulted values and the fault models.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        ope_faulted_obs = self.get_faulted_obs(ope)
        if not ope_faulted_obs is None:
            self.nb_faulted_obs += len(ope_faulted_obs)
            for faulted in ope_faulted_obs:
                self.update_faulted_obs(faulted[0])
                self.update_faulted_values(faulted[1], ope)
                self.update_fault_models(faulted)

    def is_faulted_analysis(self, ope):
        """Do the analysis routine in the case the operation has been faulted.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        self.nb_faults += 1
        self.update_result_occurrence(ope, self.powers, self.fault_powers, self.power_name)
        self.update_result_occurrence(ope, self.delays, self.fault_delays, self.delay_name)
        self.update_faulted_obs_and_values(ope)

    def is_response_bad_formated_analysis(self, ope):
        """Do the analysis routine in the case the operation has a bad formated response.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        self.nb_responses_bad_format += 1

    def analysis(self, ope):
        """Run the analysis on a given operation.

        :param ope: the operation, which is a line from the dataframe, containing all the information about this step of the experiment.

        """
        if self.is_done(ope):
            self.is_done_analysis(ope)

        if self.is_set_as_reboot(ope):
            self.is_reboot_analysis(ope)

        if not self.is_response_bad_formated(ope):
            if self.is_faulted(ope):
                self.is_faulted_analysis(ope)
        else:
            self.is_response_bad_formated_analysis(ope)

    def set_fault_models_occurrence(self):
        """Create the fault model occurrence list.

        """
        self.fault_models_occurrence = [self.fault_model_unknown,
                                        self.bit_set,
                                        self.bit_reset,
                                        self.bit_flip,
                                        self.other_obs_value,
                                        self.other_obs_complementary_value,
                                        self.add_with_other_obs,
                                        self.and_with_other_obs,
                                        self.or_with_other_obs,
                                        self.xor_with_other_obs,
                                        self.sub_with_other_obs,
                                        self.other_obs_value_after_execution,
                                        self.executed_instruction,
                                        self.or_with_two_other_obs]

    def ope_loop_analysis(self):
        """Main loop of the analysis. Go through every operation and launch the analysis.

        """
        i=0
        for _, ope in self.df.iterrows():
            self.analysis(ope)
            if self.progress:
                i += 1
                print_progress_bar(i, self.nb_to_do, prefix = "Analysis progress:", suffix = "Complete", length=50)

    def run_analysis(self):
        """Run the analysis. This function must be called before getting any result.

        """
        if self.analysis_done == False:
            self.ope_loop_analysis()
            self.set_fault_models_occurrence()
            self.analysis_done = True
        else:
            print("Analysis already done, no need to do it again.")

    def check_analysis_done(self):
        """Check if the analysis has been done. If not, do it.

        """
        if self.analysis_done == False:
            self.run_analysis()

    def get_nb_faulted_obs(self):
        """:return: the number of faulted observed.

        """
        self.check_analysis_done()
        return self.nb_faulted_obs

    def get_nb_to_do(self):
        """:return: the number of operations to do.

        """
        self.check_analysis_done()
        return self.nb_to_do

    def get_powers(self):
        """:return: the list of the voltage powers.

        """
        self.check_analysis_done()
        return self.powers

    def get_delays(self):
        """:return: the list of the delays.

        """
        self.check_analysis_done()
        return self.delays
            
    def get_obs_names(self):
        """:return: a list containing the names of the observed.

        """
        self.check_analysis_done()
        return self.obs_names
            
    def get_faulted_values(self):
        """:return: a list containing the faulted values.

        :TODO: Merge the faulted values and their occurrence.

        """
        self.check_analysis_done()
        return self.faulted_values

    def get_faulted_values_occurrence(self):
        """:return: a list containing the occurrence of the faulted values.

        :TODO: Merge the faulted values and their occurrence.

        """
        self.check_analysis_done()
        return self.faulted_values_occurrence
            
    def get_faulted_obs_occurrence(self):
        """:return: a list containing the faulted observed occurrence.

        """
        self.check_analysis_done()
        return self.faulted_obs
            
    def get_fault_delays(self):
        """:return: a list containing the delays involved in faults occurrence.
        
        """
        self.check_analysis_done()
        return self.fault_delays
            
    def get_fault_powers(self):
        """:return: a list containing the voltage power involved in faults occurrence.

        """
        self.check_analysis_done()
        return self.fault_powers
            
    def get_nb_faults(self):
        """:return: the number of faults.

        """
        self.check_analysis_done()
        return self.nb_faults
            
    def get_reboot_delays(self):
        """:return: a list containing the delays involved in reboots occurrence.

        """
        self.check_analysis_done()
        return self.reboot_delays
            
    def get_reboot_powers(self):
        """:return: a list containing the voltage powers involved in reboots occurrence.

        """
        self.check_analysis_done()
        return self.reboot_powers
            
    def get_nb_reboots(self):
        """:return: the number of reboots.

        """
        self.check_analysis_done()
        return self.nb_reboots
        
    def get_values_after_execution(self):
        """:return: a list containing the values after execution. These values correspond to one non faulted and non reboot operation but might change between operations.

        """
        self.check_analysis_done()
        return self.values_after_execution

    def get_nb_done(self):
        """:return: the number of done operations.

        """
        self.check_analysis_done()
        return self.nb_done

    def get_fault_models(self):
        """:return: a list containing the fault models and their corresponding occurrence.

        """
        self.check_analysis_done()
        ret = [self.fault_models]
        ret.append(norm_percent(self.fault_models_occurrence))
        return ret

    def get_nb_responses_bad_format(self):
        """:return: the number of responses bad formated.

        """
        self.check_analysis_done()
        return self.nb_responses_bad_format

    def get_general_stats(self):
        """:return: a list containing the general statistics of the experiments and their values.

        """
        self.check_analysis_done()
        ret = [
            ["Number of operations to do",
             "Number of operation done",
             "Percentage done (%)",
             "Number of reboots",
             "Percentage of reboots (%)",
             "Number of responses bad formated",
             "Percentage of responses bad formated (%)",
             "Number of faults",
             "Percentage of faults (%)",
             "Number of faulted obs"],
            [self.nb_to_do,
             self.nb_done,
             100*self.nb_done/float(self.nb_to_do),
             self.nb_reboots,
             100*self.nb_reboots/float(self.nb_done),
             self.nb_responses_bad_format,
             100*self.nb_responses_bad_format/float(self.nb_done),
             self.nb_faults,
             100*self.nb_faults/float(self.nb_done),
             self.nb_faulted_obs]
        ]
        if self.nb_faults != 0:
            ret[0].append("Average faulted obs per fault")
            ret[1].append(self.nb_faulted_obs/float(self.nb_faults))
        return ret

    def get_analysis_results(self):
        """:return: a dictionary containing the analysis result.

        """
        self.check_analysis_done()
        ret = {
            "nb_to_do": self.nb_to_do,
            "nb_done": self.nb_done,
            "values_after_execution": self.values_after_execution,
            "nb_reboots": self.nb_reboots,
            "reboot_powers": self.reboot_powers,
            "reboot_delays": self.reboot_delays,
            "nb_faults": self.nb_faults,
            "fault_powers": self.fault_powers,
            "fault_delays": self.fault_delays,
            "faulted_obs": self.faulted_obs,
            "faulted_values_occurrence": self.faulted_values_occurrence,
            "faulted_values": self.faulted_values,
            "obs_names": self.obs_names,
            "powers": self.powers,
            "delays": self.delays,
            "fault_models": self.get_fault_models()
        }
        return ret

    def get_other_obs_value_after_execution_origin_occurrence(self):
        """:return: a list containing the occurrence of faulted value origin in the case of the other observed value after execution faulted model.

        """
        self.check_analysis_done()
        return self.other_obs_value_after_execution_origin_occurrence

    def get_other_obs_values_after_execution_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the other observed value after execution fault model.

        """
        ret = [
            {
                "title": "Origin of the faulted value after execution",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_value_after_execution_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for other obs value after execution",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_value_after_execution_destination)]
            }
        ]
        return ret

    def get_other_obs_values_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the faulted value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_value_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for other obs value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_value_destination)]
            }
        ]
        return ret

    def get_other_obs_complementary_value_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the other observed complementary value fault model.

        """
        ret = [
            {
                "title": "Origin of the faulted complementary value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_complementary_value_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for other obs complementary value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.other_obs_complementary_value_destination)]
            }
        ]
        return ret

    def get_add_with_other_obs_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the add with other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the added value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.add_with_other_obs_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for add with other obs",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.add_with_other_obs_destination)]
            }
        ]
        return ret

    def get_and_with_other_obs_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the and with other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the ANDed value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.and_with_other_obs_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for and with other obs",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.and_with_other_obs_destination)]
            }
        ]
        return ret

    def get_or_with_other_obs_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the or with other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the ORed value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.or_with_other_obs_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for or with other obs",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.or_with_other_obs_destination)]
            }
        ]
        return ret

    def get_xor_with_other_obs_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the xor with other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the XORed value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.xor_with_other_obs_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for xor with other obs",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.xor_with_other_obs_destination)]
            }
        ]
        return ret

    def get_sub_with_other_obs_information(self):
        """:return: a list of dictionaries containing the origin of the faulted value occurrence and the faulted destination occurrence in the case of the sub with other observed value fault model.

        """
        ret = [
            {
                "title": "Origin of the subtracted value",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.sub_with_other_obs_origin_occurrence)]
            },
            {
                "title": "Destination occurrence for sub with other obs",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.sub_with_other_obs_destination)]
            }
        ]
        return ret

    def get_bit_set_information(self):
        """:return: a list of dictionaries containing the faulted destination occurrence in the case of the bit set fault model.

        """
        ret = [
            {
                "title": "Destination occurrence for bit set",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.bit_set_destination)]
            }
        ]
        return ret

    def get_bit_reset_information(self):
        """:return: a list of dictionaries containing the faulted destination occurrence in the case of the bit reset fault model.

        """
        ret = [
            {
                "title": "Destination occurrence for bit reset",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.bit_reset_destination)]
            }
        ]
        return ret

    def get_bit_flip_destination(self):
        """:return: a list of dictionaries containing the faulted destination occurrence in the case of the bit flip fault model.

        """
        ret = [
            {
                "title": "Destination occurrence for bit flip",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.bit_flip_destination)]
            }
        ]
        return ret

    def get_fault_model_unknown_information(self):
        """:return: a list of dictionaries containing the faulted destination occurrence and the values in the case of the unknown fault model.

        """
        ret = [
            {
                "title": "Destination occurrence for fault model unknown",
                "labels": ["Observed", "Occurrence (%)"],
                "data": [self.obs_names,
                         norm_percent(self.fault_model_unknown_destination)]
            },
            {
                "title": "Fault model unknown values",
                "labels": ["Values"],
                "data": [format_table(self.fault_model_unknown_values, self.data_format)]
            }
        ]
        return ret

    def get_or_with_two_other_obs_information(self):
        """This function exists be does nothing.

        :return: a list of dictionaries containing NOTHING in the case of the bit or fault model.

        """
        pass

    def get_fault_model_information(self, fault_model):
        """:param fault_model: the fault model, as a string, from which to get the result.

        :return: a list of dictionaries containing the results of the given fault model.

        """
        if fault_model == "Other obs value after execution":
            return self.get_other_obs_values_after_execution_information()
        elif fault_model == "Other obs value":
            return self.get_other_obs_values_information()
        elif fault_model == "Other obs complementary value":
            return self.get_other_obs_complementary_value_information()
        elif fault_model == "Add with other obs":
            return self.get_add_with_other_obs_information()
        elif fault_model == "And with other obs":
            return self.get_and_with_other_obs_information()
        elif fault_model == "Or with other obs":
            return self.get_or_with_other_obs_information()
        elif fault_model == "Xor with other obs":
            return self.get_xor_with_other_obs_information()
        elif fault_model == "Sub with other obs":
            return self.get_sub_with_other_obs_information()
        elif fault_model == "Bit set":
            return self.get_bit_set_information()
        elif fault_model == "Bit reset":
            return self.get_bit_reset_information()
        elif fault_model == "Bit flip":
            return self.get_bit_flip_information()
        elif fault_model == "Fault model unknown":
            return self.get_fault_model_unknown_information()
        elif fault_model == "Or with two other obs":
            return self.get_or_with_two_other_obs_information()
        else:
            print("Failed to get the results for the fault model : {}".format(fault_model))

    def get_fault_model_occurrence(self, fault_model):
        """:param fault_model: the fault model to get the number of occurrence.

        :return: the occurrence of the fault model.

        """
        return self.fault_models_occurrence[self.fault_models.index(fault_model)]

    def add_fault_model_information(self, result):
        """Check over all fault models if they have appear during the experiment. If they do, add the corresponding information to the results list.

        :param result: the result list to update with fault models information.

        :return: the result list updated with fault models information.

        """
        for fault_model in self.fault_models:
            if self.get_fault_model_occurrence(fault_model) > 0:
                fault_model_information = self.get_fault_model_information(fault_model)
                if fault_model_information != None:
                    result += fault_model_information
        return result

    def get_results(self):
        """:return: list of dictionaries containing all the results of the analysis.

        """
        self.check_analysis_done()
        results = [
            {
                "title": "General statistics",
                "labels": ["Statistic", "Value"],
                "data": self.get_general_stats()
            },
            {
                "title": "Effect of the power value",
                "labels": ["Power value (V)", "Fault (%)", "Reboot (%)"],
                "data": [self.powers,
                         norm_percent(self.fault_powers),
                         norm_percent(self.reboot_powers)]
            },
            {
                "title": "Effect of the delay",
                "labels": ["Delays (ns)", "Fault (%)", "Reboot (%)"],
                "data": [self.delays,
                         norm_percent(self.fault_delays),
                         norm_percent(self.reboot_delays)]
            },
            {
                "title": "Observed statistics",
                "labels": ["Observed",
                           "Default value",
                           "Value after execution",
                           "Fault (%)",
                           "Tested"],
                "data": [self.obs_names,
                         format_table(self.default_values, self.data_format),
                         format_table(self.values_after_execution, self.data_format),
                         norm_percent(self.faulted_obs),
                         self.to_test]
            },
            {
                "title": "Faulted values statistics",
                "labels": ["Faulted values", "Occurrence (%)"],
                "data": [format_table(self.faulted_values, self.data_format),
                         norm_percent(self.faulted_values_occurrence)]
            },
            {
                "title": "Fault model statistics",
                "labels": ["Fault model", "Occurrence (%)"],
                "data": self.get_fault_models()
            },
        ]
        results.append(self.get_effects_distribution())
        results = self.add_fault_model_information(results)
        return results

    def get_effects_distribution(self):
        """:return: a dictionary containing the fault effects distribution.

        """
        result = {
            "title": "Effects distribution",
            "labels": ["Effect", "Occurrence"],
            "data": [["Reboots", "Response bad formated", "Faults"],
                     [self.nb_reboots, self.nb_responses_bad_format, self.nb_faults]]
        }
        return result

    def set_dataframe(self, df):
        """Set the dataframe to the new value. Set the analysis_done flag to False as
        no analysis has been done on this dataframe.

        :param df: the dataframe to do the analysis on.

        """
        self.df = df
        self.analysis_done = False
