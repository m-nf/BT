# This script creates the file, where there are only rows with price change.
# e.g. i ... 5000; i+1 ... 5000   --> in created file will be only case i
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "add_header+indexing.py".
# Data file needed: "BTCUSDT-trades-2022-01-03.csv".
# It creates files: "BTCUSDT-trades-2022-01-03-onlyPriceChanges.csv".

import pandas

# PARAMETERS SETTING -------------------------------------
data_path = 'BTCUSDT-trades-2022-01-03.csv'
result_path = 'BTCUSDT-trades-2022-01-03-onlyPriceChanges.csv'
# --------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col=0)

data_lenght = len(data.index)
data['price_up/down'] = 1

data_lenght -= 1
for i in range(data_lenght):
    # Price change:
    # up ...   1
    # down ... -1
    # equal ... 0
    # indexes must be without mistakes for function .at ()

    if data.at[(i + 1), 'price'] > data.at[i, 'price']:
        data.at[(i + 1), 'price_up/down'] = 1
    elif data.at[(i + 1), 'price'] == data.at[i, 'price']:
        data.at[(i + 1), 'price_up/down'] = 0
    else:
        data.at[(i + 1), 'price_up/down'] = -1


# deleting rows with 0 (no price change)
# creating new dataframe with new indexing

data_priceChange = data[data['price_up/down'] != 0] # deleting rows with zero change
data_priceChange = pandas.DataFrame(data_priceChange, columns = ["tradeID","price","qty","quoteQty", "time","isBuyerMaker","isBestMatch", "price_up/down"]) # creating dataframe

data_priceChange_lenght = len(data_priceChange.index)

ix = list(range(0,data_priceChange_lenght)) # new indexing
data_priceChange['myID'] = ix
data_priceChange.set_index('myID', inplace = True)

data_priceChange.to_csv(result_path)
