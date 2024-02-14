# Script for the Figure in the thesis.
# Plot price of data. Tick or Binance data.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create needed data files.
# Data file needed: "EURUSD_2019_01_03_without-ID.csv" or "BTCUSDT-trades-2022-01-03_parsedDate.csv".
# It creates files: "EURUSD_price_2019_01_03.pdf" or "BTCUSDT_price_2022_01_03.pdf".

import pandas as pd
import matplotlib.pyplot as plt

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path_T = 'EURUSD_2019_01_03_without-ID.csv'
data_path_B = 'BTCUSDT-trades-2022-01-03_parsedDate.csv'
result_path = 'EURUSD_price_2019_01_03.pdf' # 'BTCUSDT_price_2022_01_03.pdf'
tick = True # Tick data = True, Binance data = False
# --------------------------------------------------------------------------------------------------

if tick == True:
    data = pd.read_csv(data_path_T, header=0, index_col=None, parse_dates=['Datetime'])
    plt.plot(data['Datetime'], data['Middle'], label='Price', color='darkblue')
else:
    data = pd.read_csv(data_path_B,  header=0, index_col='myID', parse_dates=['Datetime'])
    plt.plot(data['Datetime'], data['price'], label='Price', color='darkblue')

plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.legend()

plt.savefig(result_path, format='pdf', bbox_inches="tight")
plt.show()