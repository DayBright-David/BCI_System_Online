from CommonSystem.MessageReceiver.EventManager import EventManager
from CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
import datetime

'''
CTOK = 
DCOK = 
TROK = 
PROK = 
TNOK = 
PNOK = 
CAOK =
STSN = 
RSLT = 
'''

class StimulationExchangeMessageOperator:
    def __init__(self):
        #self.event_manager = EventManager()
        self.experiment_information = None
        self.state_monitor = None
        self.controller = None

        self.events = ['CTOK',
                       'DCOK',
                       'TROK',
                       'PROK',
                       'TNOK',
                       'PNOK',
                       'CAOK',
                       'STSN',
                       'RSLT',
                       'CUE',
                       'FreeSpelling']

    def do_CTOK(self,event):
        self.state_monitor.status = 'CTOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('CTOK', self.state_monitor.status))

    def do_DCOK(self, event):
        self.state_monitor.status = 'DCOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('DCOK', self.state_monitor.status))

    def do_TROK(self, event):
        self.state_monitor.status = 'TROK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('TROK', self.state_monitor.status))

    def do_PROK(self, event):
        self.state_monitor.status = 'PROK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('PROK', self.state_monitor.status))

    def do_TNOK(self, event):
        self.state_monitor.status = 'TNOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('TNOK', self.state_monitor.status))

    def do_PNOK(self, event):
        self.state_monitor.status = 'PNOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('PNOK', self.state_monitor.status))


    def do_CAOK(self, event):
        self.state_monitor.status = 'CAOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('CAOK', self.state_monitor.status))

    def do_STSN(self, event):
        self.state_monitor.status = 'STSN'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state_monitor.status))

    def do_CUE(self,event):
        self.state_monitor.cue_state = 'CUE'
        print('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state_monitor.status))

    def do_RSLT(self, event):
        message = event.message
        message_result = message['result']

        epochINX = self.controller.currentEpochINX
        cue = self.controller.cueId
        print('当前时刻{}：'.format(datetime.datetime.now()))
        print('收到第%s个epoch反馈,提示为%d,结果为%d' % (epochINX, cue, message_result))
        
        # 当前反馈结果
        
        self.controller.currentResult = message_result
        self.controller.currentProcess.change()

    def do_SPELLING(self, event):
        self.state_monitor.trainEnd = 'FreeSpelling'
        print('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state_monitor.status))

    def add_listener(self, event_manager):
        event_manager.AddEventListener('CTOK', self.do_CTOK)
        event_manager.AddEventListener('DCOK', self.do_DCOK)
        event_manager.AddEventListener('TROK', self.do_TROK)
        event_manager.AddEventListener('PROK', self.do_PROK)
        event_manager.AddEventListener('TNOK', self.do_TNOK)
        event_manager.AddEventListener('PNOK', self.do_PNOK)
        event_manager.AddEventListener('CAOK', self.do_CAOK)
        event_manager.AddEventListener('STSN', self.do_STSN)
        event_manager.AddEventListener('RSLT', self.do_RSLT)
        event_manager.AddEventListener('CUE', self.do_CUE)
        event_manager.AddEventListener('FreeSpelling', self.do_SPELLING)

    def remove_listener(self, event_manager):
        event_manager.RemoveEventListener('CTOK', self.do_CTOK)
        event_manager.RemoveEventListener('DCOK', self.do_DCOK)
        event_manager.RemoveEventListener('TROK', self.do_TROK)
        event_manager.RemoveEventListener('PROK', self.do_PROK)
        event_manager.RemoveEventListener('TNOK', self.do_TNOK)
        event_manager.RemoveEventListener('PNOK', self.do_PNOK)
        event_manager.RemoveEventListener('CAOK', self.do_CAOK)
        event_manager.RemoveEventListener('STSN', self.do_STSN)
        event_manager.RemoveEventListener('RSLT', self.do_RSLT)
        event_manager.RemoveEventListener('CUE', self.do_CUE)
        event_manager.RemoveEventListener('FreeSpelling', self.do_SPELLING)
