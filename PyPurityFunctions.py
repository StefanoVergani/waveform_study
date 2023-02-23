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
    def peak_finder_ave(path_raw,file_starting,file_ending,polarity,path_output,file_size):
        peaks = []
        counter = 0
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            peak = 0
            if filename.startswith(file_starting) and filename.endswith(file_ending):
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
                    with open(path_output+"ch4_peaks_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".npy",'wb') as f: pickle.dump(np.array(peaks), f)
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
    
    #I open the first waveform in the directory
    @staticmethod
    def first_waveform_check(path_raw,file_start,file_ending):
        counter = 0
        directory = os.fsencode(path_raw)
        for file in sorted(os.listdir(directory)):
            if counter == 0:
                filename = os.fsdecode(file)
                if filename.startswith(file_start) and filename.endswith(file_ending):
                    print("the file used is ",filename)
                    waveList, timeList = ppt.getScopeWaveforms(path_raw+filename)
                    counter = counter +1
                    return waveList
            if counter != 0:
                return 0
            
    #return the name of the first file in the directory
    @staticmethod
    def first_waveform_name(path_raw,file_start,file_ending):
        counter = 0
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            if counter == 0:
                filename = os.fsdecode(file)
                if filename.startswith(file_start) and filename.endswith(file_ending):
                    counter = counter +1
                    return filename
            if counter != 0:
                return 0            
            
    #I open the last waveform in the directory
    @staticmethod
    def waveform_check(path_raw,file_start,file_ending,value):
        filename_list = []
        directory = os.fsencode(path_raw)
        for file in sorted(os.listdir(directory)):
            filename = os.fsdecode(file)
            if filename.startswith(file_start) and filename.endswith(file_ending):
                filename_list.append(filename)
        if(value==1):
            filename_chosen = filename_list[len(filename_list)-1]
        if(value==0):
            filename_chosen = filename_list[0]
        print("the file used is ",filename_chosen)
        waveList, timeList = ppt.getScopeWaveforms(path_raw+filename_chosen)
        return waveList
    
    #return the name of the last file in the directory
    @staticmethod
    def waveform_name(path_raw,file_start,file_ending,value):
        filename_list = []
        directory = os.fsencode(path_raw)
        for file in sorted(os.listdir(directory)):
            filename = os.fsdecode(file)
            if filename.startswith(file_start) and filename.endswith(file_ending):
                filename_list.append(filename)
        if(value==1):
            filename_chosen = filename_list[len(filename_list)-1]
        if(value==0):
            filename_chosen = filename_list[0]
        return filename_chosen

    @staticmethod
    def waveform_averager(waveform):
        waveform_average=[]
        for i in range(len(waveform[0])):
            ave_temp = []
            for j in range(len(waveform)):
                ave_temp.append(waveform[j][i])
            waveform_average.append(sum(ave_temp)/len(ave_temp))
            ave_temp = None
        return waveform_average
    
    @staticmethod
    def waveform_averager_steps(waveform,initial,final):
        waveform_average=[]
        for i in range(len(waveform[0])):
            ave_temp = []
            for j in range(initial,final):
                ave_temp.append(waveform[j][i])
            waveform_average.append(sum(ave_temp)/len(ave_temp))
            ave_temp = None
        return waveform_average
    
    @staticmethod
    def smoothed_average(waveform,distance):
        waveform_smoothed=[]
        for i in range(0,len(waveform),distance):
            waveform_smoothed.append(sum(waveform[i:i+distance])/distance)
        return waveform_smoothed
           
            
            
    
            
                
