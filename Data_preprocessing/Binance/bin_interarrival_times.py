# Figure 3.4 on page 49, text is on page 48 in book Cartea A., Jaimungal S. and Penalva J._Algorithmic and High-Frequency Trading (CRC, 2015).pdf
# Calculates time difference between two trades + statistics stuff about that. Creates (data - percentil 0.95) histogram with time difference, and scatter plot with log time difference.
# In input dataset are only trades, where is change in price.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: 1. "add_header+indexing.py" 2. "get_only_priceChanges.py"
# Data file needed: "BTCUSDT-trades-2022-01-03-onlyPriceChanges.csv"
# It creates files: "BTCUSDT-trades-2022-01-03-interarrivalTimes.csv"

import pandas

# PARAMETERS SETTING -------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03-onlyPriceChanges.csv'
result_path_data = 'BTCUSDT-trades-2022-01-03-interarrivalTimes.csv'
result_path_stat = ''
# --------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col='myID')

data['time_difference'] = data['time'].diff() # time difference

# Statistics info ---------------------------------
diff_mean = data['time_difference'].mean()            
diff_median = data['time_difference'].median()
diff_max = data['time_difference'].max()
diff_min = data['time_difference'].min()

# Writing results to the files ----------------------------------------------
data.to_csv(result_path_data)

with open(result_path_stat,'w') as file:
    file.write("Difference mean: %s ms\n"
                "Difference median: %s ms\n"
                "Difference max: %s ms\n"
                "Difference min: %s ms\n"
            %(  diff_mean,
                diff_median,
                diff_max,
                diff_min
            )
    )


