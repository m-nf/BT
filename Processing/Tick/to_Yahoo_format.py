# It creates Yahoo! formated data from tick data, i.e. Date, Open, High, Low, Close
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: see Data_preprocessing how to get needed data file.
# Data file needed: "EURUSD_oneY_2019.csv".
# It creates files: "EURUSD_oneY_Yformat.csv".

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'EURUSD_oneY_2019.csv'
result_path = 'EURUSD_oneY_Yformat.csv'
# --------------------------------------------------------------------------------------------------

import pandas
from datetime import timedelta 

data = pandas.read_csv(data_path, header=0, index_col=0, parse_dates=['Datetime'])

start_of_day = data['Datetime'].iloc[0]
start_of_day = start_of_day.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = start_of_day + timedelta(days=1)

output_list = []
i = 0

# Main cycle
while(start_of_day < data['Datetime'].iloc[-1]):
    
    # Choosing one day
    day = data[(start_of_day < data['Datetime']) & (data['Datetime'] < end_of_day)]
    
    # Solution of weekends/holidays
    if day.empty == False:    
        output_list.append([start_of_day.strftime("%Y-%m-%d"), 
                            "{:.6f}".format((day['Ask'].iloc[0] + day['Bid'].iloc[0]) / 2), # Using ask and bid average
                            "{:.6f}".format((day['Ask'].max() + day['Bid'].max()) / 2), 
                            "{:.6f}".format((day['Ask'].min() + day['Bid'].min()) / 2), 
                            "{:.6f}".format((day['Ask'].iloc[-1] + day['Bid'].iloc[-1]) / 2)])
    
    start_of_day +=timedelta(days = 1)
    end_of_day += timedelta(days = 1)    


output = pandas.DataFrame(output_list, columns=['Datetime','Open','High','Low','Close'])
output.to_csv(result_path)


