import os
import numpy as np
import statistics
from PyPurityTools import PyPurityTools as ppt


class PyPurityFunctions:

    @staticmethod            
    def file_extractor(path_raw, file_ending):
        list_name = []
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("Field_5.10.20Vcm_FibreIn_") and filename.endswith(file_ending):
                list_name.append(ppt.getScopeWaveforms(path_raw+filename))
                print("filename ", filename)
                print("np.array(list_name).shape ",np.array(list_name).shape)
        return list_name
    
    @staticmethod            
    def file_averager(path_raw, file_ending):
        mega_average = []
        directory = os.fsencode(path_raw)
        counter = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            average_list = []
            if filename.startswith("Field_5.10.20Vcm_FibreIn_") and filename.endswith(file_ending):
                waveList, timeList = ppt.getScopeWaveforms(path_raw+filename)
                for j in range(len(waveList[0])):
                    sum_list = 0
                    average = 0
                    for i in range(len(waveList)):
                        sum_list = sum_list + waveList[i][j] 
                        average = sum_list/len(waveList)
                    average_list.append(average)
                    
            mega_average.append(average_list) 
        return mega_average

    @staticmethod            
    def peak_finder_ave(path_raw,file_ending,polarity):
        peaks = []
        directory = os.fsencode(path_raw)
        counter = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            max_list = []
            if filename.startswith("Field_5.10.20Vcm_FibreIn_") and filename.endswith(file_ending):
                waveList, timeList = ppt.getScopeWaveforms(path_raw+filename)
                for i in range(len(waveList)):
                    if(polarity==1):
                        max_list.append(max(waveList[i]))
                    if(polarity==-1):
                        max_list.append(min(waveList[i]))
                peak = statistics.mean(max_list)
                peaks.append(peak)    
             
        return peaks