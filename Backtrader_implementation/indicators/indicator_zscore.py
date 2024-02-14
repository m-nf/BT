# Z-Score indicator
# 
# Is calculates Z-score of actual price. We use the Z-score in mean reversion strategy. Std from numpy 
# isn't used because of efectivity.
# It can be used with simple moving average or with cumulative moving average.
# Parameters must be set in this file in part "PARAMETERS SETTING".

import numpy as np
import backtrader as bt
from backtrader.indicators import SimpleMovingAverage as SMA
 

class ZScoreIndicator(bt.Indicator):
    lines = ('zscore',)    

    def __init__(self, cma):

        # PARAMETERS SETTING --------------------------------------------
        use_cma = False # if to use sma or cma
        sma_period = 442812 # length of sma used, if any
        # ---------------------------------------------------------------
        
        self.count = 0 # trade counter
        self.sum = 0
        self.std = 0 # standard deviation
        self.var = 0 # variance       
        if use_cma == False:
            self.ma = SMA(self.datas[0], period = sma_period)
        else:
            self.ma = cma        

    def next(self):

        self.count += 1
        
        # Definitions:
        #   z = (x - EX) / std
        #   std = sqrt(varX)
        #   varX = sum((Xi - EX)**2) * 1/n

        self.sum += (self.data[0] - self.ma[0])**2 # intermediate calculation for variances
        self.var = self.sum / self.count
        self.std = np.sqrt(self.var)

        self.lines.zscore[0] = (self.data[0] - self.ma[0]) / self.std