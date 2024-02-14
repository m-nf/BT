# Creates: csv with 10 most frequented days
#        : csv with data of most frequented day.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "choose_datepart_from_original_data.py" or "parseDate_orig_data.py"
# Data file needed: e.g. "EURUSD_oneY-2019.csv"
# It creates files: e.g. "EURUSD_2019_01_03.csv"

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_oneY-2019.csv'
result_path_data = 'EURUSD_2019_01_03.csv'
result_path_10most = '10_most_frequented.csv'
start_date = datetime(2019, 1, 1, 0, 0, 0)
end_date = datetime(2019, 1, 2, 0, 0, 0)
# --------------------------------------------------------------------------------------------------

import pandas
from datetime import datetime, timedelta

data = pandas.read_csv(data_path, header=0, index_col=0, parse_dates=['Datetime'])

date_list = []
count_list = []
data_end = data['Datetime'].iloc[-1]

while(start_date < data_end):
    day = data[(data['Datetime'] > start_date) & (data['Datetime'] < end_date)]
    
    if day.empty == False:        
        date_list.append(start_date)
        count_list.append(len(day.index))

    start_date += timedelta(days=1)
    end_date += timedelta(days=1)


output_data = {'Datetime':date_list, 'Number_of_trades': count_list}
days_frame = pandas.DataFrame(output_data)

# Sort
days_frame.sort_values(by=['Number_of_trades'], inplace=True, ascending=False)

# Ten most frequented days
days_frame = days_frame.iloc[:10]
days_frame.to_csv(result_path_10most)

# Data of the most frequented day
data = data[(data['Datetime'] > days_frame['Datetime'].iloc[0]) & (data['Datetime'] < (days_frame['Datetime'].iloc[0] + timedelta(days=1)))]
data.to_csv(result_path_data)