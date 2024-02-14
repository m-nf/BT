# Calculates the mean of how many trades are in specific time frame (parameter "time_deltas")
# E.g. result: in 10 minutes window is average number of trades 1500.

# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to get the needed data files.
# Data file needed: "EURUSD_2019_01_03.csv" or "BTCUSDT-trades-2022-01-03_parsedDate.csv".
# It creates files: "EURUSD_2019_01_03_trades_per_time" or "BTCUSDT_trades_per_time.csv".

import pandas
from datetime import  datetime, timedelta
import time

time_stat_s = time.time() # time measuring

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03.csv' # 'BTCUSDT-trades-2022-01-03_parsedDate.csv'
result_path = 'EURUSD_2019_01_03_trades_per_time' # 'BTCUSDT_trades_per_time.csv'
time_deltas = dict({1:0, 10:0, 60:0, 300:0, 600:0, 1800:0, 3600:0}) # The time frames we want to tests. In seconds.
start_time_base = datetime(2019, 1, 3, 0, 0, 0) # date you want to start (e.g. beginning of the file) Binance - datetime(2022, 1, 3, 0, 0, 0)
end_time_base = start_time_base # or can be changed anyhow needed - datetime(2019, 1, 3, 0, 0, 0)
tick = True # Tick data = True, Binance data = False
# --------------------------------------------------------------------------------------------------

if tick == True:
    data = pandas.read_csv(data_path, header=0, index_col='ID', parse_dates=['Datetime'])
else:
    data = pandas.read_csv(data_path, header=0, index_col='myID', parse_dates=['Datetime'])

data_end = data['Datetime'].iloc[-1]

# Iterate through keys (time deltas)
for delta in time_deltas:
    
    delta_t = timedelta(seconds=delta)
    start_time = start_time_base
    end_time = end_time_base + delta_t
    the_sum = 0
    count = 0

    # Calculating the sum for the specific time delta
    while(start_time < data_end):
        x = data[(data['Datetime'] >= start_time) & (data['Datetime'] < end_time)]    
        
        the_sum += len(x.index)
        
        count +=1   
        start_time += delta_t
        end_time += delta_t
    
    # Save result for the specific time delta
    time_deltas[delta] = the_sum/count


time_stat_e = time.time()
print(time_deltas)

with open(result_path, 'w') as file:
    for delta in time_deltas:
        if delta % 60 != 0: # seconds or mnutes
             file.write('%s s: %s trades\n' % (delta, time_deltas[delta]))
        else:
            file.write('%s min: %s trades\n' % (int(delta/60), time_deltas[delta]))

print("Elapsed time: %s s" % (time_stat_e - time_stat_s))