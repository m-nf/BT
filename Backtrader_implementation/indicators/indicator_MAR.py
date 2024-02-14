# Moving average ribbon indicator
#
# Momentum indicator based on shapes of ribbons. Ribbon is created by serie of SMAs with different lenghts.
# Detailed description of implementation on https://github.com/Auquan/Tutorials/blob/master/Measuring%20Momentum.ipynb
# Additional information https://www.investopedia.com/terms/m/movingaverageribbon.asp
# Parameters must be set in this file in part "PARAMETERS SETTING".

import backtrader as bt
from backtrader.indicators import SimpleMovingAverage as SMA
import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.spatial.distance as distance
import sys

class MARIndicator(bt.Indicator):    

    lines = ('mar',)

    def __init__(self):

        # PARAMETERS SETTING --------------------------------------------
        self.params = dict(
            min_per_ma = 605, # minimal period of moving averages
            max_per_ma = 3635, # maximal period of moving averages
            num_ma = 5 # how many MA will be used
        )       
        # ---------------------------------------------------------------

        self.moving_averages = dict()
        
        # start, stop, number of MA ... creates array with equaly distanced MA
        l = np.linspace(self.params['min_per_ma'], self.params['max_per_ma'], self.params['num_ma'])        
        # Creates X simple moving averages with periods according to linspace
        for period in l:
            self.moving_averages[period] = SMA(self.datas[0], period=int(period))        

        self.sma_values = np.empty(self.params['num_ma']) # numpy array for further operation with sma_values

    def next(self):  
        i = 0
        for period in self.moving_averages:
            # getting a value of each SMA
            self.sma_values[i] = self.moving_averages[period][0]
            i += 1

        if np.array_equal(self.sma_values, np.sort(self.sma_values)): # ascending, i.e. 10 MA < 20 MA < ...
            self.lines.mar[0] = 0 # buy
        elif np.array_equal(self.sma_values, np.sort(self.sma_values)[::-1]): # descending 10 MA > 20 MA
            self.lines.mar[0] = 1 # sell
        

        