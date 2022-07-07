from StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual, core, event
import datetime

class StimulateProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()


    def update(self):
        self.dialogue = self.controller.dialogue
        self.controller.endBlock = self._checkBlock()

        self.w.flip()
        self.baseFrameworkTexture.draw()
        self.initialTextureSet.draw()
        self.dialogue.draw()

        feedback = self.controller.feedback
        if feedback is not None:
            feedback.draw()

        # 增加另一个epoch
        self.controller.currentEpochINX += 1
        # 增加另一个epoch
        self.controller.epochThisBlock += 1
        pass

    
        
    def change(self):

        self.controller.currentProcess = self.controller.finishProcess
        self.eventController.sendEvent(251)
        self.exchange_message_management.exchange_message_operator.state_monitor.cue_state = 'HOLD'
        print('set cue')


    def run(self):
        
        controller = self.controller
        self.w = controller.win
        
        message = 'STRD'
        self.exchange_message_management.send_exchange_message(message)
        print('\nStimulateProcess 发送开始异步检测指令，执行时间{}\n'.format(datetime.datetime.now()))
         
        frameINX = 0
        framesTextureVector = self.frameTextureSet[0]
        startTime = core.getTime()

        # 发送trigger
        
        while controller.currentProcess  == self:

            if frameINX == 0:
                self.eventController.sendEvent(self.controller.cueId+1)
                
            framesTextureVector[frameINX].draw()

            self.w.flip(clearBuffer=False)
            
            frameINX += 1
            if frameINX == len(framesTextureVector):
                frameINX = 0

        endTime = core.getTime()
        print("本试次结束，刺激时长{}".format(endTime-startTime))

        
        self.update()
        self.eventController.clearEvent()

    def _checkBlock(self):

        if self.controller.blockCues == []:
            self.controller.currentBlockINX += 1
            return True
        else:
            return False
