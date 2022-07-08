import numpy as np


class StimulationUIParameters():
    monitor_resolution = np.array([1920, 1080])
    monitor_refresh_rate = 144
    total_show_range = np.array([1, 1, 1920, 1080])
    targetRange = np.array([1, 1, 1920, 1080])
    max_preload_frames = 144
    base_framework_file = 'StimulationUICreator/Resource/baseFrameworkFile.png'
    stimulation_char_size = 30
    white = 255
    gray = 128
    black = 0


if __name__ == '__main__':
    t = StimulationUIParameters()
