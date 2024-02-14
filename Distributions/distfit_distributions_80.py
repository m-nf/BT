# It is finding which distribution data fits. It uses 80 distributions.
# In dataset there are only trades, where there is change in price.
# It can use Freedman–Diaconis rule to determine number of bins.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create interarrival times for Tick and Binance data.
# Data file needed: "EURUSD_2019_01_03_interarrivalTimes.csv" or "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv"
# It creates files: e.g. "IAT_distfit_80_distributions_IQR.csv" or "BTCUSDT_IAT_distfit_80_distributions_IQR.csv"

from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from scipy.stats import iqr

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_interarrivalTimes.csv'
result_path = 'IAT_distfit_80_distributions_IQR.csv'
tick = True # Tick data = True, Binance data = False
treshold = 2000 # Tick = 2000, Binance = 935 ms
n_best = 10 # how many best distributions to write into file
# --------------------------------------------------------------------------------------------------

start = time.time()

def cut_data(datas, treshold):
   cutted = list()
   lenght = datas.size
   for i in range(0, lenght):
      if datas[i] <= treshold:
        cutted.append(datas[i])
   
   return np.array(cutted)

def count_bins(datas):
   lenght = datas.size
   h = 2 * iqr(datas) / math.pow(lenght, 1/3) # bin width Freedman-Diaconis rule
   b = (datas.max() - datas.min()) / h
   return math.ceil(b) # round up, integer in list

# Data prepare
if tick == True:
   data = pd.read_csv(data_path, header=0, index_col='ID', parse_dates=['Datetime'])
   diff_num_ms = np.array(data['Difference_number[ms]'].values)
else:
   data = pd.read_csv(data_path, header=0, index_col='myID', parse_dates=['Datetime'])
   diff_num_ms = np.array(data['time_difference'].values)
cutted = cut_data(diff_num_ms, treshold)

# Whole data
wbins = count_bins(diff_num_ms)
dist = distfit(distr='full', method='parametric', bins=wbins, stats='RSS')
dist.fit_transform(diff_num_ms)
sum_whole = dist.summary[0:n_best]
#dist.qqplot(diff_num_ms, n_top=3)
#plt.show()

# treshold data
pbins = count_bins(cutted)
dist = distfit(distr='full', method='parametric', bins=pbins, stats='RSS')
dist.fit_transform(cutted)
sum_cut = dist.summary[0:n_best]
#dist.qqplot(cutted, n_top=3)
#plt.show()

# writing results to a file --------------------------------------------
with open(result_path, 'w') as file:
   file.write("-------------------------------------------------------------------------\n")
   file.write("80 distributions\n")
   file.write("-------------------------------------------------------------------------\n")
   file.write("\nWhole data - BINS %s\n" % wbins) 
   sum_whole.to_csv(file, mode='a')

   file.write("\n2 seconds data - BINS %s\n" % pbins)
   sum_cut.to_csv(file, mode='a')

end = time.time()

print('Elapsed time: ', end-start, ' s')


