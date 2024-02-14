# Replaces all NaN values with 0.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: None
# Data file needed: any
# It creates files: any

import pandas

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = ''
result_path = ''
# --------------------------------------------------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col=0)

if data.isnull().values.any():
    print("Count of NaN was: ", data.isnull().sum().sum())
    data = data.fillna(0)
    data.to_csv(result_path)
else: 
    print("Was without NaN.")






