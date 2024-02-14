# Script for the figure " Q-Q plots of the best-fitted distributions" in the thesis.
# Plots 4 qq-plots. Data: Tick-whole, Tick-treshold, Binance-whole, Binance-treshold data.
# For each data one distribution of the best fitted distribution from file: "distfit_distributions_80.py".
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "distfit_distributions_80.py" and see Data_preprocessing how to create interarrival times for Tick and Binance data.
# Data file needed: "EURUSD_2019_01_03_interarrivalTimes.csv" and "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv".
# It creates files: the result need to saved manually into png, pdf doesn't work.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs
import statsmodels.api as sm

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path_T = 'EURUSD_2019_01_03_interarrivalTimes.csv'
data_path_B = 'BTCUSDT-trades-2022-01-03-interarrivalTimes.csv'
treshold_T = 2000
treshold_B = 935
# --------------------------------------------------------------------------------------------------

def cut_data(treshold, data):
   cutted = list()
   lenght = data.size
   for i in range(0, lenght):
      if data[i] <= treshold:
        cutted.append(data[i])
   
   return np.array(cutted)


# Data preparation
T_data= pd.read_csv(data_path_T, header=0, index_col='ID', parse_dates=['Datetime'])
B_data = pd.read_csv(data_path_B, header=0, index_col='myID')
T_diff_num_ms = np.array(T_data['Difference_number[ms]'].values)
B_diff_num_ms = np.array(B_data['time_difference'].values)
T_cutted = cut_data(treshold_T, T_diff_num_ms)
B_cutted = cut_data(treshold_B, B_diff_num_ms)

# Plots
fig, ax = plt.subplots(nrows=2, ncols=2)

setting = {'alpha': 0.5,
            'markersize': 15,
            'markerfacecolor': 'darkblue',
            'markeredgewidth': 0.5,
            'markeredgecolor': '#000000',
            'marker': '.'}


# T - whole
sm.qqplot(T_diff_num_ms, scs.t, fit=True, line='45', ax=ax[0,0], **setting)
ax[0,0].set_title('Tick, Student\'s')
ax[0,0].grid(True)

# T - treshold
sm.qqplot(T_cutted, scs.dweibull, fit=True, line='45', ax=ax[0,1], **setting)
ax[0,1].set_title('Tick, Double Weibull')
ax[0,1].grid(True)

# B - whole
sm.qqplot(B_diff_num_ms, scs.genextreme, fit=True, line='45', ax=ax[1,0], **setting)
ax[1,0].set_title('Binance, Generalized extreme value')
ax[1,0].grid(True)

# B - treshold
sm.qqplot(B_cutted, scs.loglaplace, fit=True, line='45', ax=ax[1,1], **setting)
ax[1,1].set_title('Binance, Log-Laplace')
ax[1,1].grid(True)


plt.tight_layout()

plt.show()




