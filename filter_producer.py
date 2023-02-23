from PyPurityTools import PyPurityTools as ppt
from PyPurityFunctions import PyPurityFunctions as ppf
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import savgol_filter
import matplotlib.style
import matplotlib as mpl
import math
import scipy.fftpack
from scipy.signal import butter,filtfilt
import scipy.fftpack
import os
import statistics
import h5py as h5

path_dir: str = r"/unix/dune/purity/2022October14Vacuum/Gold/"
    
print("starting")
#we know that each wavefor is 1000 measurements
#filename_ch3 = ppf.waveform_name(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch3.traces",0)
#waveform_ch3 = ppf.waveform_check(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch3.traces",0)
filename_ch3="Field_5.10.20Vcm_FibreIn_19.19.ch3.traces"
waveform_ch3, timeList = ppt.getScopeWaveforms(path_dir+filename_ch3)
average_ch3=ppf.waveform_averager(waveform_ch3)
#average_0_500_ch3=ppf.waveform_averager_steps(waveform_ch3,0,500)
#average_500_1000_ch3=ppf.waveform_averager_steps(waveform_ch3,500,1000)
average_0_100_ch3=ppf.waveform_averager_steps(waveform_ch3,0,100)
average_900_1000_ch3=ppf.waveform_averager_steps(waveform_ch3,900,1000)
waveform_ch3_time=np.arange(len(waveform_ch3[0]))
print("CH3 DONE")

#filename_ch4 = ppf.waveform_name(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch4.traces",0)
#waveform_ch4 = ppf.waveform_check(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch4.traces",0)
filename_ch4="Field_5.10.20Vcm_FibreIn_19.19.ch4.traces"
waveform_ch4, timeList = ppt.getScopeWaveforms(path_dir+filename_ch4)
average_ch4=ppf.waveform_averager(waveform_ch4)
#average_0_500_ch4=ppf.waveform_averager_steps(waveform_ch4,0,500)
#average_500_1000_ch4=ppf.waveform_averager_steps(waveform_ch4,500,1000)
average_0_100_ch4=ppf.waveform_averager_steps(waveform_ch4,0,100)
average_900_1000_ch4=ppf.waveform_averager_steps(waveform_ch4,900,1000)
waveform_ch4_time=np.arange(len(waveform_ch4[0]))
print("CH4 DONE")

filename_bkg_ch3 = ppf.waveform_name(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch3.traces",0)
bkg_ch3 = ppf.waveform_check(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch3.traces",0)
average_bkg_ch3=ppf.waveform_averager(bkg_ch3)
#average_bkg_0_500_ch3=ppf.waveform_averager_steps(bkg_ch3,0,500)
#average_bkg_500_1000_ch3=ppf.waveform_averager_steps(bkg_ch3,500,1000)
average_bkg_0_100_ch3=ppf.waveform_averager_steps(bkg_ch3,0,100)
average_bkg_900_1000_ch3=ppf.waveform_averager_steps(bkg_ch3,900,1000)
bkg_time_ch3=np.arange(len(bkg_ch3[0]))
print("CH3 BKG DONE")

filename_bkg_ch4 = ppf.waveform_name(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch4.traces",0)
bkg_ch4 = ppf.waveform_check(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch4.traces",0)
average_bkg_ch4=ppf.waveform_averager(bkg_ch4)
#average_bkg_0_500_ch4=ppf.waveform_averager_steps(bkg_ch4,0,500)
#average_bkg_500_1000_ch4=ppf.waveform_averager_steps(bkg_ch4,500,1000)
average_bkg_0_100_ch4=ppf.waveform_averager_steps(bkg_ch4,0,100)
average_bkg_900_1000_ch4=ppf.waveform_averager_steps(bkg_ch4,900,1000)
bkg_time_ch4=np.arange(len(bkg_ch4[0]))
print("CH4 BKG DONE")

smoothed_ch3_ave=ppf.smoothed_average(average_ch3,10)
smoothed_ch4_ave=ppf.smoothed_average(average_ch4,10)
smoothed_ch3_bkg_ave=ppf.smoothed_average(average_bkg_ch3,10)
smoothed_ch4_bkg_ave=ppf.smoothed_average(average_bkg_ch4,10)
smoothed_ch3_time=np.arange(len(smoothed_ch3_ave))
smoothed_ch4_time=np.arange(len(smoothed_ch4_ave))
smoothed_ch3_bkg_time=np.arange(len(smoothed_ch3_bkg_ave))
smoothed_ch4_bkg_time=np.arange(len(smoothed_ch4_bkg_ave))
print("SMOOTHED DONE")

####cleaning before smoothing

ave_clean_ch3=[]
for i in range(len(average_ch3)):
    ave_clean_ch3.append(average_ch3[i]-average_bkg_ch3[i])
    
ave_clean_ch4=[]
for i in range(len(average_ch4)):
    ave_clean_ch4.append(average_ch4[i]-average_bkg_ch4[i])
    
###cleaning after smoothing

ave_clean_ch3_smooth=[]
for i in range(len(smoothed_ch3_ave)):
    ave_clean_ch3_smooth.append(smoothed_ch3_ave[i]-smoothed_ch3_bkg_ave[i])
    
ave_clean_ch4_smooth=[]
for i in range(len(smoothed_ch4_ave)):
    ave_clean_ch4_smooth.append(smoothed_ch4_ave[i]-smoothed_ch4_bkg_ave[i])

print("starting to save")

hf_target = h5.File("results_2023_02_02_19_19_waveform.hdf5", 'w')

hf_target.create_dataset('filename_ch3', data=filename_ch3)
hf_target.create_dataset('filename_ch4', data=filename_ch4)
hf_target.create_dataset('filename_bkg_ch3', data=filename_bkg_ch3)
hf_target.create_dataset('filename_bkg_ch4', data=filename_bkg_ch4)

hf_target.create_dataset('average_ch3', data=average_ch3)
#hf_target.create_dataset('average_0_500_ch3', data=average_0_500_ch3)
#hf_target.create_dataset('average_500_1000_ch3', data=average_500_1000_ch3)
hf_target.create_dataset('average_0_100_ch3', data=average_0_100_ch3)
hf_target.create_dataset('average_900_1000_ch3', data=average_900_1000_ch3)
hf_target.create_dataset('waveform_ch3_time', data=waveform_ch3_time)
hf_target.create_dataset('smoothed_ch3_ave', data=smoothed_ch3_ave)
hf_target.create_dataset('smoothed_ch3_time', data=smoothed_ch3_time)

hf_target.create_dataset('average_ch4', data=average_ch4)
#hf_target.create_dataset('average_0_500_ch4', data=average_0_500_ch4)
#hf_target.create_dataset('average_500_1000_ch4', data=average_500_1000_ch4)
hf_target.create_dataset('average_0_100_ch4', data=average_0_100_ch4)
hf_target.create_dataset('average_900_1000_ch4', data=average_900_1000_ch4)
hf_target.create_dataset('waveform_ch4_time', data=waveform_ch4_time)
hf_target.create_dataset('smoothed_ch4_ave', data=smoothed_ch4_ave)
hf_target.create_dataset('smoothed_ch4_time', data=smoothed_ch4_time)

hf_target.create_dataset('average_bkg_ch3', data=average_bkg_ch3)
#hf_target.create_dataset('average_bkg_0_500_ch3', data=average_bkg_0_500_ch3)
#hf_target.create_dataset('average_bkg_500_1000_ch3', data=average_bkg_500_1000_ch3)
hf_target.create_dataset('average_bkg_0_100_ch3', data=average_bkg_0_100_ch3)
hf_target.create_dataset('average_bkg_900_1000_ch3', data=average_bkg_900_1000_ch3)
hf_target.create_dataset('bkg_time_ch3', data=bkg_time_ch3)
hf_target.create_dataset('smoothed_ch3_bkg_ave', data=smoothed_ch3_bkg_ave)
hf_target.create_dataset('smoothed_ch3_bkg_time', data=smoothed_ch3_bkg_time)

hf_target.create_dataset('average_bkg_ch4', data=average_bkg_ch4)
#hf_target.create_dataset('average_bkg_0_500_ch4', data=average_bkg_0_500_ch4)
#hf_target.create_dataset('average_bkg_500_1000_ch4', data=average_bkg_500_1000_ch4)
hf_target.create_dataset('average_bkg_0_100_ch4', data=average_bkg_0_100_ch4)
hf_target.create_dataset('average_bkg_900_1000_ch4', data=average_bkg_900_1000_ch4)
hf_target.create_dataset('bkg_time_ch4', data=bkg_time_ch4)
hf_target.create_dataset('smoothed_ch4_bkg_ave', data=smoothed_ch4_bkg_ave)
hf_target.create_dataset('smoothed_ch4_bkg_time', data=smoothed_ch4_bkg_time)

hf_target.create_dataset('ave_clean_ch3',data=ave_clean_ch3)
hf_target.create_dataset('ave_clean_ch4',data=ave_clean_ch4)
hf_target.create_dataset('ave_clean_ch3_smooth',data=ave_clean_ch3_smooth)
hf_target.create_dataset('ave_clean_ch4_smooth',data=ave_clean_ch4_smooth)

hf_target.close()

print("finished")


