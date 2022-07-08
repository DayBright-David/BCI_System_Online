from ExperimentInfomation.ExperimentInformation import ExperimentInformation
from ExperimentInfomation.displayUIsetting import displayUIsetting
import numpy as np
import math
from scipy import signal
import random


def create_experiment_information(personID,paradigm_name,user_folder_path):

    experiment_information = ExperimentInformation()

    experiment_information.save_path = user_folder_path + '/' + paradigm_name + '.mat'

    experiment_information.personID = int(personID)

    experiment_information.frame_rate = 60

    experiment_information.targetNUM = 40

    cueOrder = np.arange(0,experiment_information.targetNUM-20) 

    random.shuffle(cueOrder)

    experiment_information.blockNUM = 1

    experiment_information.cues = np.tile(cueOrder,experiment_information.blockNUM).tolist()

    experiment_information.stimulation_max_time = 5

    experiment_information.prepare_last_time = 0.5

    experiment_information.finish_last_time = 0.5

    experiment_information.stimulation_frequency_set = np.linspace(8.0, 15.8, 40)

    experiment_information.stimulation_phase_set = np.tile(np.arange(0,2,0.5)*math.pi,10)

    schema_process_information = displayUIsetting()

    experiment_information.schema_process_information = schema_process_information

    experiment_information.channel_no = 10

    experiment_information.frequency_sample = 1000

    experiment_information.down_frequency_sample = 250

    experiment_information.multiplicate_time = 5

    experiment_information.window_step_time = 0.12

    experiment_information.max_window_time = 6

    experiment_information.offset_time = 0

    experiment_information.equalizer_order = [4, 6]

    experiment_information.threshold = 1e-7

    experiment_information.min_detection_window_layer = 8

    experiment_information.continuous_detection_window_layer = 8

    experiment_information.equalizer_update_time = 10

    experiment_information.equalizer_estimate_time = 50

    experiment_information.winLen = 3

    experiment_information.model_dir = 'DataPool/models'

    experiment_information.dataset_dir = 'DataPool/datasets'

    experiment_information.data_dir = 'DataPool/data'

    experiment_information.CvINX = '0'

    experiment_information.k = 5

    experiment_information.topNUM = 5

    experiment_information.step = [40,30,20,10,10,10]

    experiment_information.recordGap = 40



    
    return experiment_information





