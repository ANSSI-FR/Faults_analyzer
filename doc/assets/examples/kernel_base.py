import time # For example purpose only (NOT MANDATORY)

from labmanager.manager import KernelBase

class Kernel(KernelBase):
    def __init__(self):
        KernelBase.__init__(self)
        self.i = 0 # For example purpose only (NOT MANDATORY)

    def open(self) -> None:
        pass

    def work(self, exp) -> dict:
        self.logger.info(exp)   # Print the experiment parameters
        exp["plan_done"] = True # Set the "plan_done" to "True" to avoid
                                # infinite loop
        exp["i"] = self.i       # Add a parameter in the experiment
        self.i += 1
        self.logger.info(exp)   # Print the experiment parameters
        time.sleep(1)
        return exp

    def close(self) -> None:
        pass

