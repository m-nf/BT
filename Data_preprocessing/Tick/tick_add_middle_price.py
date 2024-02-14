# Add a middle price (Ask+Bid) / 2 to dataset.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "choose_datepart_from_original_data.py" or "parseDate_orig_data.py".
# Data file needed: e.g. "EURUSD_2019_01_03.csv".
# It creates files: e.g. "EURUSD_2019_01_03.csv".

import pandas

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_2019_01_03.csv'
result_path = 'EURUSD_2019_01_03.csv'
# --------------------------------------------------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col=0, parse_dates=['Datetime'])

data['Middle'] = round((data['Ask'] + data['Bid']) / 2, 6)

data.to_csv(result_path)