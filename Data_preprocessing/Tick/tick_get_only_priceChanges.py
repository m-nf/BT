# This script creates three files 1. there are only rows with price change in ask           
#                                 2. there are only rows with price change in bid
#                                 3. there are only rows with price change in bid or ask

# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "choose_datepart_from_original_data.py" or "parseDate_orig_data.py"
# Data file needed: e.g. "EURUSD_2019_01_03.csv"
# It creates files: e.g. "EURUSD_2019_01_03_bothPriceChanges.csv"

import pandas

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03.csv'
result_path = 'EURUSD_2019_01_03_bothPriceChanges.csv'
# --------------------------------------------------------------------------------------------------


data = pandas.read_csv(data_path, header=0, index_col='ID', parse_dates=['Datetime'])

data['Ask_up/down'] = 0
data['Bid_up/down'] = 0
data_lenght = len(data.index) - 1

for i in range(data_lenght):
    # Price change:
    # up ...   1
    # down ... -1
    # equal ... 0
    # indexes must be without mistakes for function .at ()

    # doing ask
    if data.at[(i + 1), 'Ask'] > data.at[i, 'Ask']:
        data.at[(i + 1), 'Ask_up/down'] = 1
    elif data.at[(i + 1), 'Ask'] == data.at[i, 'Ask']:
        data.at[(i + 1), 'Ask_up/down'] = 0
    else:
        data.at[(i + 1), 'Ask_up/down'] = -1

    # doing bid
    if data.at[(i + 1), 'Bid'] > data.at[i, 'Bid']:
        data.at[(i + 1), 'Bid_up/down'] = 1
    elif data.at[(i + 1), 'Bid'] == data.at[i, 'Bid']:
        data.at[(i + 1), 'Bid_up/down'] = 0
    else:
        data.at[(i + 1), 'Bid_up/down'] = -1


# Price change is in bid OR ask
data_both = data[(data['Bid_up/down'] != 0) | (data['Ask_up/down'] != 0)] # deleting rows, that contain zero change in both - ask and bid
data_both = pandas.DataFrame(data_both, columns = ["Datetime", "Ask", "Bid", "Ask_up/down", "Bid_up/down"]) # creating dataframe

data_both_lenght = len(data_both.index)

ix = list(range(0,data_both_lenght)) # new indexing
data_both['ID'] = ix
data_both.set_index('ID', inplace = True)

data_both.to_csv(result_path)