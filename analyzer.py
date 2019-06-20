import logging
import daiquiri

from bin_utils import *
from utils import print_progress_bar

class Analyzer():

    def __init_logger(self):
        daiquiri.setup(level=logging.DEBUG)
        return daiquiri.getLogger()       
    
    def __init__(self, PARAMS):
        self.logger = self.__init_logger()
        
        self.obs_names = PARAMS["obs_names"]
        self.nb_obs = len(self.obs_names)
        self.default_values = PARAMS["default_values"]
        self.to_test = PARAMS["to_test"]
        self.done_name = PARAMS["done_name"]
        self.fault_name = PARAMS["fault_name"]
        self.reboot_name = PARAMS["reboot_name"]
        self.log_name = PARAMS["log_name"]
        self.log_separator = PARAMS["log_separator"]
        self.power_name = PARAMS["power_name"]
        self.delay_name = PARAMS["delay_name"]
        self.nb_bits = PARAMS["nb_bits"]        
        self.df = PARAMS["dataframe"]
        self.base_add_reg = None
        self.exp_type = None
        if "type" in PARAMS:
            self.exp_type = PARAMS["type"]
        if self.exp_type is "memory":
            self.base_add_reg = PARAMS["base_add_reg"]
        
        self.powers = list(self.df[self.power_name].unique())
        self.delays = list(self.df[self.delay_name].unique())

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
        self.base_address = []
        self.analysis_done = False

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

        self.other_obs_value_after_execution_origin_occurence = [0]*self.nb_obs
        
    def __get_faulted_obs(self, ope):
        ret = []
        values = self.__get_values_from_log(ope)
        if not values is None:
            for i in range(len(values)):
                if self.to_test[i]:
                    if values[i] != self.default_values[i]:
                        ret.append([i, values[i]])
        return ret
        
    def __update_result(self, ope, values, result, param):
        param_value = ope[param]
        value_index = values.index(param_value)
        result[value_index] += 1
        
    def __is_done(self, ope):
        return ope[self.done_name]

    def __is_set_as_faulted(self, ope):
        if self.__is_done(ope):
            return ope[self.fault_name]
        return False

    def __is_set_as_reboot(self, ope):
        if self.__is_done(ope):
            return ope[self.reboot_name]
        return False

    def __get_values_from_log(self, ope):
        try:
            log = ope[self.log_name]
            log = log.split(self.log_separator)
            values = log[1:-1]
            values = [int(v) for v in values]
            return values
        except Exception as e:
            self.logger.error("In __get_values_from_log(): " + str(e))
    
    def __get_values_after_execution(self, ope):
        if not self.__is_set_as_reboot(ope) and not self.__is_set_as_faulted(ope):
            return self.__get_values_from_log(ope)

    def __get_values_after_current_execution(self, ope):
        return self.__get_values_from_log(ope)
        
    def __is_done_analysis(self, ope):
        self.nb_done += 1
        self.values_after_current_execution = self.__get_values_after_current_execution(ope)
        if len(self.values_after_execution) == 0:
            self.values_after_execution = self.__get_values_after_execution(ope)

    def __is_reboot_analysis(self, ope):
        self.nb_reboots += 1
        self.__update_result(ope, self.powers, self.reboot_powers, self.power_name)
        self.__update_result(ope, self.delays, self.reboot_delays, self.delay_name)

    def __update_faulted_obs(self, faulted_obs):
        self.faulted_obs[faulted_obs] += 1        

    def __get_base_address(self, ope):
        return self.__get_values_from_log(ope)[self.base_add_reg]
        
    def __update_faulted_values(self, faulted_value, ope):
        if not faulted_value in self.faulted_values:
            self.faulted_values.append(faulted_value)
            self.faulted_values_occurrence.append(1)
            if self.exp_type is "memory":
                self.base_address.append([self.__get_base_address(ope)])
        else:
            for i, v in enumerate(self.faulted_values):
                if v == faulted_value:
                    self.faulted_values_occurrence[i] += 1
                    if self.exp_type is "memory":
                        self.base_address[i].append(self.__get_base_address(ope))

    def __update_bit_set(self, faulted_value):
        max_value = (1 << self.nb_bits) - 1
        if s2u(faulted_value, self.nb_bits) == max_value:
            self.bit_set += 1
            return True
        return False

    def __update_bit_reset(self, faulted_value):
        if s2u(faulted_value, self.nb_bits) == 0:
            self.bit_reset += 1
            return True
        return False

    def __update_bit_flip(self, faulted_obs, faulted_value):
        if s2u(faulted_value, self.nb_bits) == a2_comp(self.default_values[faulted_obs], self.nb_bits):
            self.bit_flip += 1
            return True
        return False

    def __update_other_obs_value(self, faulted_obs, faulted_value):
        if s2u(faulted_value, self.nb_bits) in self.default_values:
            self.other_obs_value += 1
            return True
        return False

    def __update_other_obs_value_after_execution_origin_occurence(self, faulted_value):
        origin = self.values_after_current_execution.index(faulted_value)
        self.other_obs_value_after_execution_origin_occurence[origin] += 1
    
    def __update_other_obs_value_after_execution(self, faulted_obs, faulted_value):
        if s2u(faulted_value, self.nb_bits) in self.values_after_current_execution:
            if not faulted_obs is self.values_after_current_execution.index(s2u(faulted_value, self.nb_bits)):
                self.other_obs_value_after_execution += 1
                self.__update_other_obs_value_after_execution_origin_occurence(faulted_value)
                return True
        return False
    
    def __update_other_obs_complementary_value(self, faulted_obs, faulted_value):
        for val in self.default_values:
            if s2u(faulted_value, self.nb_bits) == a2_comp(val, self.nb_bits):
                self.other_obs_complementary_value += 1
                return True
        return False

    def __update_add_with_other_obs(self, faulted_obs, faulted_value):
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] + val, self.nb_bits):
                if i != faulted_obs:
                    self.add_with_other_obs += 1
                    return True
        return False
    
    def __update_and_with_other_obs(self, faulted_obs, faulted_value):
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] & val, self.nb_bits):
                if i != faulted_obs:
                    self.and_with_other_obs += 1
                    return True
        return False
    
    def __update_or_with_other_obs(self, faulted_obs, faulted_value):
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] | val, self.nb_bits):
                if i != faulted_obs:
                    self.or_with_other_obs += 1
                    return True
        return False
    
    def __update_xor_with_other_obs(self, faulted_obs, faulted_value):
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] ^ val, self.nb_bits):
                if i != faulted_obs:
                    self.xor_with_other_obs += 1
                    return True
        return False
    
    def __update_sub_with_other_obs(self, faulted_obs, faulted_value):
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] - val, self.nb_bits):
                if i != faulted_obs:
                    self.sub_with_other_obs += 1
                    return True
        return False
    
    def __update_fault_models(self, faulted):
        faulted_obs = faulted[0]
        faulted_value = faulted[1]
        fault_model_known = False
        fault_model_known |= self.__update_bit_set(faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_bit_reset(faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_bit_flip(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_other_obs_value(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_other_obs_complementary_value(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_add_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_and_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_or_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_xor_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_sub_with_other_obs(faulted_obs, faulted_value)
        if not fault_model_known:
            fault_model_known |= self.__update_other_obs_value_after_execution(faulted_obs, faulted_value)
        if not fault_model_known:
            self.fault_model_unknown += 1
                    
    def __update_faulted_obs_and_values(self, ope):
        ope_faulted_obs = self.__get_faulted_obs(ope)
        if not ope_faulted_obs is None:
            self.nb_faulted_obs += len(ope_faulted_obs)
            for faulted in ope_faulted_obs:
                self.__update_faulted_obs(faulted[0])
                self.__update_faulted_values(faulted[1], ope)
                self.__update_fault_models(faulted)
        
    def __is_faulted_analysis(self, ope):
        self.nb_faults += 1
        self.__update_result(ope, self.powers, self.fault_powers, self.power_name)
        self.__update_result(ope, self.delays, self.fault_delays, self.delay_name)
        self.__update_faulted_obs_and_values(ope)
        
    def __ope_loop_analysis(self):
        i=0
        for _, ope in self.df.iterrows():
            if self.__is_done(ope):
                self.__is_done_analysis(ope)

            if self.__is_set_as_reboot(ope):
                self.__is_reboot_analysis(ope)

            if self.__is_set_as_faulted(ope):
                self.__is_faulted_analysis(ope)

            i += 1
            print_progress_bar(i, self.nb_to_do, prefix = "Analysis progress:",
                               suffix = "Complete", length=50)
            
    def run_analysis(self):
        if self.analysis_done == False:
            self.__ope_loop_analysis()
            self.analysis_done = True
        else:
            self.logger.info("Analysis already done, no need to do it again.")

    def get_nb_faulted_obs(self):
        return self.nb_faulted_obs
            
    def get_nb_to_do(self):
        return self.nb_to_do
            
    def get_powers(self):
        return self.powers

    def get_delays(self):
        return self.delays
            
    def get_obs_names(self):
        return self.obs_names
            
    def get_faulted_values(self):
        return self.faulted_values

    def get_faulted_values_occurrence(self):
        return self.faulted_values_occurrence
            
    def get_faulted_obs(self):
        return self.faulted_obs
            
    def get_fault_delays(self):
        return self.fault_delays
            
    def get_fault_powers(self):
        return self.fault_powers
            
    def get_nb_faults(self):
        return self.nb_faults
            
    def get_reboot_delays(self):
        return self.reboot_delays
            
    def get_reboot_powers(self):
        return self.reboot_powers
            
    def get_nb_reboots(self):
        return self.nb_reboots
        
    def get_values_after_execution(self):
        return self.values_after_execution

    def get_nb_done(self):
        return self.nb_done

    def get_fault_models(self):
        ret = []
        ret.append(["Fault model unknown", "Bit set", "Bit reset", "Bit flip", "Other obs value", "Other obs complementary value", "Add with other obs", "And with other obs", "Or with other obs", "Xor with other obs", "Sub with other obs", "Other obs value after execution"])
        ret.append([self.fault_model_unknown, self.bit_set, self.bit_reset, self.bit_flip, self.other_obs_value, self.other_obs_complementary_value, self.add_with_other_obs, self.and_with_other_obs, self.or_with_other_obs, self.xor_with_other_obs, self.sub_with_other_obs, self.other_obs_value_after_execution])
        return ret
    
    def get_analysis_results(self):
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

    def get_base_address(self):
        return self.base_address

    def get_other_obs_value_after_execution_origin_occurence(self):
        return self.other_obs_value_after_execution_origin_occurence
