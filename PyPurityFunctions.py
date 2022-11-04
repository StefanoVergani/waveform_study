import os
import numpy as np
import statistics
import time
from datetime import datetime
import pickle
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
    def peak_finder_ave(path_raw,file_ending,polarity,path_output,file_size):
        peaks = []
        counter = 0
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            peak = 0
            if filename.startswith("Field_5.10.20Vcm_FibreIn_") and filename.endswith(file_ending):
                print(counter)
                waveList, timeList = ppt.getScopeWaveforms(path_raw+filename)
                timeList = None
                max_list = []
                for i in range(len(waveList)):  
                    if(polarity==1):
                        max_list.append(max(waveList[i]))
                    if(polarity==-1):
                        max_list.append(min(waveList[i]))
                        waveList[i]=None
                waveList = None
                peak = statistics.mean(max_list)
                max_list.clear()
                counter = counter +1
                peaks.append(peak)
                if counter == file_size and polarity==1:
                    print("I am now printing file ch3_peaks_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".npy")
                    with open(path_output+"ch3_peaks_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".npy",'wb') as f: pickle.dump(np.array(peaks), f)
                    counter=0
                    peaks.clear()
                if counter == file_size and polarity==-1:
                    print("I am now printing file ch4_peaks_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".npy")
                    with open("/home/svergani/waveform_study_results/2022_10_31/ch4_peaks_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".npy",'wb') as f: pickle.dump(np.array(peaks), f)
                    counter=0
                    peaks.clear()
        #return peaks
    
    @staticmethod            
    def specific_file_counter(path_raw,file_ending):
        peaks = []
        directory = os.fsencode(path_raw)
        counter = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("Field_5.10.20Vcm_FibreIn_") and filename.endswith(file_ending):
                counter = counter+1             
        return counter
    
    #I loop over all the files in path_dir_output
    @staticmethod            
    def file_collector(path_raw,file_type):
        peaks = []
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(file_type) and filename.endswith(".npy"):
                print("filename ", filename)
                temp = []
                with open(path_raw+filename, "rb") as fp:   #Pickling
                    temp=pickle.load(fp)
                for i in range(len(temp)):
                    peaks.append(temp[i])
                temp= None
        return peaks
