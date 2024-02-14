# It tests if data of time frames follow powerlaw distribution. Lenght of time frames is given by parameter t_delta.
# It uses whole dataset and dataset cutted on treshold 935 ms. That is 95th percentile.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create interarrival times
# Data file needed: "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv"
# It creates files: e.g. "BTCUSDT_powerlaw_dist_5min.csv"

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy import stats

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03-interarrivalTimes.csv'
result_path = 'BTCUSDT_powerlaw_dist_5min.csv'
t_delta = timedelta(minutes=5) # it determines the timeframe
treshold = 935 # where to cut data, 95th percentil
alphas = {0.05} # {0.05, 0.01, 0.001}, confidence interval
bounds =  [(0, 10), (0, 10)] # bounds for fitting distribution
start_date = datetime(2022, 1, 3, 0, 0, 0) # the datetime of beginning of file
end_date = start_date + t_delta
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
    part = data[(data['Datetime'] > start_date) & (data['Datetime'] < end_date)]
    iat_w = np.array(part['time_difference'].values)
    part_treshold = part[part['time_difference'] < treshold]
    iat_t = np.array(part_treshold['time_difference'].values)

    dist_w = stats.fit(stats.powerlaw, iat_w, bounds = bounds)
    dist_t = stats.fit(stats.powerlaw, iat_t, bounds = bounds)
    
    # H0 -> distributions are identical
    ktest_w = stats.ks_1samp(x=iat_w, cdf=stats.powerlaw.cdf, args=(dist_w.params.a, dist_w.params.loc, dist_w.params.scale))
    ktest_t = stats.ks_1samp(x=iat_t, cdf=stats.powerlaw.cdf, args=(dist_t.params.a, dist_t.params.loc, dist_t.params.scale))

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


