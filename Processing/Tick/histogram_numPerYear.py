# Counts number of trades per year. Result is save to csv file in form of table: Year, Number of trades.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: None
# Data file needed: original Tick data files, e.g. "EURUSD_GMT+0_NO-DST-2011-01012014.csv"
# It creates files: e.g. "histogram_numPerYear_2011-2014.csv"

import pandas as pd
from datetime import datetime, timedelta # timedelta doesn't support years -> relativedelta should
from dateutil.relativedelta import relativedelta
import time

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_GMT+0_NO-DST-2011-01012014.csv'
result_path = 'histogram_numPerYear_2011-2014.csv'
# --------------------------------------------------------------------------------------------------

start_time = time.time()

custom_date_parser = lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S.%f")
data = pd.read_csv(data_path, header=None, 
                        names=["Datetime", "Ask", "Bid", "Nothing", "Nothing1"], index_col = None, parse_dates=['Datetime'], date_parser=custom_date_parser)
data.index.name = 'ID'

first_date = data.at[0, 'Datetime']
start_date = datetime(first_date.year, 1, 1, 0, 0, 0)
end_date = start_date + relativedelta(years=1)
data_end = data['Datetime'].iloc[-1]

results = dict()


while(start_date < data_end):
    year = data[(data['Datetime'] >= start_date) & (data['Datetime'] < end_date)] # choose one year    
    
    if year.empty == False: # because there are weekends, holidays # I think this row is useless in this file
        results[start_date] = len(year.index)        

    start_date += relativedelta(years=1)
    end_date += relativedelta(years=1)


output_data = pd.DataFrame.from_dict(results, orient='index', columns=['Number of trades'])
output_data.index.name = 'Year'

output_data.to_csv(result_path)

end_time = time.time()
print("Elapsed time: ", (end_time-start_time)/60, " minutes")

