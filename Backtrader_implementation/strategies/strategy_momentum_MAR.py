# Momentum strategy (using moving average ribbons)
#
# Logic of strategy according to https://github.com/Auquan/Tutorials/blob/master/Momentum%20Strategies.ipynb
# Additional information https://www.investopedia.com/terms/m/movingaverageribbon.asp
# Code based on example strategy from Quickstart Guide on Backtrader site: https://www.backtrader.com/docu/quickstart/quickstart/
# Parameters to set: none.

import backtrader as bt
from indicators.indicator_MAR import MARIndicator
import os
import global_variables as globvar

class MomentumStrategy(bt.Strategy):
    
    def __init__(self, arg_path_log):    
        self.params = dict(
            path_log = arg_path_log            
        ) 

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Delete existing log file               
        if os.path.isfile(self.params['path_log']):
            os.remove(self.params['path_log'])        

        # Add a MAR indicator
        self.mar = MARIndicator(self.datas[0])       
        

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log_file(
                    'BUY EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                globvar.buy_count += 1

            else: 
                self.log_file('SELL EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                globvar.sell_count += 1

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log_file('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log_file('OPERATION PROFIT, GROSS %.5f, NET %.5f' % (trade.pnl, trade.pnlcomm))

        if trade.pnlcomm > 0:
            globvar.success_trades += 1                    
        elif trade.pnlcomm < 0:
            globvar.fail_trades += 1
        else:
            globvar.balanced_trades +=1

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log_file('Close %.5f, MAR %.5f' % (self.dataclose[0], self.mar[0]))        

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # We might buy if ...
            if self.mar[0] == 0:

                # Buy
                self.log_file('BUY CREATE, %.5f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()                
                
        else:

            if  self.mar[0] == 1:
                # Sell
                self.log_file('SELL CREATE, %.5f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()               

    # File log
    def log_file(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        with open(self.params['path_log'], 'a') as file:
            file.write('%s, %s\n' % (dt.isoformat(), txt))

    # Terminal log
    def log_terminal(self, txt, dt=None):        
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
