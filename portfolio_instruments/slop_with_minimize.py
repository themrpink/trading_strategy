# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 01:05:18 2019

@author: themr
"""
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import math
import scipy.optimize as spo

spy = pd.read_csv("SPY.csv", parse_dates=True, usecols=["Date","Close", "Adj Close"], na_values="nan")
xom = pd.read_csv("XOM.csv", parse_dates=True, usecols=["Date","Close", "Adj Close"], na_values="nan")
goog = pd.read_csv("GOOG.csv", parse_dates=True, usecols=["Date","Close", "Adj Close"], na_values="nan")
gld = pd.read_csv("GLD.csv", parse_dates=True, usecols=["Date","Close", "Adj Close"], na_values="nan")

datay=np.array(spy["Close"].values)
dataz=np.array(xom["Close"].values)
datax=np.asarray(spy.index.values)
data=np.array([datax, datay, dataz]).T
print(datax, datay, dataz)
plt.plot(datax, datay, dataz, "ro")
def error(line, data):
    err = np.sum((data[:,1]- (line[0]*data[:,0] + line[1]))**2)
    return err

#define intial guess line
x_ends = np.float32([-5,5])

def fit_line(data, error_func):
    #intial guess
    l=np.float32([0, np.mean(data[:,1])]) #slop and intercept
    result = spo.minimize(error_func, l, args=(data,), method="SLSQP")
    return result.x

l_fit = fit_line(data, error)
plt.plot(data[:,0], l_fit[0]*data[:,0]+l_fit[1],"r--", linewidth=2.0, label="result guess")

plt.show()