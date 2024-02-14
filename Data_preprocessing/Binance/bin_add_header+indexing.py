# It adds a header and indexing to the original file.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: None.
# Data file needed: "BTCUSDT-trades-2022-01-03_original.csv".
# It creates files: "BTCUSDT-trades-2022-01-03.csv".

import pandas

# PARAMETERS SETTING -------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03_original.csv'
result_path = 'BTCUSDT-trades-2022-01-03.csv'
# --------------------------------------------------------

data = pandas.read_csv(data_path, header=None, index_col=None, names=["tradeID","price","qty","quoteQty", "time","isBuyerMaker","isBestMatch"])
data.index.name = "myID"
data.to_csv(result_path)