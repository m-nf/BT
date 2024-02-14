# Main class for running strategies for Tick data.
#
# Parameters must be set in this file in part "PARAMETERS SETTING" and in indicators files.
# Scripts needed to run before:
# Data file needed: "EURUSD_2019_01_03_without-ID.csv"
# It creates files: results and log file


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path  # To manage paths
import time 

# Import the backtrader platform
import backtrader as bt
from strategies.strategy_momentum_MAR import MomentumStrategy
from strategies.strategy_mean_rev import MeanReversionStrategy
from strategies.strategy_arima import ArimaStrategy
import global_variables as globvar

# PARAMETERS SETTING -------------------------------------------------------------------------------
params = dict(
    path_data = 'EURUSD_2019_01_03-without-ID.csv',
    path_results = '',
    path_log = '',

    strategy = ArimaStrategy,
    commission = 0,
    trd_amount = 10, # in %, (of available cash)
    strategy_title = '',
    cash = 10000.0
)
# --------------------------------------------------------------------------------------------------

def log_results(txt):
    with open(params['path_results'], 'a') as file:
        file.write('%s\n' % txt)

def get_cerebro():
    return cerebro


if __name__ == '__main__':

    start_time = time.time()

    # Delete log file if exists
    if os.path.isfile(params['path_results']):
        os.remove(params['path_results'])  

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(params['strategy'], params['path_log'])
    
    # Define data feed
    data = bt.feeds.GenericCSVData(
        dataname=params['path_data'],
        
        timeframe=bt.TimeFrame.Ticks,
        #timeframe=bt.TimeFrame.MicroSeconds,
        fromdate=datetime.datetime(2019, 1, 2),
        todate=datetime.datetime(2019, 1, 4),
        dtformat=('%Y-%m-%d %H:%M:%S.%f'),
        datetime = 0,
        high = -1,
        low = -1,
        open = 3,
        close = 3,
        volume = -1,
        openinterest = -1
    )     

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(params['cash'])
    #cerebro.broker.set_coc(True)

    # Add a PercentSizer - we trade with x % of available cash
    cerebro.addsizer(bt.sizers.PercentSizer, percents = params['trd_amount'])
    # Add a FixedSize sizer - we trade a fixed amount of commodity (shares/currencies/crypto, ...), e.g. we bought 1 € (stake=1) for 1.x $
    #cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    # Add observer - for acces to portofolio value in strategy (for purpose of log)
    cerebro.addobserver(bt.observers.Broker)
    
    # Set the commission - 0.1% ... divide by 100 to remove the % --> commission=0.001
    cerebro.broker.setcommission(commission=params['commission'])    


    # Logs the starting conditions
    log_results('%s\n' % params['strategy_title'])    
    log_results('Trading amount = %f %% of available cash' % params['trd_amount'])
    log_results('Commission = %f' % params['commission'])
    log_results('Starting Portfolio Value: %.5f' % cerebro.broker.getvalue())
    
    # Run over everything
    cerebro.run()

    # Logs the final result 
    log_results('Final Portfolio Value: %.5f' % cerebro.broker.getvalue())
    
    log_results('\nCount of executed buy orders: %s' % globvar.buy_count)
    log_results('Count of executed sell orders: %s' % globvar.sell_count)
    log_results('Count of profitable trades: %s' % globvar.success_trades)
    log_results('Count of loss-making trades: %s' % globvar.fail_trades)
    log_results('Count of balanced trades: %s' % globvar.balanced_trades)
    

    # Time measuring
    end_time = time.time()

    # Logs elapsed time
    log_results('\nElapsed time %f s' % (end_time - start_time))