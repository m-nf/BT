# Indicator for ARIMA strategy
#
# It makes forecast of logarithm returns using ARIMA model.
# Order of ARIMA model must be determined before running this code, you must use the same data as here, even the same
# lenght. Tool for use: notebook ARIMA_fitting.ipynb.
# Parameters must be set in this file in part "PARAMETERS SETTING".

import backtrader as bt
from backtrader.indicators import SimpleMovingAverage as SMA
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

class ArimaFcIndicator(bt.Indicator):

    lines = ('fc_buy', 'fc_sell', 'fc_log')

    def __init__(self):

        # PARAMETERS SETTING --------------------------------------------
        self.params = dict(
            num_samples = 36901, # number of samples for forecast
            fc_lenght = 615, # lenght of forecast
            ci = 0.05, # confidence interval
            order = (5,0,0), # order for ARIMA model

            counter = 0 # counting (each 'fc_lenght' trades - new forecast)           
        )
        # ---------------------------------------------------------------

    def next(self):
        self.params['counter'] += 1

        # delay in start - we don't have samples for forecast
        if len(self) >= self.params['num_samples']:           
            
            if self.params['counter'] > (self.params['fc_lenght'] - 3): # ... -3 because of last row in this code
                data = self.data.get(ago = 0, size = self.params['num_samples'])
                
                data = pd.DataFrame(data=data)
                lrets = np.log(data/data.shift(1)).fillna(0)                

                model = ARIMA(endog=lrets, order=self.params['order']).fit()
                fc_raw = model.get_forecast(steps=self.params['fc_lenght'])
                self.fc_ci = fc_raw.summary_frame(alpha=self.params['ci'])
                
                self.fc_ci.index = range(0, self.params['fc_lenght'])
                self.params['counter'] = 0
                
            self.lines.fc_buy[0] = self.fc_ci.at[self.params['counter'] + 2, 'mean'] # +2 because at time t is created order and at t+1 is executed
            self.lines.fc_sell[0] = self.fc_ci.at[self.params['counter'] + 2, 'mean'] # +2 because at time t is created order and at t+1 is executed
            self.lines.fc_log[0] = self.fc_ci.at[self.params['counter'], 'mean']
          


