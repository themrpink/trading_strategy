# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 22:42:02 2019

#@author: themr
"""
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import math
import scipy.optimize as spo


#spy = pdr.get_data_yahoo(symbols='spy', start=datetime(2009, 1, 1), end=datetime(2011,12,31))
#xom = pdr.get_data_yahoo(symbols='xom', start=datetime(2009, 1, 1), end=datetime(2011,12,31))
#goog = pdr.get_data_yahoo(symbols='goog', start=datetime(2009, 1, 1), end=datetime(2011,12,31))
#gld = pdr.get_data_yahoo(symbols='gld', start=datetime(2009, 1, 1), end=datetime(2011,12,31))


def getData(dates, symbols):  
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        df_temp = pd.read_csv("{}.csv".format(symbol), index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'], na_values="NaN")
        df_temp = df_temp.rename(columns={"Adj Close":symbol})
        df = df.join(df_temp, how="inner")
    return df

def normalize(df):
    df=df / df.iloc[0,:]
    return df


def allocateShares(df, symbols, allocs, start_val):
    df2 = df.copy()
#    for i,symbol in enumerate(symbols):        
#        df2["{} allocated".format(symbol)] = df2[symbol]*allocs[i]
#        df2["{} allocated".format(symbol)] = df2["{} allocated".format(symbol)]*start_val
#        df['Port_Val'] = df1.sum(axis=1)
    df2*allocs
    df2*start_val

    print(df2)
    
    dfcopy = df.copy()

	# Find cumulative value over time
    df = (df/df.iloc[0,:])
    df =df * allocs
    df = df.sum(axis=1)

	# Compute Portfolio Statistics
    cumulative_return = (df.ix[-1]/df.ix[0]) - 1
    dailyreturns = (df.ix[1:]/df.ix[:-1].values) - 1
    average_daily_return = dailyreturns.mean(axis=0)
    std_daily_return = dailyreturns.std(axis=0)
    sharpe_ratio = (252**(1/2.0)) * ((average_daily_return-0)/std_daily_return)
    ending_value = df.ix[-1]
    total_returns = average_daily_return*(252/252)
	#return (-1 * sharpe_ratio)
    diz = {"cumulative return":cumulative_return, "daily returns":dailyreturns, "total return":total_returns,"average_daily_return ":average_daily_return,"std daily return":std_daily_return}

    dfcopynormed = dfcopy['SPY']/dfcopy['SPY'].ix[0]
    ax = dfcopynormed.plot(title='Daily Portfolio Value and SPY', label='SPY')
    sumcopy = dfcopy.sum(axis=1)
    normed = sumcopy/sumcopy.ix[0]
    normed.plot(label='Portfolio Value', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc=2)
    plt.show()
    return df2 , diz
    
#def portfolio_statistics(df, allocs):
#    pass





""""Portfolio optimizer (sharpe ratio)"""

def negative_sharpe(x, df_norm, risk_free):
    """    
    Function to minimize for an optimal portfolio based on maximal sharpe ratio.
    We're calculating the negative sharpe ratio to make sure to optimize for maximal (and not minimal) sharpe ratio.
  
  * x: list with allocations for sinlge stocks in a portfolio, these are our dependend variables.
         e.g. [0.8, 0.2] for GOOG, AAPL will allocate 80% Google and 20% Apple stocks to the portfolio.
         Make sure the sum of allocations is 1.
    * df_norm: dataframe with normalized stock prices for each stock in separate columns.
    """
    df_pf = (df_norm*x).sum(axis=1) # perform allocation and sum up to get total value of portfolio
    daily_return = compute_daily_returns(df_pf)
    
    # formula to calculate the sharpe ratio for a daily sampling frequency (252 trading days a year)
    neg_sharpe = (-1)*np.sqrt(252)*(daily_return-risk_free).mean()/daily_return.std() 
    return neg_sharpe

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns = df[1:].div(df[:-1].values, fill_value=0)-1 # use .values to access underlying numpy array, otherwise pandas will try and match indices which undoes the shifting. omit index 0 since always 0
    return daily_returns    
    
def run_portfolio_optimizer(dates, symbols, guess, risk_free_rate, df):
    """
    * dates: pandas date_range for selected stocks
    * symbols: list of strings for stock names
    * guess: list of initial guess for allocations
    * risk_free_rate: estimated daily risk free return to calculate sharpe ratio
    """
    # perform some checks
    #assert len(guess) == len(symbols)
    assert np.sum(guess) == 1
    
    # get stock data, normalize and plot
    if 'SPY' in symbols:
        add_SPY = True
    else:
        add_SPY = False
    
    #df = get_data(symbols, dates, add_SPY=add_SPY)
    df_norm = normalize(df)
    plot_data(df_norm, title='Normalized Share Prices of Portfolio')
    
    # define optimizer with boundary conditions and constraints
    bounds = [(0,1) for a in guess] # optimal values need to be within [0,1]
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1}) # sum of allocations = 1      
    result = spo.minimize(negative_sharpe, guess, args=(df_norm, risk_free_rate), method='SLSQP', bounds=bounds, constraints=constraints, options={'disp':True})
    print("Results:", result)
    best_sharpe = (-1)*negative_sharpe(result.x, df_norm, risk_free_rate)
    print('Optimal allocations for {}: {} with sharpe ratio of {}'.format(symbols, np.round(result.x,4), np.round(best_sharpe, 2)))
    
def plot_data(df, title='Stock Prices'):
    ax = df.plot(title=title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()
    
def run():
    start_val=1000000
    start_date="2009-1-1"
    end_date="2011-12-31"
    symbols=["SPY", "XOM", "GOOG", "GLD"]
    allocs=[0.4, 0.4, 0.1, 0.1]    
    dates = pd.date_range(start_date, end_date)
    
    df = getData(dates, symbols)
    df = normalize(df)
    df, diz = allocateShares(df, symbols, allocs, start_val)
    print(df.sum(axis=1)  ) 
    plt.plot(df)
    plt.show()
    print(df)
    print(diz)
#    alloc_guess = [0.4, 0.4,0.1, 0.1] # initial guess for allocations
    
    # estimate risk free rate
    libor_yr = 0.023 #current annual libor rate is 2.3%
    risk_free_rate = np.power(1+libor_yr, 1/252)-1 # convert to daily rate
    
    run_portfolio_optimizer(dates, symbols, allocs, risk_free_rate, getData(dates, symbols))

#print(df1)
##np.cum
#for x in symbols:
#df1['Port_Val'] = df1.sum(axis=1)
#print(df1["GOOG cum_ret"])
#daily return
#today/yesterday -1
#for s in symbols:
#    daily = []
#    for i,x in enumerate(df1[s][:-1]):
#        daily.append(df1[s][i+1]/x-1)
#        print(df1[s][i+1]/x-1)
#    daily.insert(0,0)
#    df1[s+" d_ret"]=daily
#plt.plot(df1[["GOOG cum_ret", "SPY cum_ret"]])
#plt.show()
#print(df1)
#spy_mean = df1["SPY"].mean()
#spy_std = df1["SPY"].std()
#xom_mean = df1["XOM"].mean()
#xom_std = df1["XOM"].std()
#goog_mean = df1["GOOG"].mean()
#goog_std = df1["GOOG"].std()
#gld_mean = df1["GLD"].mean()
#gld_std = df1["GLD"].std()
#
#sharpe_ratio = {}
#for x in symbols:
#    x2=x+" sharpe_ratio"
#    sharpe_ratio[x2] = df1[x+" day_ret"].mean()/df1[x+" day_ret"].std() * math.sqrt(252)
    


#plt.plot(df1["SPY"], "go")

#np.std
#print(spy.columns.to_numpy().tolist())
#
#df=spy["Low"]
#print(df)

#line sono due coefficienti iniziali della retta (y=mx+b) sarebbero m(coeficiente angolare) e b (interceptor)
#data è una lista di dati
