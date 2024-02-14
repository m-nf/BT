# It fits ARIMA model to data of time frames of different lenght. Data of specific time frame are randomly
# chosen from a day 10 times.
# I.e. time frame 30 min ~ 5000 trades, it randomly chooses data from 70000:75000, then fits, repeats 10 times.
# Time frames are given according to trades per time, here must be typed manually. Whole day is fitted in Notebooks.

# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "trades_per_time_mean.py" and see Data_preprocessing how to get needed files.
# Data file needed: "EURUSD_2019_01_03_without-ID.csv" or "BTCUSDT-trades-2022-01-03_parsedDate.csv".
# It creates files: e.g. "EURUSD_arima_exhFit_table.csv".

import pandas as pd
import numpy as np
import pmdarima as pm
import random as rnd
import statsmodels.stats as sms
import time

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_without-ID.csv' # 'BTCUSDT-trades-2022-01-03_parsedDate.csv'
result_path = 'EURUSD_arima_exhFit_table.csv' # 'BTC_arima_exhFit_table.csv'
tick = True # Tick data = True, Binance data = False
times = dict({30:3635, 60:7270, 720:87240}) # In seconds for Binance dict({30:18450, 60:36901, 720:442812})
# Further parameters need to be set in function "pm.auto_arima()".
# --------------------------------------------------------------------------------------------------

t_start = time.time()

if tick == True:
    data = pd.read_csv(data_path, header=0, index_col=None, parse_dates=['Datetime'])
    data = data['Middle']
else:
    data = pd.read_csv(data_path, header=0, index_col='myID', parse_dates=['Datetime'])
    data = data['price']

data_lenght = len(data.index)
lrets = np.log(data/data.shift(1)).fillna(0)

results = pd.DataFrame(columns=['Time frame', 'Order', 'Number of orders', 'Number of valid fits'])
df_counter = 0

for t in times:
    # Process info
    print(t)
    print('Elapsed time: ', time.time() - t_start)

    for i in range(0,10):
        # Choose random part of day with exact leght
        rnd_index = rnd.randint(1, data_lenght - times[t]) # 1, because lrets[0] is always 0
        lrets_part = lrets[rnd_index : rnd_index + times[t]]
        
        # Find the best order
        mdl = pm.auto_arima(y=lrets_part, 
                     start_p=2, 
                     d=None, 
                     start_q=2, 
                     max_p=5,
                     max_d=2, 
                     max_q=5, 
                     max_order=12,
                     stepwise=True, 
                     n_jobs=1,    
                     seasonal=False, 
                     stationary=False,
                     # most likely no need to change, just to know that there are such a possibilities to change
                     information_criterion='aic', 
                     alpha=0.05, test='kpss', 
                     seasonal_test='ocsb',                                     
                     method='lbfgs', 
                     random=False,  
                     n_fits=10, 
                     return_valid_fits=False,                     
                     with_intercept='auto')

        order = mdl.get_params().get('order')
        ljung = sms.diagnostic.acorr_ljungbox(mdl.resid(), lags=[25], boxpierce=False)     
        
        # Write results
        index = results[(results['Order'] == order) & (results['Time frame'] == t)].index
        if len(index) == 0:
            if ljung['lb_pvalue'].iloc[0] < 0.05:
                results.loc[df_counter] = [t, order, 1, 0]                
            else: # it is ok, increment the valid counter
                results.loc[df_counter] = [t, order, 1, 1]            
            df_counter += 1
        else:
            results['Number of orders'].loc[index] = results['Number of orders'].loc[index] + 1
            if ljung['lb_pvalue'].iloc[0] > 0.05:  # it is ok, increment the valid counter          
                results['Number of valid fits'].loc[index] = results['Number of valid fits'].loc[index] + 1
        
results.to_csv(result_path)
print('Elapsed time: ', time.time() - t_start) 
    