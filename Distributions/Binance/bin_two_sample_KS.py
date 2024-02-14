# It tests if data of time frames t+1 and t have the same distribution with use of KS two-sample test.
# It uses whole dataset and dataset cutted on treshold 935 ms. That is 95th percentile.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create Binance interarrival times
# Data file needed: "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv"
# It creates files: e.g. "BTCUSDT_same_dist_5min_2KS.csv"

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy import stats

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03-interarrivalTimes.csv'
result_path = 'BTCUSDT_same_dist_5min_2KS.csv'
t_delta = timedelta(minutes=5) # it determines the timeframe
treshold = 935 # where to cut data, 95th percentil
alphas = {0.05} # {0.05, 0.01, 0.001}, confidence interval
bounds =  [(0, 10), (0, 10)] # bounds for fitting distribution
start_date = datetime(2022, 1, 3, 0, 0, 0) + t_delta # the datetime of beginning of file + t_delta
end_date = datetime(2022, 1, 3, 0, 0, 0) + t_delta + t_delta
# --------------------------------------------------------------------------------------------------

data = pd.read_csv(data_path, header=0, index_col='myID', parse_dates=['Datetime'])
results = pd.DataFrame(columns=['Time frame', 'alpha', 'pvalue_w', 'reject the null_w', 'pvalue_t', 'reject the null_t'])  #3 rows for one tframe
data_end = data['Datetime'].iloc[-1]

df_counter = 0
rej_counter_w = 0
cannot_counter_w = 0
rej_counter_t = 0
cannot_counter_t = 0

while(start_date < data_end):
    # data first time frame
    part = data[(data['Datetime'] > (start_date - t_delta)) & (data['Datetime'] < (end_date - t_delta))]
    iat1_w = np.array(part['time_difference'].values)
    part_treshold = part[part['time_difference'] < treshold]
    iat1_t = np.array(part_treshold['time_difference'].values)
    
    # data second time frame
    part = data[(data['Datetime'] > start_date) & (data['Datetime'] < end_date)]
    iat2_w = np.array(part['time_difference'].values)
    part_treshold = part[part['time_difference'] < treshold]
    iat2_t = np.array(part_treshold['time_difference'].values)

    # H0 -> distributions are identical
    ktest_w = stats.ks_2samp(data1=iat1_w, data2=iat2_w)
    ktest_t = stats.ks_2samp(data1=iat1_t, data2=iat2_t)

    # If there is more alphas ...
    for alpha in alphas:
        # both reject 
        if ((ktest_w.pvalue < alpha) and (ktest_t.pvalue < alpha)):
            results.loc[df_counter] = [start_date.strftime("%H:%M"), alpha, ktest_w.pvalue, 'REJECT', ktest_t.pvalue, 'REJECT']
            rej_counter_w += 1
            rej_counter_t += 1
        # both cannot reject
        elif ((ktest_w.pvalue > alpha) and (ktest_t.pvalue > alpha)):
            results.loc[df_counter] = [start_date.strftime("%H:%M"), alpha, ktest_w.pvalue, 'CANNOT REJECT', ktest_t.pvalue, 'CANNOT REJECT']
            cannot_counter_w += 1
            cannot_counter_t +=1

        # w - REJECT and t - CANNOT
        elif ((ktest_w.pvalue < alpha) and (ktest_t.pvalue > alpha)):
            results.loc[df_counter] = [start_date.strftime("%H:%M"), alpha, ktest_w.pvalue, 'REJECT', ktest_t.pvalue, 'CANNOT REJECT']
            rej_counter_w += 1
            cannot_counter_t += 1
        # w - CANNOT and t -REJECT
        elif ((ktest_w.pvalue > alpha) and (ktest_t.pvalue < alpha)):
            results.loc[df_counter] = [start_date.strftime("%H:%M"), alpha, ktest_w.pvalue, 'CANNOT REJECT', ktest_t.pvalue, 'REJECT']
            cannot_counter_w += 1
            rej_counter_t += 1

        df_counter += 1

    start_date += t_delta
    end_date += t_delta


results.to_csv(result_path)

print('W - rejected: ', rej_counter_w, '/', (cannot_counter_w + rej_counter_w))
print('T - rejected: ', rej_counter_t, '/', (rej_counter_t + cannot_counter_t))
