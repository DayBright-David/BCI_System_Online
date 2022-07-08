from numpy.lib.shape_base import column_stack
from StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from StimulationUICreator.BasicSchemaStimulationFramesFactory import BasicSchemaStimulationFramesFactory
from StimulationUICreator.SchemaStimulationFrames import SchemaStimulationFrames
from StimulationUICreator.StimTargetRect import StimTargetRect
from StimulationUICreator.Resource.fig2data import fig2data
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from psychopy import visual, core, event

import matplotlib
import copy
matplotlib.use('agg')


class SchemaStimulationFramesFactory(BasicSchemaStimulationFramesFactory):

    def initial(self, stimulation_ui_parameters):
        BasicSchemaStimulationFramesFactory.initial(
            self, stimulation_ui_parameters)

    def get_frames(self, target_table):
        frames = SchemaStimulationFrames()
        rowNUM = target_table['ROW']
        columnNUM = target_table['COL']
        targetNUM = rowNUM*columnNUM
        stimulation_frequency_set = np.array(
            target_table['FREQUENCY']).reshape((rowNUM, columnNUM))
        stimulation_phase_set = np.array(
            target_table['PHASE']).reshape((rowNUM, columnNUM))
        stim_rect_max_color = self.stimulation_ui_parameters.white
        char_set = np.array(target_table['DISPLAYCHAR']).reshape(
            (rowNUM, columnNUM))

        stimTargetRectSet = []
        stiNUM = len(stimulation_frequency_set)

        # 刺激大小

        interval = 50
        squareSize = 140
        current_stim_rect_size = [squareSize, squareSize]

        initHeight = (1080-(rowNUM*squareSize+(rowNUM-1)*interval))/2
        initWidth = (1920-(columnNUM*squareSize+(columnNUM-1)*interval))/2

        for rowINX, (freRow, phaseRow, charRow) in enumerate(zip(stimulation_frequency_set, stimulation_phase_set, char_set)):
            for colINX, (freq, phase, char) in enumerate(zip(freRow, phaseRow, charRow)):
                # 左下角
                target_site_point = [(colINX*(current_stim_rect_size[1]+interval)+initWidth), ((
                    rowNUM-rowINX-1)*(current_stim_rect_size[0]+interval)+initHeight)]

                stimTargetRectSet.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                         self.stimulation_ui_parameters.monitor_refresh_rate,
                                                         freq, phase, stim_rect_max_color, char))

        target_char_set = target_table['DISPLAYCHAR']
        # initial frames
        f0 = plt.figure(figsize=(19.20, 10.80), facecolor='none', dpi=100)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        plt.subplots_adjust(top=1, bottom=0, left=0,
                            right=1, hspace=0, wspace=0)

        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        initial_axis = plt.gca()

        # 聊天框
        init_x = initWidth
        init_y = initHeight+rowNUM*(current_stim_rect_size[0]+interval)-20

        init_len = columnNUM*(current_stim_rect_size[0]+interval)-interval
        init_height = 50

        stringPositions = [(init_x-1920/2+320), (init_y-1080/2-10)]

        f_0_frames = initial_axis
        for stimuli in stimTargetRectSet:
            brightness = 1
            rect = patches.Rectangle(
                (stimuli.site_point[0] / 1920, stimuli.site_point[1] / 1080),
                stimuli.rect_size[0] / 1920, stimuli.rect_size[1] / 1080,
                linewidth=1, facecolor=[brightness, brightness, brightness])

            # phase = (stimuli.start_phase/np.pi)
            # char = '%s pi'%phase
            v = plt.text(
                stimuli.site_point[0] / 1920 +
                (stimuli.rect_size[0] / 1920) / 2,
                stimuli.site_point[1] / 1080 +
                (stimuli.rect_size[1] / 1080) / 2,
                stimuli.char, fontsize=30, horizontalalignment='center', verticalalignment='center')
            f_0_frames.add_patch(rect)

        plt.axis('off')
        initial_frame = fig2data(f0)
        plt.close(f0)

        frameSet = []

        for N in range(0, self.stimulation_ui_parameters.max_preload_frames):
            f = plt.figure(figsize=(19.20, 10.80), facecolor='none', dpi=100)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, left=0,
                                right=1, hspace=0, wspace=0)

            # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

            current_axis = plt.gca()

            for stimuli in stimTargetRectSet:
                brightness = stimuli.cal_brightness(N)
                rect = patches.Rectangle((stimuli.site_point[0] / 1920, stimuli.site_point[1] / 1080),
                                         stimuli.rect_size[0] /
                                         1920, stimuli.rect_size[1] / 1080,
                                         linewidth=1, facecolor=[brightness, brightness, brightness])
                v = plt.text(stimuli.site_point[0] / 1920 + (stimuli.rect_size[0] / 1920) / 2,
                             stimuli.site_point[1] / 1080 +
                             (stimuli.rect_size[1] / 1080) / 2, stimuli.char,
                             fontsize=30, horizontalalignment='center', verticalalignment='center')
                current_axis.add_patch(rect)
            plt.axis('off')
            frameSet.append(fig2data(f))
            plt.close(f)

        frames.initial_frame = initial_frame
        frames.frameSet = frameSet
        frames.stimTargetRectSet = stimTargetRectSet
        frames.stringPositions = stringPositions

        return frames

