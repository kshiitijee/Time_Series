# -*- coding: utf-8 -*-

"""
HDFCBANK, ICICIBANK, CANBK, AMBIKCO
"""
import os
import openpyxl


os.chdir("E:\\Kshitij\\Projects\\Time_Series")


import download_data_NSE as nse 



Ticker = 'ICICIBANK'
from_date = '2016-01-01'
to_date = '2016-04-15'
time_period = ''

if not(os.path.isdir(Ticker)):
    os.mkdir(Ticker)    

c1 = nse.get_NSE_data(Ticker, from_date, to_date)

c2 = c1.reset_index(drop = True)

c2.to_csv(os.path.join(Ticker, 'bkup.' + Ticker + '_' + from_date + '_' + to_date + '.csv'))
c2.to_excel(os.path.join(Ticker, 'bkup.' + Ticker + '_' + from_date + '_' + to_date + '.xlsx'))

