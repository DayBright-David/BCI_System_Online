from abc import ABCMeta, abstractmethod
from psychopy.visual.rect import Rect
from psychopy import visual, core, event
from psychopy.visual.circle import Circle

import time

class BasicStimulationProcess:
    def __init__(self):
        self.controller = None

    @abstractmethod
    def initial(self,controller, viewStruct,exchange_message_management):
        # controller 负责控制刺激状态的调换
        self.controller = controller
        # eventController 负责发送事件标记
        self.eventController = controller.eventController
        # exchange_message_management 负责刺激和处理之间的通讯
        self.exchange_message_management = exchange_message_management

        # 刺激帧
        self.frameTextureSet = viewStruct['frameTextureSet']
        # 黑色背景
        self.baseFrameworkTexture = viewStruct['baseFrameworkTexture']
        # 初始帧
        self.initialTextureSet = viewStruct['initialTextureSet'][0]
        # 界面
        self.w = viewStruct['w']
        # 刺激目标信息
        self.stimTargetRectSet = viewStruct['stimTargetRectSet']
        # 所有的提示
        self.cues = viewStruct['cues']
        # 目标数
        self.targetNUM = viewStruct['targetNUM']
        # 一个block的大小
        self.blockSize = self.targetNUM//2
        # 字符对应
        self.targetTable = viewStruct['targetTable']
        # 提示字符
        self.cueText = viewStruct['cueText']
        # 字符串应该出现的位置
        self.stringPosition = viewStruct['stringPositions'][0]
        # 字符映射
        self.commandID = viewStruct['commandID']
        # 历史出现的字符
        self.historyString = []

        
        
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def change(self):
        pass

    @abstractmethod
    def run(self):
        pass
    
    def drawDialogue(self,text,color,fillColor):
    
        dialogue = visual.TextBox2(
        self.w, text=text, font='Hack',
        pos=(0,530),units='pix',     letterHeight=50.0,
        size=(1470,60), borderWidth=4.0,
        color=color, colorSpace='rgb',
        opacity=1.0,
        bold=False, italic=False,
        lineSpacing=10.0,
        padding=0.0,
        anchor='top-center',
        fillColor=fillColor, borderColor='black',
        flipHoriz=False, flipVert=False,
        editable=False,
        name='textbox',
        autoLog=True) 



        return dialogue
