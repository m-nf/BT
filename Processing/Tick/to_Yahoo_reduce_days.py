# It reduces the number of days according to count of days in yahoo data using merge function.
# E.g. it kicks out weekends. In tick data is one day of weekend, in Yahoo data there is no weekend day.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "to_yahoo_format.py".
# Data file needed: "EURUSD_oneY_Yformat.csv" and "EURUSD_yahoo.csv".
# It creates files: "EURUSD_oneY_Yformat_reduced_days.csv".

import pandas

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path_T = 'EURUSD_oneY_Yformat.csv'
data_path_Y = 'EURUSD_yahoo.csv'
result_path = 'EURUSD_oneY_Yformat_reduced_days.csv'
# --------------------------------------------------------------------------------------------------

data_Y = pandas.read_csv(data_path_Y, header=0, index_col=None, parse_dates=['Datetime'])
data_T = pandas.read_csv(data_path_T, header=0, index_col=0, parse_dates=['Datetime'])

output = data_T.merge(right=data_Y['Datetime'])


output.to_csv(result_path, index=False)