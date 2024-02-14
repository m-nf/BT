# Script for the figures in the thesis: "ACF, PACF - logarithmic returns", "ACF, PACF - ARIMA(0,1,0)", "ACF, PACF - ARIMA(2,0,2)", " ACF, PACF - ARIMA(3,0,2)".
# It plots ACF and PACF for the residuals of fitted ARIMA model.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to create needed files.
# Data file needed: "EURUSD_2019_01_03_without-ID.csv".
# It creates files: "acf.pdf".

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03_without-ID.csv'
result_path = 'acf.pdf'
order  = (3,0,2) # order for arima model
num_of_lags = 25 # number of lags for ACF and PACF
# --------------------------------------------------------------------------------------------------

def acf_plot(y, lags=None, figsize=(9, 3), result_path=''):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    
    fig = plt.figure(figsize=figsize)
    
    layout = (1, 2)
    acf_ax = plt.subplot2grid(layout, (0, 0))
    pacf_ax = plt.subplot2grid(layout, (0, 1))

    acf_ax.grid(True)
    pacf_ax.grid(True)
    
    plot_acf(y, lags=lags, ax=acf_ax, alpha=0.05, zero=False, auto_ylims=True)
    plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.05, method='ywm', zero=False, auto_ylims=True)    
    
    plt.tight_layout()
    plt.show()
    plt.savefig(result_path, format='pdf', bbox_inches="tight")
    return

# Data preparation
data = pd.read_csv(data_path, header=0, index_col=None, parse_dates=['Datetime'])
data = data['Middle']
print(data.shape)
# log returns
lrets = np.log(data/data.shift(1)).fillna(0)                                             
print(lrets)
print("Data preparing done.")

# ARIMA fitting
mdl = ARIMA(endog=lrets, order=order).fit()
# Plotting
acf_plot(y=mdl.resid, lags=num_of_lags, result_path=result_path)