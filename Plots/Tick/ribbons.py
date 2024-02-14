# Script for figure "Moving average ribbons" in the thesis.
# It generates picture of moving averages ribbons. The buy and sell signals are based on the fact obtained during backtesting the strategy.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create needed data files.
# Data file needed: "EURUSD_2019_01_03_without-ID.csv"
# It creates files: "ribbons.pdf"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_without-ID.csv'
result_path = 'ribbons.pdf'
# --------------------------------------------------------------------------------------------------

data = pd.read_csv(data_path, header=0, index_col=None, parse_dates=['Datetime'])
part = data[1100:1600]

plt.rcParams.update({'font.size': 12})
plt.plot(part['Middle'], alpha = 1, label='Price')

rolling_means = {}

for i in np.linspace(30, 120, 10):
    X = part['Middle'].rolling(window=int(i),center=False).mean()
    rolling_means[i] = X
    plt.plot(X, alpha = 0.55, label='MA(%.0f)' % i)

plt.annotate('Buy', xy=(1262, 1.133025), xytext=(1262, 1.1329), arrowprops = dict(facecolor='black', shrink=0.05, width=0.1, headwidth=6))
plt.annotate('Sell', xy=(1464, 1.1335), xytext=(1464, 1.1337), arrowprops = dict(facecolor='black', shrink=0.05, width=0.1, headwidth=6))

plt.xlabel('Quotes')
plt.ylabel('Price')
plt.legend(fontsize=9)
plt.savefig(result_path, format='pdf', bbox_inches="tight")
plt.show()