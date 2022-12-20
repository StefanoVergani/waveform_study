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
waveform_ch3 = ppf.single_waveform_check(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch3.traces")
average_ch3=ppf.waveform_averager(waveform_ch3)
average_0_500_ch3=ppf.waveform_averager_steps(waveform_ch3,0,500)
average_500_1000_ch3=ppf.waveform_averager_steps(waveform_ch3,500,1000)
waveform_ch3_time=np.arange(len(waveform_ch3[0]))
print("CH3 DONE")

waveform_ch4 = ppf.single_waveform_check(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch4.traces")
average_ch4=ppf.waveform_averager(waveform_ch4)
average_0_500_ch4=ppf.waveform_averager_steps(waveform_ch4,0,500)
average_500_1000_ch4=ppf.waveform_averager_steps(waveform_ch4,500,1000)
waveform_ch4_time=np.arange(len(waveform_ch4[0]))
print("CH4 DONE")

bkg_ch3 = ppf.single_waveform_check(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch3.traces")
average_bkg_ch3=ppf.waveform_averager(bkg_ch3)
average_bkg_0_500_ch3=ppf.waveform_averager_steps(bkg_ch3,0,500)
average_bkg_500_1000_ch3=ppf.waveform_averager_steps(bkg_ch3,500,1000)
bkg_time_ch3=np.arange(len(bkg_ch3[0]))
print("CH3 BKG DONE")

bkg_ch4 = ppf.single_waveform_check(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch3.traces")
average_bkg_ch4=ppf.waveform_averager(bkg_ch4)
average_bkg_0_500_ch4=ppf.waveform_averager_steps(bkg_ch4,0,500)
average_bkg_500_1000_ch4=ppf.waveform_averager_steps(bkg_ch4,500,1000)
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

hf_target = h5.File("results_2022_12_20.hdf5", 'w')

hf_target.create_dataset('average_ch3', data=average_ch3)
hf_target.create_dataset('average_0_500_ch3', data=average_0_500_ch3)
hf_target.create_dataset('average_500_1000_ch3', data=average_500_1000_ch3)
hf_target.create_dataset('waveform_ch3_time', data=waveform_ch3_time)
hf_target.create_dataset('smoothed_ch3_ave', data=smoothed_ch3_ave)
hf_target.create_dataset('smoothed_ch3_time', data=smoothed_ch3_time)

hf_target.create_dataset('average_ch4', data=average_ch4)
hf_target.create_dataset('average_0_500_ch4', data=average_0_500_ch4)
hf_target.create_dataset('average_500_1000_ch4', data=average_500_1000_ch4)
hf_target.create_dataset('waveform_ch4_time', data=waveform_ch4_time)
hf_target.create_dataset('smoothed_ch4_ave', data=smoothed_ch4_ave)
hf_target.create_dataset('smoothed_ch4_time', data=smoothed_ch4_time)

hf_target.create_dataset('average_bkg_ch3', data=average_bkg_ch3)
hf_target.create_dataset('average_bkg_0_500_ch3', data=average_bkg_0_500_ch3)
hf_target.create_dataset('average_bkg_500_1000_ch3', data=average_bkg_500_1000_ch3)
hf_target.create_dataset('bkg_time_ch3', data=bkg_time_ch3)
hf_target.create_dataset('smoothed_ch3_bkg_ave', data=smoothed_ch3_bkg_ave)
hf_target.create_dataset('smoothed_ch3_bkg_time', data=smoothed_ch3_bkg_time)

hf_target.create_dataset('average_bkg_ch4', data=average_bkg_ch4)
hf_target.create_dataset('average_bkg_0_500_ch4', data=average_bkg_0_500_ch4)
hf_target.create_dataset('average_bkg_500_1000_ch4', data=average_bkg_500_1000_ch4)
hf_target.create_dataset('bkg_time_ch4', data=bkg_time_ch4)
hf_target.create_dataset('smoothed_ch4_bkg_ave', data=smoothed_ch4_bkg_ave)
hf_target.create_dataset('smoothed_ch4_bkg_time', data=smoothed_ch4_bkg_time)

hf_target.create_dataset('ave_clean_ch3',data=ave_clean_ch3)
hf_target.create_dataset('ave_clean_ch4',data=ave_clean_ch4)
hf_target.create_dataset('ave_clean_ch3_smooth',data=ave_clean_ch3_smooth)
hf_target.create_dataset('ave_clean_ch4_smooth',data=ave_clean_ch4_smooth)

hf_target.close()


#fig, ax = plt.subplots()
#ax.plot(waveform_ch3_time,average_ch3,label="Average over 1000 measurements")
#ax.plot(waveform_ch3_time,average_0_500_ch3,label="Average between measurements 0 - 500")
#ax.plot(waveform_ch3_time,average_500_1000_ch3,label="Average between measurements 500 - 1000")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average waveform for channel 3 ANODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(waveform_ch4_time,average_ch4,label="Average over 1000 measurements")
#ax.plot(waveform_ch4_time,average_0_500_ch4,label="Average between measurements 0 - 500")
#ax.plot(waveform_ch4_time,average_500_1000_ch4,label="Average between measurements 500 - 1000")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average waveform for channel 4 CATHODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(bkg_time_ch3,average_bkg_ch3,label="Average over 1000 measurements")
#ax.plot(bkg_time_ch3,average_bkg_0_500_ch3,label="Average between measurements 0 - 500")
#ax.plot(bkg_time_ch3,average_bkg_500_1000_ch3,label="Average between measurements 500 - 1000")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average background waveform for channel 3 ANODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(bkg_time_ch4,average_bkg_ch4,label="Average over 1000 measurements")
#ax.plot(bkg_time_ch4,average_bkg_0_500_ch4,label="Average between measurements 0 - 500")
#ax.plot(bkg_time_ch4,average_bkg_500_1000_ch4,label="Average between measurements 500 - 1000")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average background waveform for channel 4 CATHODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(smoothed_ch3__bkg_time,smoothed_ch3_ave,label="Smoothed CH3 average 10 steps")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average waveform for channel 3 ANODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(smoothed_ch4_time,smoothed_ch4_time_ave,label="Smoothed CH4 average 10 steps")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An smoothed average waveform for channel 4 CATHODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(smoothed_ch3_bkg_time,smoothed_ch3_bkg_ave,label="Smoothed CH3 BKG average 10 steps")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average background waveform for channel 3 ANODE")
#ax.legend()

#fig, ax = plt.subplots()
#ax.plot(smoothed_ch4_bkg_time,smoothed_ch4_bkg_ave,label="Smoothed CH4 BKG average 10 steps")
#ax.set_xlabel("Measurement [a.u.]")
#ax.set_ylabel("Voltage [Volts]")
#ax.set_title("An average background waveform for channel 4 CATHODE")
#ax.legend()


