# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:16:07 2019

@author: themr
"""
import engine
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#import engine

class CandlePrice:
    def __init__(self, data_extractor):
        self.data_extractor=data_extractor
        self.valueType="close"
        self.name="CandlePrice"
        
    def getData(self, timestamp, TP):
        self.filename="TP"+str(TP)+"_from_dictionary.csv"      
        filename=self.data_extractor.file
        self.data_extractor.createTPFromRawFile(filename, int(TP))    
        self.df = pd.read_csv(self.filename, usecols=[self.valueType, "timestamp"])
        self.df['timestamp'] = self.df['timestamp'].astype(int) 
        self.df=self.df[self.df.timestamp>timestamp]
        return self.df[self.valueType].tolist()
    