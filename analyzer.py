import logging
import daiquiri
import numpy as np

from bin_utils import *
from utils import print_progress_bar

class Analyzer():
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

    type - type of the experiment (memory or registers).

    TODO: remove the "type" parameter.

    """

    def __get_map_size(self):
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
    
    def __init_logger(self):
        """Initialize the logger the corresponding level.

        TODO: pass the logging level as an argument.

        """
        daiquiri.setup(level=logging.DEBUG)
        return daiquiri.getLogger()       
    
    def __init__(self, PARAMS):
        """Constructor of the class. Parse the parameters from the PARAMS dictionary.
        Realize also some other initialization.

        Arguments:

        PARAMS - a dictionary containing all the parameters needed for the
        analysis of the experiments

        TODO: pass all parameters as arguments instead of a dictionnary
        TODO: refactoring and clean up

        """
        # Initialization of the logger
        self.logger = self.__init_logger()

        # Parsing of the PARAMS dictionary
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
        self.executed_instructions = PARAMS["executed_instructions"]
        self.base_add_reg = None
        self.exp_type = None
        if "type" in PARAMS:
            self.exp_type = PARAMS["type"]
        if self.exp_type is "memory":
            self.base_add_reg = PARAMS["base_add_reg"]
        self.coordinates = None
        if "coordinates" in PARAMS:
            self.coordinates = PARAMS["coordinates"]

        # Extract all the power, delay value from the dataframe
        self.powers = list(self.df[self.power_name].unique())
        self.delays = list(self.df[self.delay_name].unique())

        # Extract the map size
        self.map_size = None
        if not self.coordinates is None:
            self.map_size = self.__get_map_size()

        # General information about the experiment
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

        # Fault models
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

        # General information about the fault models
        self.other_obs_value_after_execution_origin_occurence = [0]*self.nb_obs

        # Matrix
        self.reboot_matrix = None
        self.fault_matrix = None
        self.done_matrix = None
        if not self.map_size is None:
            self.reboot_matrix = np.zeros(self.map_size)
            self.fault_matrix = np.zeros(self.map_size)
            self.done_matrix = np.zeros(self.map_size)

    def __get_faulted_obs(self, ope):
        """Return the faulted observed to test with their faulted value from an
        operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        ret = []
        values = self.__get_values_from_log(ope)
        if not values is None:
            for i in range(len(values)):
                if self.to_test[i]:
                    if values[i] != self.default_values[i]:
                        ret.append([i, values[i]])
        return ret
        
    def __update_result(self, ope, values, result, param):
        """Update a list of results.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        values - list of the values that are analyzed.

        result - occurrence of apparition of the corresponding values. A value
        and its occurrence share the same index in result and values lists.

        param - the key name of the parameter to be updated.

        """
        param_value = ope[param]
        value_index = values.index(param_value)
        result[value_index] += 1
        
    def __is_done(self, ope):
        """Return if the operation is set as done.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        return ope[self.done_name]

    def __is_response_bad_formated(self, ope):
        """Return if the response of receive during the operation is bad formated. Ie.
        the number of values from the log in different from the number of
        observed.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        if self.__is_done(ope):
            values = self.__get_values_from_log(ope)
            if not len(values) is self.nb_obs:
                self.nb_responses_bad_format += 1
                return True
            return False

    def __is_faulted(self, ope):
        """Return if the operation has at least one observed faulted.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        if self.__is_done(ope):
            values = self.__get_values_from_log(ope)
            for i in range(self.nb_obs):
                if self.to_test[i]:
                    if values[i] != self.default_values[i]:
                        return True
        return False

    def __is_set_as_faulted(self, ope):
        """Return if the operation is set as faulted or not.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        if self.__is_done(ope):
            return ope[self.fault_name]
        return False

    def __is_set_as_reboot(self, ope):
        """Return if the operation is set as reboot or not.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        if self.__is_done(ope):
            return ope[self.reboot_name]
        return False

    def __get_values_from_log(self, ope):
        """Return the values of the observed from the log.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        try:
            log = str(ope[self.log_name])
            log = log.split(self.log_separator)
            values = log[1:-1]
            values = [int(v) for v in values]
            return values
        except Exception as e:
            self.logger.error("In __get_values_from_log(): " + str(e))
    
    def __get_values_after_execution(self, ope):
        """Return the values of the observed if the operation is neither reboot nor
        faulted. This should correspond to the expected values of the observed after a
        normal execution. However, in some case, these value can be different from an
        operation to another due to reboot. Take care with this function during the
        analysis.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        if not self.__is_set_as_reboot(ope) and not self.__is_set_as_faulted(ope):
            return self.__get_values_from_log(ope)

    def __get_values_after_current_execution(self, ope):
        """Return the values of the observed as stored in the log.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        return self.__get_values_from_log(ope)
        
    def __is_done_analysis(self, ope):
        """Do the analysis routine in the case the operation is done.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.nb_done += 1
        self.values_after_current_execution = self.__get_values_after_current_execution(ope)
        if len(self.values_after_execution) == 0:
            self.values_after_execution = self.__get_values_after_execution(ope)
        if not self.coordinates is None:
            self.__update_done_matrix(ope)

    def __update_matrix(self, ope, mat):
        """Update the matrix with the coordinates of the operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.
        
        """
        ope_coord = []
        for coord in self.coordinates:
            ope_coord.append(ope[coord])
        mat[tuple(ope_coord)] += 1

    def __update_done_matrix(self, ope):
        """Update the done matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.__update_matrix(ope, self.done_matrix)

    def __update_fault_matrix(self, ope):
        """Update the fault matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.__update_matrix(ope, self.fault_matrix)

    def __update_reboot_matrix(self, ope):
        """Update the reboot matrix.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.__update_matrix(ope, self.reboot_matrix)

    def __is_reboot_analysis(self, ope):
        """Do the analysis routine in the case the operation led to a reboot of the
        system.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.nb_reboots += 1
        self.__update_result(ope, self.powers, self.reboot_powers, self.power_name)
        self.__update_result(ope, self.delays, self.reboot_delays, self.delay_name)
        if not self.coordinates is None:
            self.__update_reboot_matrix(ope)

    def __update_faulted_obs(self, faulted_obs):
        """Update the list of the faulted observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        """
        self.faulted_obs[faulted_obs] += 1

    def __get_base_address(self, ope):
        """Return the value of the register containing the base address from the
        operation.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        TODO: remove this useless function.

        """
        return self.__get_values_from_log(ope)[self.base_add_reg]

    def __update_faulted_values(self, faulted_value, ope):
        """Update the faulted values, their occurrence and the used base address in the
        case of a memory experiment.

        Arguments:

        faulted_value - the value of the faulted observed.

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        TODO: remove everything about "memory" experiment

        """
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
        """Update the bit set fault model. Attention ! This function only consider a
        bit set on the WHOLE word.

        Arguments:

        faulted_value - the value of the faulted observed.

        """
        max_value = (1 << self.nb_bits) - 1
        if s2u(faulted_value, self.nb_bits) == max_value:
            self.bit_set += 1
            return True
        return False

    def __update_bit_reset(self, faulted_value):
        """Update the bit reset fault model. Attention ! This function only consider a
        bit reset on the WHOLE word.

        Arguments:

        faulted_value - the value of the faulted observed.

        """
        if s2u(faulted_value, self.nb_bits) == 0:
            self.bit_reset += 1
            return True
        return False

    def __update_bit_flip(self, faulted_obs, faulted_value):
        """Update the bit flip fault model. Attention ! This function only consider a
        bit flip on the WHOLE world.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        if s2u(faulted_value, self.nb_bits) == a2_comp(self.default_values[faulted_obs], self.nb_bits):
            self.bit_flip += 1
            return True
        return False

    def __update_other_obs_value(self, faulted_obs, faulted_value):
        """Update the other observed value fault model considering the initial
        state.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        if s2u(faulted_value, self.nb_bits) in self.default_values:
            self.other_obs_value += 1
            return True
        return False

    def __update_other_obs_value_after_execution(self, faulted_obs, faulted_value):
        """Update the other observed value fault model considering the values of the observed after the execution of the program.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.values_after_current_execution):
            if not i is faulted_obs:
                if s2u(faulted_value, self.nb_bits) == s2u(int(val), self.nb_bits):
                    self.other_obs_value_after_execution += 1
                    self.other_obs_value_after_execution_origin_occurence[i] += 1
                    return True
        return False
    
    def __update_other_obs_complementary_value(self, faulted_obs, faulted_value):
        """Update the other observed complementary value fault model considering the
        initial values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for val in self.default_values:
            if s2u(faulted_value, self.nb_bits) == a2_comp(val, self.nb_bits):
                self.other_obs_complementary_value += 1
                return True
        return False

    def __update_add_with_other_obs(self, faulted_obs, faulted_value):
        """Update the add with other observed fault model considering the initial
        values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] + val, self.nb_bits):
                if i != faulted_obs:
                    self.add_with_other_obs += 1
                    return True
        return False
    
    def __update_and_with_other_obs(self, faulted_obs, faulted_value):
        """Update the and with other observed fault model considering the initial
        values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] & val, self.nb_bits):
                if i != faulted_obs:
                    self.and_with_other_obs += 1
                    return True
        return False
    
    def __update_or_with_other_obs(self, faulted_obs, faulted_value):
        """Update the or with other observed fault model considering the initial
        values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] | val, self.nb_bits):
                if i != faulted_obs:
                    self.or_with_other_obs += 1
                    return True
        return False
    
    def __update_xor_with_other_obs(self, faulted_obs, faulted_value):
        """Update the xor with other observed fault model considering the initial
        values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] ^ val, self.nb_bits):
                if i != faulted_obs:
                    self.xor_with_other_obs += 1
                    return True
        return False
    
    def __update_sub_with_other_obs(self, faulted_obs, faulted_value):
        """Update the sub with other observed fault model considering the initial
        values of the observed.

        Arguments:

        faulted_obs - the index of the faulted observed.

        faulted_value - the value of the faulted observed.

        """
        for i, val in enumerate(self.default_values):
            if s2u(faulted_value, self.nb_bits) == s2u(self.default_values[faulted_obs] - val, self.nb_bits):
                if i != faulted_obs:
                    self.sub_with_other_obs += 1
                    return True
        return False

    def __update_executed_instruction(self, faulted_value):
        """Update the executed instruction fault model.

        Arguments:

        faulted_value - the value of the faulted observed.

        """
        if s2u(faulted_value, self.nb_bits) in self.executed_instructions:
            self.executed_instruction += 1
            return True
        return False

    def __update_fault_models(self, faulted):
        """Update the fault models. Attention ! This function is not satisfactory as it
        will stop once a fault explain the faulted value. However, several fault models
        might explain it. But removing the fault_model_known test will biased the
        statistics has we would have more fault models than faults...

        Arguments:

        faulted - a 2 items list containing the index of the faulted obs and
        the faulted value.

        """
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
            fault_model_known |= self.__update_executed_instruction(faulted_value)
        if not fault_model_known:
            self.fault_model_unknown += 1

    def __update_faulted_obs_and_values(self, ope):
        """Update the number of faulted observed, the faulted observed, the faulted
        values and the fault models.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        ope_faulted_obs = self.__get_faulted_obs(ope)
        if not ope_faulted_obs is None:
            self.nb_faulted_obs += len(ope_faulted_obs)
            for faulted in ope_faulted_obs:
                self.__update_faulted_obs(faulted[0])
                self.__update_faulted_values(faulted[1], ope)
                self.__update_fault_models(faulted)
        
    def __is_faulted_analysis(self, ope):
        """Do the analysis routine in the case the operation has been faulted.

        Arguments:

        ope - the operation, which is a line from the dataframe, containing all
        the information about this step of the experiment.

        """
        self.nb_faults += 1
        self.__update_result(ope, self.powers, self.fault_powers, self.power_name)
        self.__update_result(ope, self.delays, self.fault_delays, self.delay_name)
        self.__update_faulted_obs_and_values(ope)
        if not self.coordinates is None:
            self.__update_fault_matrix(ope)

        
    def __ope_loop_analysis(self):
        """Main loop of the analysis. Go through every operation and launch the
        corresponding analysis routines."""
        i=0
        for _, ope in self.df.iterrows():
            if self.__is_done(ope):
                self.__is_done_analysis(ope)

            if self.__is_set_as_reboot(ope):
                self.__is_reboot_analysis(ope)

            if not self.__is_response_bad_formated(ope):
                if self.__is_faulted(ope):
                    self.__is_faulted_analysis(ope)

            i += 1
            print_progress_bar(i, self.nb_to_do, prefix = "Analysis progress:",
                               suffix = "Complete", length=50)
            
    def run_analysis(self):
        """Run the analysis. This function must be called before getting any result.

        TODO: Automatically run this function if a result is asked and it has
        not been done.

        """
        if self.analysis_done == False:
            self.__ope_loop_analysis()
            self.analysis_done = True
        else:
            self.logger.info("Analysis already done, no need to do it again.")

    def get_nb_faulted_obs(self):
        """Return the number of faulted observed.

        """
        return self.nb_faulted_obs

    def get_nb_to_do(self):
        """Return the number of operations to do.

        """
        return self.nb_to_do

    def get_powers(self):
        """Return the tested voltage powers.

        """
        return self.powers

    def get_delays(self):
        """Return the tested delays.

        """
        return self.delays
            
    def get_obs_names(self):
        """Return the names of the observed.

        """
        return self.obs_names
            
    def get_faulted_values(self):
        """Return the faulted values.

        TODO: Merge the faulted values and their occurrence.

        """
        return self.faulted_values

    def get_faulted_values_occurrence(self):
        """Return the occurrence of the faulted values.

        TODO: Merge the faulted values and their occurrence.

        """
        return self.faulted_values_occurrence
            
    def get_faulted_obs(self):
        """Return the faulted observed occurrence.

        """
        return self.faulted_obs
            
    def get_fault_delays(self):
        """Return delays occurrence in faults.
        
        """
        return self.fault_delays
            
    def get_fault_powers(self):
        """Return voltage power occurrence in faults.

        """
        return self.fault_powers
            
    def get_nb_faults(self):
        """Return the number of faults.

        """
        return self.nb_faults
            
    def get_reboot_delays(self):
        """Return delays occurrence in reboots.

        """
        return self.reboot_delays
            
    def get_reboot_powers(self):
        """Return voltage powers occurrence in reboots.

        """
        return self.reboot_powers
            
    def get_nb_reboots(self):
        """Return the number of reboots.

        """
        return self.nb_reboots
        
    def get_values_after_execution(self):
        """Return the values after execution. Attention ! These values correspond to
        one non faulted and non reboot operation but might change between
        operations."""
        return self.values_after_execution

    def get_nb_done(self):
        """Return the number of done operations.

        """
        return self.nb_done

    def get_fault_models(self):
        """Return the fault models and their corresponding occurrence in faults.

        """
        ret = []
        ret.append(["Fault model unknown",
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
                    "Executed instruction"])
        ret.append([self.fault_model_unknown,
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
                    self.executed_instruction])
        return ret

    def get_nb_responses_bad_format(self):
        """Return the number of responses bad formated.

        """
        return self.nb_responses_bad_format

    def get_general_stats(self):
        """Return the general statistics of the experiments and their values.

        """
        ret = {
            "titles": ["Number of operations to do",
                       "Number of operation done",
                       "Percentage done (%)",
                       "Number of reboots",
                       "Percentage of reboots (%)",
                       "Number of responses bad formated",
                       "Percentage of responses bad formated (%)",
                       "Number of faults",
                       "Percentage of faults (%)",
                       "Number of faulted obs",
                       "Average faulted obs per fault"],
            "data": [self.nb_to_do,
                     self.nb_done,
                     100*self.nb_done/float(self.nb_to_do),
                     self.nb_reboots,
                     100*self.nb_reboots/float(self.nb_done),
                     self.nb_responses_bad_format,
                     100*self.nb_responses_bad_format/float(self.nb_done),
                     self.nb_faults,
                     100*self.nb_faults/float(self.nb_done),
                     self.nb_faulted_obs,
                     self.nb_faulted_obs/float(self.nb_faults)]
        }
        return ret

    def get_analysis_results(self):
        """Return the analysis result.

        """
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
        """Return the base address.

        """
        return self.base_address

    def get_other_obs_value_after_execution_origin_occurence(self):
        """Return the occurrence of faulted value origin in the case of the other
        observed value after execution faulted model."""
        return self.other_obs_value_after_execution_origin_occurence

    def get_reboot_matrix(self):
        """Return the reboot matrix.

        """
        return self.reboot_matrix

    def get_fault_matrix(self):
        """Return the fault matrix.

        """
        return self.fault_matrix

    def get_done_matrix(self):
        """Return the done matrix.

        """
        return self.done_matrix
