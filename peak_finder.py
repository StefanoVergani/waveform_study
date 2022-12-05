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

path_dir: str = r"/unix/dune/purity/2022October14Vacuum/Gold/"
path_dir_output: str =r"/home/svergani/waveform_study_results/2022_12_05/"
#the third argument is polarity. It is +1 if the waveform has a positive peak, -1 if negative.
#ppf.peak_finder_ave(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch3.traces",1,path_dir_output,20)
#ppf.peak_finder_ave(path_dir,"Field_5.10.20Vcm_FibreIn_",".ch4.traces",-1,path_dir_output,20)
ppf.peak_finder_ave(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch3.traces",1,path_dir_output,1)
ppf.peak_finder_ave(path_dir,"Field_5.10.20Vcm_FibreOut_HVOn",".ch4.traces",-1,path_dir_output,1)