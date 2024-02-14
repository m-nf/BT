# Script for the figure "The difference between Tick and Yahoo! data in close price" in the thesis.
# Check tick data with Yahoo! data in close price.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: 1. "to_Yahoo_format.py" 2. "to_Yahoo_reduce_days.py"
# Data file needed: "EURUSD_yahoo.csv" and "EURUSD_oneY_Yformat_reduced_days.csv"
# It creates files: "check_Yahoo_closeP.pdf"

import pandas
import matplotlib.pyplot as plt

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path_T = 'EURUSD_oneY_Yformat_reduced_days.csv'
data_path_Y = 'EURUSD_yahoo.csv'
result_path = 'check_Yahoo_closeP.pdf'
# --------------------------------------------------------------------------------------------------

dataY = pandas.read_csv(data_path_Y, header=0, index_col=None, parse_dates=['Datetime'])
data = pandas.read_csv(data_path_T, header=0, index_col=None, parse_dates=['Datetime'])

p_diff = data['Close'].shift(periods=1) - dataY['Close']

plt.plot(data['Datetime'], p_diff, label='Difference in close price (Tick - Yahoo!)', color='darkblue')
plt.xlabel('Date')
plt.ylabel('USD')
plt.grid(True)
plt.legend()

plt.savefig(result_path, format='pdf', bbox_inches="tight")

plt.show()