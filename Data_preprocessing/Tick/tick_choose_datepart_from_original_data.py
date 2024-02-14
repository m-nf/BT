# It chooses part from original data in the given time range. It sets columns, parses date, removes two empty columns.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: None.
# Data file needed: original data file, e.g. "EURUSD_GMT+0_NO-DST-2014-01012020.csv".
# It creates files: e.g. "EURUSD_oneY-2019.csv".

import pandas
from datetime import datetime

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_GMT+0_NO-DST-2014-01012020.csv'
result_path = 'EURUSD_oneY-2019.csv'
start_date = '2018-12-31 23:59:59.999'
end_date = '2020-01-02 00:00:00.000'
# --------------------------------------------------------------------------------------------------

custom_date_parser = lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S.%f")

data = pandas.read_csv(data_path, header=None, names=["Datetime", "Ask", "Bid", "Nothing", "Nothing1"], index_col = None, 
                        parse_dates=['Datetime'], date_parser=custom_date_parser)

data.index.name = 'ID'
data.drop(columns=['Nothing', 'Nothing1'], axis=1, inplace=True)
                                                 
data[(data['Datetime'] > start_date) & (data['Datetime'] < end_date)].to_csv(result_path)

# Note: don't do this: data = data[(data['Datetime'] > start_date) & (data['Datetime'] < end_date)]
#                      data.to_csv()
# It consumes more memory.