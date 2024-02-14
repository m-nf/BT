# It parses datetime of original data, drops two useless columns and result saves to csv file.
# Similar to the script "choose_datepart_from_original_data.py", bu it takes directly whole file.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: None.
# Data file needed: original data file, e.g. "EURUSD_GMT+0_NO-DST-2014-01012020.csv".
# It creates files: e.g. "EURUSD_GMT+0_NO-DST-2014-01012020_parsedDatetime.csv".

import pandas as pd
from datetime import datetime

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_GMT+0_NO-DST-2014-01012020.csv'
result_path = 'EURUSD_GMT+0_NO-DST-2014-01012020_parsedDatetime.csv'
# --------------------------------------------------------------------------------------------------

custom_date_parser = lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S.%f")

data = pd.read_csv(data_path, header=None, names=["Datetime", "Ask", "Bid", "Nothing", "Nothing1"], 
                   index_col = None, parse_dates=['Datetime'], date_parser=custom_date_parser)
data.index.name = 'ID'

# don't do data=data.drop() and then data.to_csv with big data - it consumes more memory
data.drop(columns=["Nothing", "Nothing1"]).to_csv(result_path)