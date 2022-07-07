import sys
sys.path.append('.')

import datetime
import time
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from CommonSystem.Config import Config
from OperationSystem.MessageOperator import MessageOperator
from OperationSystem.AnalysisProcess.AnalysisController import AnalysisController
from OperationSystem.DataCash import  DataCash

# 启动控制接收及结果管理器
messageOperator = MessageOperator()  # 处理端接收消息处理函数

# 交换信息中心管理器
receiveTopic = 'stim_to_ope'
sendTopic = 'ope_to_stim'
messanger = ExchangeMessageManagement(messageOperator,receiveTopic,sendTopic)

# 创建实验信息从脚本函数中生成
config = Config()

# 放大器设置
dataStreaming = DataCash()
dataStreaming.connect()

messageOperator.messanger = messanger
messageOperator.streaming = dataStreaming

# 生成脑电信号分析检测控制器
controller = AnalysisController().initial(config, dataStreaming, messanger)
# 启动与刺激系统数据交换器
messanger.start()
print('Put on hold for stimulation,current state:%s'%messanger.state.control_state)


while messanger.state.control_state != 'STON':
    messanger.state.control_state = 'STON'
    # 等待开始处理标识
    time.sleep(0.1)

while messanger.state.control_state != 'EXIT':
    controller.run()
    time.sleep(0.1)
