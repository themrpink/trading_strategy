# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:50:32 2019

@author: themr
"""
import engine 

class positiveSignalEngine:
    def __init__(self, name, data_extractor):
        self.mainTPs=[15, 30, 60, 240, 360, 720, 1440, 4320, 10080] #15 min, 30 min, 1h, 4h, 6h, 12h, 24h, 3 giorni, 1 settimana
        self.data_extractor=data_extractor
        self.timestamp=0
        self.price=0
        self.required_return=0.05
        self.data=[]
        self.time_limit=False
        self.fees=0.0026
        price_target= self.price + self.price*self.required_return + (self.price*self.fees)
        self.price_target+= price_target*self.fees
        
    def search(self, indicator, TP_list=self.mainTPs):            
        diz_results={}       
        self.indicator=indicator                
        for TP in TP_list:
            sum_results=0
            name = indicator.name+str(TP)           
            filename=self.data_extractor.createTPFromRawFile(TP)
            candle_extractor = engine.CandleExtractor(filename)
            data, = candle_extractor.creaDiz(TP, self.timestamp)
            for row in data:
                if self.indicator.foundSignal(row):
                    data_for_result = data[data["timestamp"]>row["timestamp"]]  #prendere il data_for_result però dalla data del row attuale in poi                  
                    sum_results+=self.itHappened(data_for_result, indicator)
            diz_results[name]=sum_results
        return diz_results

        
    def itHappened(self, data):       
        for row in data[self.timestamp:]: #questo ovviamente va adatto al dataframe
            if self.indicator.fails(row, self.price):
                return -1
            if self.indicator.succeeds(row, self.price_target):
                return 1
        return -1
            
            
            
        #se dal punto in cui ci troviamo, il prezzo raggiunge in target richiesto prima che il prezzo
        #sia sceso al di sotto del prezzo iniziale, considera l´operazione riuscita
        #torna +1
        #altrimenti -1
        
        