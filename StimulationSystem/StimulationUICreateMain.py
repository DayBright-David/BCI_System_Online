import sys
sys.path.append('..')
sys.path.append('.')

sys.path.append('../..')
from CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from StimulationSystem.StimulationUICreator.Singleton.SingletonStimulationUIFactory import factory_StimulationUIFactory
from StimulationSystem.StimulationUICreator.Singleton.SingletonSchemaStimulationFramesFactory import factory_SchemaStimulationFramesFactory
from StimulationSystem.ParadigmConfig.ParadigmConfig import ParadigmConfig
import matplotlib.pyplot as plt
import datetime
import  os
import pickle
from tqdm import tqdm

folder_path = os.getcwd()
paradigm_name = 'adaptiveOnline'

if not os.path.exists(folder_path+'/stimulationInformationFolder'):
    os.makedirs(folder_path+'/stimulationInformationFolder')

if not os.path.exists(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name):
    os.makedirs(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name)

paradigm_folder_path = folder_path+'/stimulationInformationFolder'+'/'+paradigm_name
personID = 0
experiment_information = create_experiment_information(personID,paradigm_name, paradigm_folder_path)

factory = factory_StimulationUIFactory

factory.initial(factory_SchemaStimulationFramesFactory)

background_frame = factory.get_background_frame()

stimulation_frames = factory.get_stimulation_frame(experiment_information.schema_process_information.targetTable)

paradigm_config = ParadigmConfig()
paradigm_config.paradigm_name = paradigm_name
paradigm_config.save_time = datetime.datetime.now()
paradigm_config.background_frame_path= background_frame

#paradigm_config.stimulation_frames_path = []

for num in range(0, len(stimulation_frames)):
    frames_temp = []
    path = folder_path + '/stimulationInformationFolder' + '/' + paradigm_name + '/' +str(num)
    if not os.path.exists(path):
        os.makedirs(path)
    plt.imsave(path + '/initial_frame.png', stimulation_frames[num].initial_frame)
    frames_temp.append(path + '/initial_frame.png')
    for frame in tqdm(range(0, len(stimulation_frames[num].frameSet))):
        frames_temp.append(path + '/' + str(frame) + '.png')
        plt.imsave(path + '/' + str(frame) + '.png', stimulation_frames[num].frameSet[frame])

    paradigm_config.stimulation_frames_path.append(frames_temp)
    paradigm_config.stimTargetRectSet.append(stimulation_frames[num].stimTargetRectSet)
    paradigm_config.stringPositions.append(stimulation_frames[num].stringPositions)

a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'wb')
pickle.dump(paradigm_config, a_file)
a_file.close()
a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'rb')
output = pickle.load(a_file)
print(output)

