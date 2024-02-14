# Cumulative moving average indicator
#
# It calculates cumulative moving average, i.e. calculates average from 0 to i. With every event, as time 
# passes, is i incremented by 1 --> window size for average is bigger and bigger.
# Parameters setting: None.

import backtrader as bt

class CMAIndicator(bt.Indicator):
    lines = ('cma',)   

    def __init__(self):
        self.datasum = 0  
        self.count = 0

    def next(self):
        self.datasum += self.data[0]
        self.count += 1

        self.lines.cma[0] = self.datasum / self.count