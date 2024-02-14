# It is finding which distribution data fits. It uses 80 distributions.
# In dataset there are only trades, where there is change in price.
# It can use Freedman–Diaconis rule to determine number of bins.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create interarrival times for Tick and Binance data.
# Data file needed: "EURUSD_2019_01_03_interarrivalTimes.csv" or "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv"
# It creates files: e.g. "IAT_fitter_80_distributions_IQR.csv" or "BTCUSDT_IAT_fitter_80_distributions_IQR.csv"

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from fitter import Fitter, get_distributions
import time
import math
from scipy.stats import iqr

start = time.time()

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_interarrivalTimes.csv'
result_path = 'IAT_fitter_80_distributions_IQR.csv'
tick = True # Tick data = True, Binance data = False
treshold = 2000 # Tick = 2000, Binance = 935 ms
n_best = 10 # how many best distributions to write into file
timeout = 2000 # timeout for fitting one distribution in seconds
# --------------------------------------------------------------------------------------------------

def fit(datas, distributions, bins, n_best):
   f = Fitter(data=datas, distributions=distributions, timeout=timeout, bins=bins)
   f.fit(progress=True)
   return (f.summary(n_best), f.get_best(method='sumsquare_error'))

def cut_data(datas, treshold):
   cutted = list()
   lenght = datas.size
   for i in range(0, lenght):
      if datas[i] <= treshold:
        cutted.append(datas[i])
   
   return np.array(cutted)

def count_bins(datas):
   lenght = datas.size
   h = 2 * iqr(datas) / math.pow(lenght, 1/3) # bin width
   b = (datas.max() - datas.min()) / h
   return [math.ceil(b)] # round up, integer in list

# Data prepare
if tick == True:
   data = pd.read_csv(data_path, header=0, index_col='ID', parse_dates=['Datetime'])
   diff_num_ms = np.array(data['Difference_number[ms]'].values)
else:
   data = pd.read_csv(data_path, header=0, index_col='myID', parse_dates=['Datetime'])
   diff_num_ms = np.array(data['time_difference'].values)
diff_num_ms_cutted = cut_data(diff_num_ms, treshold)

# Number of bins
wbins = count_bins(diff_num_ms) # bins for whole data
pbins = count_bins(diff_num_ms_cutted) # bins for cutted data
# If we want to define by hand
# wbins = [25, 50, 100, 300, 500,1000,1500,2000]
# pbins = [25, 50, 100, 300, 500,1000,1500,2000]

wsum = dict()  # whole data
wbest = dict()
psum = dict()  # part of data
pbest = dict()

dist = get_distributions()
# whole data
for b in wbins:
   wsum[b], wbest[b] = fit(diff_num_ms, dist, b, n_best)

# tresold data
for b in pbins:
   psum[b], pbest[b] = fit(diff_num_ms_cutted, dist, b, n_best)


# writing results to a file --------------------------------------------
with open(result_path, 'w') as file:
   file.write("-------------------------------------------------------------------------\n")
   file.write("80 distributions\n")
   file.write("-------------------------------------------------------------------------\n")
   # whole data
   for b in wbins:
      file.write("\nWhole data - BINS %s\n" %b) 
      file.write("Best fitted distribution: ")
      writer = csv.writer(file)
      for key, value in wbest[b].items():
         writer.writerow([key, value])
      file.write("Best five:\n")
      wsum[b].to_csv(file)
   # 2s data
   for b in pbins:
      file.write("\n2 seconds data - BINS %s\n" %b)  
      file.write("Best fitted distribution: ")
      writer = csv.writer(file)
      for key, value in pbest[b].items():
         writer.writerow([key, value])
      file.write("Best five:\n")
      psum[b].to_csv(file)

end = time.time()

print('Elapsed time: ', (end-start)/60, ' min')