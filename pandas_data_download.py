
# -*- coding: utf-8 -*-
from __future__ import division, print_function
import pandas
import pandas_datareader.data as web
import numpy
from scipy.stats import gaussian_kde as kde
import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.formula.api as smf


# Function to download data 
def get_data(stock, source, start, end):
    return web.DataReader(stock, source, start, end)


# Function to get the kernel density estimate of distribution
def build_kde(inputData, columnName):
    
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

    return plot_range, kde_function


# Function to calculate returns
def calc_returns(inputData, columnName, lag = 0):
    
    if min(inputData.index) == inputData.index[0]:
        # Ascending
        lag = 1
    elif max(inputData.index) == inputData.index[0]:
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

# Get basic statistics for the time series
def basics(inputDataSeries):
    
    return {
            'mean' : inputDataSeries.mean(), \
            'stdev' : inputDataSeries.std(), \
            'skewness' : inputDataSeries.skew(), \
            'kurtosis' : inputDataSeries.kurt()
    }
    

# Calculate acf and pacf
def get_acf(inputDataSeries, lag = 15):
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
    return outputData, {'acf' : list(acf_values), \
                        'pacf': pacf(inputDataSeries, nlags = n_iter)} 


# Calculate CDF for given data
def calc_cdf(inputDataSeries):
    
    sortedData = inputDataSeries.sort_values(ascending = True)
    n = len(sortedData)    
    
    cdf = []
    i = 1
    
    for item in sortedData:
        cdf.append(i/n)
        i += 1
    
    plt.plot(sortedData, cdf)    
    return pandas.DataFrame({'Return' : sortedData, 'CDF' : cdf})




a = get_data(stock = 'ICICIBANK.BO', source = 'yahoo', \
             start = datetime.datetime(2005,01,01), \
             end = datetime.datetime(2016,07,17))



b = calc_returns(a, 'Close')
c, d = get_acf(b['2015':'2016']['Simple_Returns'], lag = 25)
stats = basics(b['2015':'2016']['Simple_Returns'])

x_simple, y_simple = build_kde(b['2015':'2016'], 'Simple_Returns')
x_log, y_log = build_kde(b['2015':'2016'], 'Log_Returns')

plt.plot(b['2015':'2016']['Simple_Returns'])


calc_cdf(b['2015':'2016']['Simple_Returns'])


