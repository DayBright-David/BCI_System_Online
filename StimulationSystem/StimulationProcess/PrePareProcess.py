import time
from StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
from psychopy.visual.circle import Circle


class PrepareProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()

    def update(self):
    
        self.w = self.controller.win

        self.controller.cueId = self.controller.blockCues.pop(0)
        
        print()

    def change(self):
        
        self.controller.currentProcess = self.controller.stimulateProcess
        

    def run(self):
    
        self.update()
        
        self.controller.win = self.w

        time.sleep(1)

        self.change()

        

    def _showCue(self, id):
        """
        draw initial texture and show result
        :return: None
        """
        id = None
        # 绘制初始帧
        self.w.flip(False)
        self.initialTextureSet.draw()

        # 绘制识别结果提示框 用tuple

        stimTargetRectCell = self.stimTargetRectSet[0]
        pos = stimTargetRectCell[id].position
        x, y = pos
        y = y-90
        circle = Circle(win=self.w, pos=[x, y], radius=5)
        circle.colorSpace = 'rgb255'
        circle.color = (255, 0, 0)
        circle.draw()

        self.w.flip(False)
        time.sleep(0.5)

        return self.w
