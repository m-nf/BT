# It converts datetime from unix timestamp to ISO 8601 in millisecond accuracy.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "add_header+indexing.py"
# Data file needed: "BTCUSDT-trades-2022-01-03.csv"
# It creates files: "BTCUSDT-trades-2022-01-03_parsedDate.csv"

import pandas as pd

# PARAMETERS SETTING -------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03.csv'
result_path = 'BTCUSDT-trades-2022-01-03_parsedDate.csv'
# --------------------------------------------------------

data = pd.read_csv(data_path, header=0, index_col='myID')

data['Datetime'] = pd.to_datetime(data['time'],unit='ms')

data.drop(columns=['time'], axis=1, inplace=True)

data.to_csv(result_path)