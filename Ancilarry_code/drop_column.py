# Drops column from dataframe.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Data file needed: any with header, without indexing. Can be easily changed in the code.
# It creates files: result file

import pandas as pd

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = ''
result_path = ''
columns = ['', ''] # columns to drop
# --------------------------------------------------------------------------------------------------

data = pd.read_csv(data_path, header=0, index_col=None)

data.drop(columns=columns, axis=1, inplace=True)

print(data)

data.to_csv(result_path, index=False)