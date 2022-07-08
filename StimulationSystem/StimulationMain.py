import sys
sys.path.append('..')
sys.path.append('.')

sys.path.append(r'../CommonSystem/MessageReceiver')

from CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from StimulationSystem.StateMonitor import StateMonitor
from StimulationSystem.StimulationExchangeMessageOperator import StimulationExchangeMessageOperator
from StimulationSystem.Singleton.SingletonStimulationController import controller
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from CommonSystem.MessageReceiver.EventManager import EventManager
from StimulationSystem.enterStimulation import enterStimulation
import os
import pickle
import datetime
import time


folder_path = os.getcwd()

paradigm_name = 'adaptiveOnline'

if not os.path.exists(folder_path+'/stimulationInformationFolder'):
    os.makedirs(folder_path+'/stimulationInformationFolder')

if not os.path.exists(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name):
    os.makedirs(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name)

paradigm_folder_path = folder_path+'/stimulationInformationFolder'+'/'+paradigm_name

experiment_information = create_experiment_information(0,paradigm_name, paradigm_folder_path)

a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'rb')
paradigm_config = pickle.load(a_file)

state_monitor = StateMonitor() 
state_monitor.resultString = '>>'
state_monitor.status = 'INIT'

stimulationExchange_Messager = StimulationExchangeMessageOperator()
stimulationExchange_Messager.experiment_information = experiment_information
stimulationExchange_Messager.state_monitor = state_monitor
stimulationExchange_Messager.controller = controller

#event_manager = EventManager()
#exchange_message_operator = StimulationExchangeMessageOperator()

topic_stim_receive = 'ope_to_stim'
topic_stim_send = 'stim_to_ope'

exchange_message_management =ExchangeMessageManagement(stimulationExchange_Messager, topic_receive = topic_stim_receive, topic_send=topic_stim_send)
exchange_message_management.start()

experimentInformation = enterStimulation(experiment_information, paradigm_config, state_monitor, exchange_message_management)

# message = 'STOP'
# exchange_message_management.send_exchange_message(message)
                       
while state_monitor.status != 'PROK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'PROK', datetime.datetime.now()))
    time.sleep(0.1)

message = 'DCNS'
exchange_message_management.send_exchange_message(message)
while state_monitor.status != 'DCOK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'DCOK', datetime.datetime.now()))
    time.sleep(0.1)

message = 'CSAL'
exchange_message_management.send_exchange_message(message)
while state_monitor.status != 'CAOK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'CAOK', datetime.datetime.now()))
    time.sleep(0.1)


exchange_message_management.stop()  



      
