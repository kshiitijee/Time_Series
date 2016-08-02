# -*- coding: utf-8 -*-
from __future__ import division, print_function
import pandas
import pandas_datareader.data as web
import numpy
from scipy.stats import gaussian_kde as kde
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
# import statsmodels.formula.api as smf



class stock:
    
    # Initialize and download the data
    def __init__(self, scrip  = 'ICICIBANK.BO', 
                 from_date = datetime.strftime(datetime.today() - timedelta(days = 365), '%Y-%m-%d'), 
                 to_date = datetime.strftime(datetime.today(), '%Y-%m-%d'),
                 source = 'yahoo'):
        self.scrip = scrip
        self.source = source
        self.from_date = datetime.strptime(from_date, '%Y-%m-%d')
        self.to_date = datetime.strptime(to_date, '%Y-%m-%d')
        
        
        # Calling function to get the data
        self.data_matrix = {}
        self.data_matrix['input_data'] = self.get_data(scrip, from_date, to_date, source)        
        
        # Calculating the returns on input data on closing prices with lag = 1 
        self.data_matrix['returns_data'] = self.calc_returns(self.data_matrix['input_data'], 'Close', 1)
        
        # Get all basics calculated
        self.basic_stats = {}
        self.basic_stats['Simple_Returns'] = self.basics(self.data_matrix['returns_data']['Simple_Returns'])
        self.basic_stats['Log_Returns'] = self.basics(self.data_matrix['returns_data']['Log_Returns'])
        
        # Building KDE
        self.kde_func = {}
        self.kde_func['Simple_Returns'] = self.build_kde(self.data_matrix['returns_data'], 'Simple_Returns')
        self.kde_func['Log_Returns'] = self.build_kde(self.data_matrix['returns_data'], 'Log_Returns')
        
        # Calculate acf & pacf
        self.acf_pacf = {}
        self.acf_pacf['Simple_Returns'] = self.get_acf_pacf(self.data_matrix['returns_data']['Simple_Returns'], lag = 25)
        self.acf_pacf['Log_Returns'] = self.get_acf_pacf(self.data_matrix['returns_data']['Log_Returns'], lag = 25)

        # Calculate CDF
        self.cdf = {}
        self.cdf['Simple_Returns'] = self.calc_cdf(self.data_matrix['returns_data']['Simple_Returns'])
        self.cdf['Log_Returns'] = self.calc_cdf(self.data_matrix['returns_data']['Log_Returns'])

        
    # -----------------------------------------------
    # Download the data
    # -----------------------------------------------
    def get_data(self, scrip = None, from_date = None, to_date = None, source = 'yahoo'):
        
        # In case any variable is not provided use the default one fed earlier
        if scrip is None:
            print('Scrip value not provided. Taking value:', self.scrip)
            scrip = self.scrip

        if from_date is None:
            print('from date not provided Taking value:', self.from_date)
            from_date = self.from_date
        
        if to_date is None:
            print('to date not provided. Taking value:', self.to_date)
            to_date = self.to_date
            
        return web.DataReader(scrip, source, from_date, to_date)

    # -----------------------------------------------
    # Function to calculate returns
    # -----------------------------------------------
    def calc_returns(self, inputData = None, columnName = None, lag = None):
        
        if lag == 0:
            if min(inputData.index) == 1: #inputData.index[0]:
                # Ascending
                lag = 1
            elif max(inputData.index) == 2: # inputData.index[0]:
                # Descending
                lag = -1
            else:
                print('Cannot determine the order put the lag value manually')
                print('Syntax: calc_returns(inputData, columnName, lag = lag_value)')
        
        # Copy the input data in a separate dataframe
        outputData = pandas.DataFrame(inputData[columnName])
        
        # Define the name of lagged column based on input column name given
        lagged_columnName = 'Lagged_' + columnName 
        
        # Create the lagged column by shifting values appropiately
        outputData[lagged_columnName] = outputData[columnName].shift(lag)
        
        # Drop all the nan values
        outputData = outputData.dropna()
        
        # Define simple return
        outputData['Simple_Returns'] = outputData[columnName]/outputData[lagged_columnName] - 1
        
        # Define log returns
        outputData['Log_Returns'] = numpy.log(outputData[columnName]/outputData[lagged_columnName])
        
        # Return output data frame    
        return outputData

    # -----------------------------------------------
    # Get basic statistics for the time series
    # -----------------------------------------------
    def basics(self, inputDataSeries):
        
        return {
                'mean' : inputDataSeries.mean(), \
                'stdev' : inputDataSeries.std(), \
                'skewness' : inputDataSeries.skew(), \
                'kurtosis' : inputDataSeries.kurt()
        }



    #ICICI = stock('ICICIBANK.BO', '2005-01-01', '2016-07-25', 'yahoo')

    # -----------------------------------------------
    # Function to get the kernel density estimate of 
    # distribution
    # -----------------------------------------------
    def build_kde(self, inputData, columnName):
    
        if len(inputData) < 5:
            print("Please input atleast 5 data points")
            return
        
        # Get number of data points to be plotted        
        num_div = max(5, int(len(inputData)/10))
        
        # Generate the plot range
        plot_range = numpy.linspace(max(inputData[columnName]), \
                                    min(inputData[columnName]), \
                                    num = num_div)
        # Generating the kde function
        kde_function = kde(inputData[columnName])
        
        # Plotting the KDE and histogram simultaneously
        # ----------------------------------------------
    
        # Initializing the plot
        fig, ax1 = plt.subplots()
    
        # Plot secondary y-axis
        inputData[columnName].hist(bins = num_div)
    
    
        # Create secondary y-axis
        ax2 = ax1.twinx()
        
        # Plot the graph on primary x-axis
        ax1.plot(plot_range, kde_function(plot_range), 'r-', \
                 plot_range, kde_function(plot_range), 'ko')
        
    
        # Labeling the axis
        ax1.set_xlabel('Returns')
        ax1.set_ylabel('KDE', color='g')
        ax2.set_ylabel('Frequency', color='b')
    
        return {'x_kde':plot_range, 'y_kde':kde_function}


    # -----------------------------------------------
    # Calculate acf and pacf
    # -----------------------------------------------
    def get_acf_pacf(self, inputDataSeries, lag = 15):
        # Copy the data in input data
        outputData = pandas.DataFrame(inputDataSeries)
        
        if min(inputDataSeries.index) == inputDataSeries.index[0]:
            # Ascending
            multiplier = 1
            lag = multiplier*lag
        elif max(inputDataSeries.index) == inputDataSeries.index[0]:
            # Descending
            multiplier = -1
            lag = multiplier*lag
        else:
            print('Cannot determine the order put the lag value manually')
            print('Syntax: calc_returns(inputData, columnName, lag = lag_value)')
        
        n_iter = lag
        columnName = outputData.columns[0]
        i = 1
        
        
        # Calculate ACF
        acf_values = []
        acf_values.append(outputData[columnName].corr(outputData[columnName]))
        
        while i <= abs(n_iter):
            col_name = 'lag_' + str(i)
            outputData[col_name] = ''
            outputData[col_name] = outputData[columnName].shift(multiplier*i)
            
            i += 1
            
            acf_values.append(outputData[columnName].corr(outputData[col_name]))
        
        # Define an emplty figure
        fig = plt.figure()
        
        # Define 2 subplots
        ax1 = fig.add_subplot(211) # 2 by 1 by 1 - 1st plot in 2 plots
        ax2 = fig.add_subplot(212) # 2 by 1 by 2 - 2nd plot in 2 plots
        
        ax1.plot(range(len(acf_values)), acf(inputDataSeries, nlags = n_iter), \
                 range(len(acf_values)), acf_values, 'ro')
        ax2.plot(range(len(acf_values)), pacf(inputDataSeries, nlags = n_iter), 'g*-')
        
        # Plot horizontal lines    
        ax1.axhline(y = 0.0, color = 'black')
        ax2.axhline(y = 0.0, color = 'black')
            
        # Axis labels    
        plt.xlabel = 'Lags'
        plt.ylabel = 'Correlation Coefficient'
        return {'acf' : list(acf_values), \
                'pacf': pacf(inputDataSeries, nlags = n_iter)} 
    
    # -----------------------------------------------    
    # Calculate CDF for given data
    # -----------------------------------------------
    def calc_cdf(self, inputDataSeries):
        
        sortedData = inputDataSeries.sort_values(ascending = True)
        n = len(sortedData)    
        
        cdf = []
        i = 1
        
        for item in sortedData:
            cdf.append(i/n)
            i += 1
        
        plt.plot(sortedData, cdf)    
        return pandas.DataFrame({'Return' : sortedData, 'CDF' : cdf})




'''a = get_data(stock = 'ICICIBANK.BO', source = 'yahoo', \
             start = datetime.datetime(2005,01,01), \
             end = datetime.datetime(2016,07,17))



b = calc_returns(a, 'Close')
c, d = get_acf_pacf(b['2015':'2016']['Simple_Returns'], lag = 25)
stats = basics(b['2015':'2016']['Simple_Returns'])

x_simple, y_simple = build_kde(b['2015':'2016'], 'Simple_Returns')
x_log, y_log = build_kde(b['2015':'2016'], 'Log_Returns')

plt.plot(b['2015':'2016']['Simple_Returns'])


calc_cdf(b['2015':'2016']['Simple_Returns'])
'''


        