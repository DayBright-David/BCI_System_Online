from numpy import random
from StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from StimulationSystem.Singleton.SingletonStimulationController import controller
import datetime
import time
from psychopy import visual, core, event
from psychopy.visual.rect import Rect
import os
from tqdm import tqdm
import numpy as np


def enterStimulation(experiment_information, paradigm_config, state_monitor, exchange_message_management):

    message = 'CTNS'
    exchange_message_management.send_exchange_message(message)
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status,
            'CTOK', datetime.datetime.now()))

    while state_monitor.status != 'CTOK':
        time.sleep(0.1)

    message = 'STAR'
    exchange_message_management.send_exchange_message(message)
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status,
            'TROK', datetime.datetime.now()))

    while state_monitor.status != 'TROK':
        time.sleep(0.1)


    experiment_information.experiment_start_time = datetime.datetime.now()
    print(datetime.datetime.now())

    # 刺激界面
    mywin = visual.Window([1920, 1080], monitor="testMonitor", units="pix", fullscr=True, waitBlanking=True,useFBO=True,allowStencil=True,
                          color=(0, 0, 0),colorSpace='rgb255',screen=0)

    relaxText = visual.TextStim(mywin, pos=[0, 0], text='系统初始化，请保持放松\n\n\n运行过程中，按住ESC键可退出实验', color=(255, 255, 255), colorSpace='rgb255', )
    relaxText.draw()
    mywin.flip()

    stimulation_frames_path = paradigm_config.stimulation_frames_path
    stimTargetRectSet = paradigm_config.stimTargetRectSet
    stringPositions = paradigm_config.stringPositions


    # 背景帧
    base_framework = paradigm_config.background_frame_path
    baseFrameworkTexture = visual.ImageStim(mywin, image=base_framework,
                                            pos=[0, 0], size=[1920, 1080],
                                            units='pix', flipVert=False)


    #  
    frameSet = []
    initial_frameSet = []
    for i in range(0, len(stimulation_frames_path)):
        temp_frameSet = stimulation_frames_path[i][1:len(
            stimulation_frames_path[i])]
        frameSet.append(temp_frameSet)
        initial_frameSet.append(stimulation_frames_path[i][0])


    # 刺激帧 和 初始帧
    initialTextureSet = []
    frameTextureSet = []
    initialFrameTemp = initial_frameSet[0]
    initialTextureSet.append(visual.ImageStim(mywin, image=initialFrameTemp, pos=[
                             0, 0], size=[1920, 1080], units='pix', flipVert=False))

    framesTemp = frameSet[0]
    framesTextureVector = []

    for frame in tqdm(framesTemp):
        framesTextureVector.append(visual.ImageStim(mywin, image=frame, pos=[
                                   0, 0], size=[1920, 1080], units='pix', flipVert=False))
        frameTextureSet.append(framesTextureVector)


    schema_process_information = experiment_information.schema_process_information
    # viewStruct 存放所有的刺激信息
    viewStruct = {'frameTextureSet': frameTextureSet,
                  'baseFrameworkTexture': baseFrameworkTexture,
                  'initialTextureSet': initialTextureSet,
                  'stimTargetRectSet': stimTargetRectSet,
                  'stringPositions': stringPositions,
                  'w': mywin,
                  'COM': experiment_information.port,
                  'targetNUM': experiment_information.targetNUM,
                  'cues': experiment_information.cues,
                  'cueText': experiment_information.cueText,
                  'targetTable':schema_process_information.targetTable['DISPLAYCHAR'],
                  'commandID':schema_process_information.targetTable['COMMANDID']}

    
    stimulationController = controller
    stimulationController.initial(viewStruct,exchange_message_management)

    # 实验准备开始信息
    prepareFinishText = visual.TextStim(mywin, pos=[0, 0], text='系统准备完毕，即将开始实验。', color=(255, 255, 255),
                                 colorSpace='rgb255')
    prepareFinishText.draw()

    mywin.flip()
    time.sleep(0.5)
    print(datetime.datetime.now())
    message = 'STON'
    exchange_message_management.send_exchange_message(message)
    while state_monitor.status != 'TNOK':
       
        print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'TNOK', datetime.datetime.now()))
        time.sleep(0.1)


    # exchange_message_management.exchange_message_operator.state_monitor.cue_state = 'CUE'
    # while True:
    #     if exchange_message_management.exchange_message_operator.state_monitor.cue_state == 'CUE':
    #         stimulationController.run()
    #     else:
    #         time.sleep(0.1)
    #     event.clearEvents()
    while True:
        stimulationController.run()
        


