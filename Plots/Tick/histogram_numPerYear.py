# Script for the figure "Histogram with number of quotes per year" in the thesis.
# Plots histogram of number of trades per year.
# Parameters must be set in this file in part "PARAMETERS SETTING".
# Scripts needed to run before: "histogram_numPerYear.py" over all of the original data files, then manually copy the results into one file.
# Data file needed: "histogram_numPerYear_2004-2020.csv" (the one manually created)
# It creates files: "histogram_numPerYear.pdf"

import pandas
import matplotlib.pyplot as plt

# PARAMETERS SETTING -------------------------------------------------------------------------------
data_path = 'histogram_numPerYear_2004-2020.csv'
result_path = 'histogram_numPerYear.pdf'
# --------------------------------------------------------------------------------------------------

data = pandas.read_csv(data_path, header=0, index_col=None)
data['Number of trades'] = data['Number of trades'] / 1000000 # in millions
print(data.info())

plt.rcParams.update({'font.size': 12})

data.plot(x='Year', y='Number of trades', kind='bar', color='midnightblue', label='Number of quotes')
plt.xlabel('Year')
plt.ylabel('Number of quotes (in millions)')
plt.legend()

plt.savefig(result_path, format='pdf', bbox_inches="tight")

plt.show()