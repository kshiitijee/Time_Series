# -*- coding: utf-8 -*-
from __future__ import division, print_function
import pandas
import pandas_datareader.data as web
import numpy
from scipy.stats import gaussian_kde as kde
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2005,01,01)
end = datetime.datetime(2016,05,26)

f = web.DataReader('ICICIBANK.BO', 'yahoo', start, end)

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
            'skew' : inputDataSeries.skew(), \
            'kurt' : inputDataSeries.kurt()
    }
    

a = calc_returns(f, 'Close')
x_simple, y_simple = build_kde(a['2015':'2016'], 'Simple_Returns')
x_log, y_log = build_kde(a['2015':'2016'], 'Log_Returns')

plt.plot(a['2015':'2016']['Simple_Returns'])

stats = basics(a['2015':'2016']['Simple_Returns'])

d
