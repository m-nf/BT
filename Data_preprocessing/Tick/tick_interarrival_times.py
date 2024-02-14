# Figure 3.4 on page 49, text is on page 48 in book Cartea A., Jaimungal S. and Penalva J._Algorithmic and High-Frequency Trading (CRC, 2015).pdf
# It calculates time difference between two trades + statistics stuff about that.
# In dataset there are only trades, where there is change in ask or in bid price.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: 1. "choose_datepart_from_original_data.py" or "parseDate_orig_data.py", 
# 2. "get_only_priceChanges.py".
# Data file needed: e.g. "EURUSD_2019_01_03_bothPriceChanges.csv".
# It creates files: e.g. "EURUSD_2019_01_03_interarrivalTimes.csv", "EURUSD_2019_01_03_interarrival_times_diff.csv".

import pandas
from datetime import timedelta

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_bothPriceChanges.csv'
result_path = 'EURUSD_2019_01_03_interarrivalTimes.csv'
result_path_stat = 'EURUSD_2019_01_03_interarrival_times_diffStats.csv'
# --------------------------------------------------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col='ID', parse_dates=['Datetime'])

data['Difference_time'] = data['Datetime']
data['Difference_time'] = data['Difference_time'].diff() # time difference in time
data['Difference_number[ms]'] = data['Difference_time']  / timedelta(microseconds = 1) / 1000 # time difference in milliseconds
data.at[0, 'Difference_number[ms]'] = 0 # taking care of the first row

# statistics stuff ---------------------------------
diff_mean = data['Difference_time'].mean()            
diff_median = data['Difference_time'].median()
diff_max = data['Difference_time'].max()
diff_min = data['Difference_time'].min()

# writing result to a file ----------------------------------------------
data.to_csv(result_path)

with open(result_path_stat,'w') as file:
    file.write("Difference mean: %s\n"
                "Difference median: %s\n"
                "Difference max: %s\n"
                "Difference min: %s\n"
            %(  diff_mean,
                diff_median,
                diff_max,
                diff_min
            )
    )


