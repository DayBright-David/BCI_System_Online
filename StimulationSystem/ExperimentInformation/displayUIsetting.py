from ExperimentInfomation.SchemaProcessInformation import SchemaProcessInformation
import numpy as np
import math
import string


def displayUIsetting():


    display_char_set = list(string.ascii_uppercase)+list(np.arange(10))+['.',' ',',','Del']

    uav_command_id = list(np.arange(1,41))

    total_frequency = np.linspace(8.0, 15.8, 40)

    total_phase = np.tile(np.arange(0,2,0.5)*math.pi,10)

    schema_process_information = SchemaProcessInformation()
    schema_process_information.targetTable = { 'ID':list(range(1,11)),
                                                'UAVCOMMANDID':uav_command_id,
                                                'DISPLAYCHAR': display_char_set,
                                                'FREQUENCY': total_frequency,
                                                'PHASE': total_phase }
    return schema_process_information

