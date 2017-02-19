# -*- coding: utf-8 -*-

"""
HDFCBANK, ICICIBANK, CANBK, AMBIKCO
"""
import os
import openpyxl
import datetime
import pandas


os.chdir("E:\\Kshitij\\Projects\\Time_Series")


import NSE_Downloader.download_data_NSE as nse 



Ticker = 'ICICIBANK'
from_date = '2005-01-01'
to_date = '2006-12-31'
time_period = ''

if not(os.path.isdir(Ticker)):
    os.mkdir(Ticker)    

# Call function to get the data from the net
c1 = nse.get_NSE_data(Ticker, from_date, to_date)

# Reset the index
c2 = c1.reset_index(drop = True)

# Saving data in excel and csv format for future usage
c2.to_csv(os.path.join(Ticker, 'bkup.' + Ticker + '_' + from_date + '_' + to_date + '.csv'))
c2.to_excel(os.path.join(Ticker, 'bkup.' + Ticker + '_' + from_date + '_' + to_date + '.xlsx'))

# --------------------------------------------------------------------
# Time Series Analysis start here
# --------------------------------------------------------------------
ts = pandas.DataFrame(c2[['Close Price', 'Total Traded Quantity']])
ts.index = pandas.to_datetime(c2['Date'], format = '%d-%b-%Y')

# Plotting to see the data
ts.plot()