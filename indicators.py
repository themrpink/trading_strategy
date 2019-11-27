# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:16:07 2019

@author: themr
"""
import engine
import pandas as pd
import matplotlib.pyplot as plt


"""
oggetto generico candela con dei metodi che serviranno poi ad analizzare i prezzi
"""
class Candle:
    def __init__(self):
        self.volume=0
        self.real_body=0
        self.open=0
        self.close=0
        self.upper_shadow=0
        self.lower_shadow=0
        self.name="candle"
        self.criterio="close"
        self.stop_tolerance=1.0   
        
    """
    controlla se il prezzo attuale è sceso sotto il prezzo d' acquisto
    """
    def fails(self, row, price):
        if float(row["close"])<price:
            return True
        return False
    """
    controlla se il prezzo attuale è arrivato al prezzo target
    """    
    def succedes(self, row, target_price):
        target_price = target_price*self.stop_tolerance
        if float(row["high"]>=target_price):
            return True
        return False
    
    def foundSignal(self, row):
        self.volume=row["volume"]
        self.open=row["open"]
        self.close=row["close"]
        self.upper_shadow=row["upper_shadow"]
        self.lower_shadow=row["lower_shadow"]       
        return False
    
"""
Estende @Candle
"""
def GreenHammerCandle(Candle):
    def __init__(self):
        self.name = "green hammer candle"
    
    def foundSignal(self, row):
        volume=row["volume"]
        open_price=row["open"]
        close_price=row["close"]
        upper_shadow=row["upper_shadow"]
        lower_shadow=row["lower_shadow"]
        #stabilire i criteri per la candela
        #le percentuali perché una candela sia di un tipo piuttosto che di un altro
        #a quel punto confronta i dati, vedi se corrispondono
        #tipo: il close è entro una certa percentuale piú piccolo dell´high?
        #l´open é sopra una certa percentuale (direi il 50%) piú grande del low?
        #in proporzione al TP, oppure all´open e al close, ha una coda abbastanza lunga?
        #questa ultima opzione ci devo ragionare su
        

"""
individua il trend del volume, l'andamento tramite la funzione della retta che 
passa tra i valori di un blocco di dimensioni date di volume
"""
class VolumeSpotter:
    def __init__(self, size, data):
        self.size=size
        self.data=data
        self.volume_points=[]
    def checkTimestamp(self, timestamp, TP):
        starting_candle = timestamp - (TP*size*60)
        data=data[data["timestamp"]>starting_candle]
        #ecco adesso lui guarda le prime "size" candele e verifica se hanno un andamento positivo
        for i in range(size):
            data[i]["volume"].append(self.volume_points)
            
        #adesso cerca la retta col minimizzatore e verifica se l´andamento é positivo o negativo
        return True or False #a seconda dello slop della retta che ottengo con il minimozzatore
        
        
        
class CandlePrice:
    def __init__(self, data_extractor):
        self.data_extractor=data_extractor
        self.valueType="close"
        self.name="CandlePrice"
        self.resultObject=""
        
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.resultObject=""
        
    def getData(self, timestamp, TP):
        self.filename="TP"+str(TP)+"_from_dictionary.csv"      
#        filename=self.data_extractor.file
        self.data_extractor.createTPFromRawFile(int(TP))    
        self.df = pd.read_csv(self.filename, usecols=[self.valueType, "timestamp"])
        self.df['timestamp'] = self.df['timestamp'].astype(int) 
        self.df=self.df[self.df.timestamp>timestamp]
        if self.resultObject=="":
            self.df["date"]=pd.to_datetime(self.df["timestamp"], unit="s")
            self.resultObject=engine.ResultsToPlot()
            self.resultObject.x = self.df["date"]
            self.resultObject.y = self.df[self.valueType]
            self.resultObject.name=self.name
            self.data_extractor.result_objects.append(self.resultObject)
        return self.df[self.valueType].tolist()
    