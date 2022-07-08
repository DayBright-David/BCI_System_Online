class StateMonitor:
    def __init__(self):
        self.resultString = None
        self.status = None
        self.cal_time = None
        self.result_id = None

        self.cue_state = 'CUE'
        self.trainEnd = 'FreeSpelling'
