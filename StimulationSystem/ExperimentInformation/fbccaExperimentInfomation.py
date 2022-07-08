from ExperimentInformation import ExperimentInformation


class fbccaExperimentInformation(ExperimentInformation):
    def __init__(self):
        self.channel_no = None
        self.frequency_sample = None
        self.down_frequency_sample = None
        self.multiplicate_time = None

        self.window_step_time = None
        self.max_window_time = None
        self.offset_time = None
        self.equalizer_order = None
        self.threshold = None
        self.min_detection_window_layer = None
        self.continuous_detection_window_layer = None
        self.equalizer_update_time = None
        self.equalizer_estimate_time = None
        self.winLen = None

        # 选择参数
        self.model_dir = None
        self.k = None
        self.threshold = None





        
