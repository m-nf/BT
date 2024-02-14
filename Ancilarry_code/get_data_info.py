# Writes down info about data.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Data file needed: any file with header and indexing.
# It creates files: None

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = ''
# --------------------------------------------------------------------------------------------------

import pandas as pd

data = pd.read_csv(data_path, header=0, index_col=0)

print(data.info)