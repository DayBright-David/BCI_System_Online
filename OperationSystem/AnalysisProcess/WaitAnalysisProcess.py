from os import wait
from OperationSystem.AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import datetime
import time


class WaitAnalysisProcess(BasicAnalysisProcess):

    def run(self):

        print('Epoch {0} finished, entering waiting stage,{1}\n'.format(
            self.controller.currentEpochINX, datetime.datetime.now()))

        while (self.messenger.state.current_detect_state != 'STRD') and (self.messenger.state.control_state != 'EXIT'):
            self.messenger.state.current_detect_state = 'STRD'
            time.sleep(0.1)

        if self.controller.trainFlag is not True:
            self.controller.current_process = self.controller.training_process

        else :
            self.controller.current_process = self.controller.testing_process

        self.messenger.state.current_detect_state = 'HOLD'
            

        
