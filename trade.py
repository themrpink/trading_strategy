
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 23:54:23 2019
@author: themr
"""
# import math
# import os
# import numpy as np
# import talib as tl
# import json
# from datetime import datetime
# import matplotlib.pyplot as plt
# import csv
# import traceback
# import datetime as dt
# import matplotlib.dates as mdates
import pandas as pd
#import pandas_datareader as web
#from mpl_finance import candlestick_ohlc

result=pd.DataFrame([["1","2","3","4"]], columns=["prezzo acquisto", "prezzo vendita", "data acquisto", "data vendita"])
row={"prezzo acquisto":"123",  "prezzo vendita":"245",  "data acquisto":"ieri", "data vendita":"oggi"}
result=result.append(row, ignore_index=True)
print(result)


result.to_csv("result.csv")
    
capital=1000   #euro
amount=capital*0.1
risk=0.02
target=5        #%
stop=3          #%
maker_fee=0.13  #%
taker_fee=0.26  #%


def openFile(file):
    filename=file
    trade_file=pd.read_csv(filename, sep=",", header=1, names=["timestamp", "price", "volume"])
    trade_file.head(n=5)
    rows_n=len(trade_file.index)
    print(rows_n)
    
    
def makerLimits(amount, price, risk, maker_fee):
    target_risk=risk+0.01
    target_price=price*(1+target_risk-maker_fee)
    stop_price=price-(price*risk-taker_fee)


    result=pd.DataFrame(columns=["prezzo acquisto", "prezzo vendita", "data acquisto", "data vendita"])
    result=result.append("123", "245", "ieri", "oggi")
    result.to_csv("result.csv")
    
    return target_price, stop_price