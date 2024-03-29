# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:16:27 2019

@author: themr
"""
import numpy as np
import json
import matplotlib.pyplot as plt
import engine
import pandas as pd
class VolumeExtractor:   
    def __init__(self, data_extractor):
        self.distance = 20
        self.timeperiod = 240
        self.data_extractor = data_extractor
        self.values = np.zeros(1)
        self.name = "Volume"
        self.value_type = "volume"
        self.volumes_tuples=[]
        self.volume_blocks = []
   
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.volumes_tuples=[]
        self.volume_blocks = []
        
        
    def execute(self, timestamp):
        self.getData()
        self.createGroups()
        self.lista, self.listaTime = self.convertToNP()
        
    def getData(self): 
        with open("TP"+str(self.timeperiod)+".json") as f:
            data = json.load(f)
            for candle in data["TP"+str(self.timeperiod)]:
                tupla=(float(candle["timestamp"]),float(candle["volume"]))
                self.volumes_tuples.append(tupla)       
        self.volumes_tuples.sort(key=lambda tupla: tupla[1])  
        return self.volumes_tuples
   
    
    def createGroups(self):
        tupla = self.volumes_tuples[0]
        block1 = VolumeBlock()
        block2 = VolumeBlock()
        block1.last = tupla[0]
#        block1.first=0
        block1.candles.append(tupla)
        block2.first = tupla[0]
#        block2.last = tupla[0] + (tupla[0]/self.timeperiod)*self.min_distance
        block2.candles.append(tupla) 
        self.volume_blocks.append(block1)
        self.volume_blocks.append(block2)
        
        for x in self.volumes_tuples[1:]:
            timestamp = x[0]
            for j,y in enumerate(self.volume_blocks):
                check=False
                if y.first==None and timestamp<y.last:                               
                    if ((y.last-timestamp)/60)/self.timeperiod>=self.distance:
                        y.first=timestamp
                        y.candles.insert(0, x)
                        check=True
                    else:
                        for i,t in enumerate(y.candles):
                            if timestamp<t[0]:
                                y.candles.insert(i, x)
                                check=True
                                break
                        if not check:
                            y.candles.append(x)
                            check=True
                            break
                elif y.last==None and timestamp>y.first:                     
                    if ((timestamp-y.first)/60)/self.timeperiod>=self.distance:
                        y.last=timestamp
                        y.candles.append(x)
                        check=True
                    else:
                        for i,t in enumerate(y.candles):
                            if timestamp<t[0]:
                                y.candles.insert(i, x)
                                check=True
                                break
                        if not check:
                            y.candles.append(x)
                            check=True
                            break
                         
                elif y.first!=None and (0<((timestamp-y.first)/60)/self.timeperiod<self.distance):
                    for i, value in enumerate(y.candles):
                        if value[0]>timestamp:
                            y.candles.insert(i,x)
                            check=True
                            break
                   

                    if not check:
                        y.candles.append(x)
                        check=True
                        break  
                    break
                
                elif y.last!=None and (0<((y.last-timestamp)/60)/self.timeperiod<self.distance):
                    for i, value in enumerate(y.candles):
                        if value[0]>timestamp:
                            y.candles.insert(i,x)
                            check=True
                            break
                        
                    if not check:
                        y.candles.append(x)
                        check=True
                        break                        
                    break 
                
                elif y.first!=None and y.last!=None:     
                    if ((timestamp-y.first)/60)/self.timeperiod>=self.distance and ((y.last-timestamp)/60)/self.timeperiod>=self.distance:# and j<(len(self.volume_blocks)-1):
                        new_block=VolumeBlock()
                        new_block.first=timestamp
                        new_block.last=y.last
                        
                       # new_block.candles.append(x)
                        y.last=timestamp
                        #y.candles.append(x)
                        k=0
                        for i,t in enumerate(y.candles):
                            if t[0]>timestamp:
                                k=i-1
                                check=True
                                break
                        new_block.candles=y.candles[k:]
                        new_block.candles.insert(0, x)
                        y.candles=y.candles[:k+1]
                        y.candles.append(x)
                        self.volume_blocks.insert(j+1, new_block)
                        check=True
                        break

                
                elif y.first!=None and ((timestamp-y.first)/60)/self.timeperiod>=self.distance:
                    y.last=timestamp
                    y.candles.append(x)
                    new_block=VolumeBlock()
                    new_block.first=timestamp
                    self.volume_blocks.append(new_block)
                    check=True
                    break
                
                elif y.last!=None and ((y.last-timestamp)/60)/self.timeperiod>=self.distance:
                    y.first=timestamp
                    y.candles.insert(0,x)
                    new_block=VolumeBlock()
                    new_block.last=timestamp
                    self.volume_blocks.insert(0,new_block)
                    check=True
                    break
           
                if check==True:
                    break       
   
    
    def convertToNP(self):  
        lista=[]
        lista_time=[]
        for group in self.volume_blocks:       
            for value in group.candles:
                if group.first==value[0] or group.last==value[0]:
                    lista.append(0)
                else:
                    lista.append(value[1])
                lista_time.append(value[0])
        np.array(lista)
        return lista,lista_time
       
    
    def printGraph(self): 
        self.getData()
        self.createGroups()
        lista, listaTime = self.convertToNP()
        print("ee")
        plt.plot(lista)
        plt.savefig('plot_name.png', dpi = 300)
        plt.show()
        

        
class VolumeBlock:    
    def __init__(self):
        self.first = None
        self.last = None
        self.candles = []


class TrendSpot:
    def __init__(self, data_extractor):
        self.data_extractor = data_extractor
        self.TP=240
        self.raggio=10
        self.tolleranza = 0.5
        self.trend=False
        self.dati_per_plot=[]   
        self.point_in_list=""
        self.name="TrendSpot"
        
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.dati_per_plot=[] 
        self.point_in_list==""
        
    def execute(self, timestamp):
        dati_raggio=[]
        date=""
#        try:
        with open("TP"+str(self.TP)+".json") as f:
            data = json.load(f)
            i=1     
            j=0
            for k,candle in enumerate(data["TP"+str(self.TP)]): #riprende dal timestamp passato come argomento
                if int(candle["timestamp"]) >= int(timestamp):
                    j=k
                    break
                
            print(len(data["TP"+str(self.TP)]))
            for candle in data["TP"+str(self.TP)][j:]:
                if i==int(self.raggio):
                    self.checkRaggio(dati_raggio)
                    break
                low=float(candle["low"])
                high=float(candle["high"])
                close=float(candle["close"])
                media=(low+high)/2
                if close==media:
                    dati_raggio.append((0, candle["date"]))
                else:
                    new_high=high-media
                    new_close=close-media
                    perc=new_close/new_high
                    dati_raggio.append((perc,candle["date"])) 
                i+=1
            print(len(data["TP"+str(self.TP)]))
            if len(data["TP"+str(self.TP)])>j+int(self.raggio):
                for candle in data["TP"+str(self.TP)][j+int(self.raggio):]:
                    dati_raggio=dati_raggio[1:]
                    low=float(candle["low"])
                    high=float(candle["high"])
                    close=float(candle["close"])
                    media=(low+high)/2
                    self.timestamp=int(candle["timestamp"])
                    if close==media:
                        dati_raggio.append((0,candle["date"]))
                    else:
                        new_high=high-media
    #                    new_low=0
                        new_close=close-media
                        perc=new_close/new_high
                        dati_raggio.append((perc,candle["date"]))              
                        
                    check, date = self.checkRaggio(dati_raggio)
                    if check:
    #                    timestamp=datetime.datetime.timestamp(datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S'))
                        print(self.timestamp)
                        if self.point_in_list=="":
                            self.point_in_list=len(self.data_extractor.result_objects)
                            self.df=pd.DataFrame({"date":[pd.to_datetime(self.timestamp, unit="s")]})
                            self.df1=pd.DataFrame({close})
                            self.resultObject=engine.ResultsToPlot()   
                            self.resultObject.print_just_points=True
                            self.resultObject.x=self.df
                            self.resultObject.y=self.df1#np.array([close])
                            self.resultObject.name=self.name
                            self.data_extractor.result_objects.append(self.resultObject)
                        else:
                            self.df=pd.DataFrame({"date":[pd.to_datetime(self.timestamp, unit="s")]})
                            self.df1=pd.DataFrame({close})
                            self.data_extractor.result_objects[self.point_in_list].x=self.data_extractor.result_objects[self.point_in_list].x.append(self.df)
                            print(self.data_extractor.result_objects[self.point_in_list].x)
                            self.data_extractor.result_objects[self.point_in_list].y=self.data_extractor.result_objects[self.point_in_list].y.append(self.df1)
#                            np.append(self.data_extractor.result_objects[self.point_in_list].y, close)
                        return True, {"result": "SpotTrend found a trend",
                                      "ind1": "raggio={}, tolerance={}".format(self.raggio, self.tolleranza),
                                      "method-name":"TrendSpot",
                                      "timestamp":self.timestamp, 
                                      "tolleranza":self.tolleranza, 
                                      "raggio":self.raggio, 
                                      "date":date, 
                                      "timeperiod":self.TP}, timestamp ,[("TrendSpot",date)]
            else:
                print("arrivati al termine della lista di candele, riga 261 methods.py")
#        timestamp=datetime.datetime.timestamp(datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S'))
        return False, {"result": "SpotTrend didn´t found a trend",
                       "method-name":"TrendSpot",
                       "timestamp":self.timestamp,
                       "tolleranza":self.tolleranza, 
                       "raggio":self.raggio, 
                       "timeperiod":self.TP}, timestamp ,[("TrendSpot",date)]
#    
#        except:
#            print("c´é stato un errore, lancio createFile e rilancio execute di TrendSpot")
#            self.data_extractor.createFile(self.data_extractor.file, self.TP)
#            self.execute(timestamp)
#            
    def checkRaggio(self, raggio):
#        print(raggio)
        value=0.0

        for x in raggio:
            value+=x[0]
        l=len(raggio)
        if value/l>=float(self.tolleranza):
            self.trend=True
#            print(raggio[0][1],raggio[-1][1])
        else:
            self.trend=False
        
        return self.trend, raggio[-1][1]

    
    def drawAndSave(self):
        filename="saved_trendspot"
        self.filename=filename
        self.dati_per_plot=[] 
        dati_raggio=[]
        if self.data_extractor=="":
            return
        if self.data_extractor.checkTPFile(self.TP):
            with open("TP"+str(self.TP)+".json") as f:
                data = json.load(f)
                i=1
                j=0
                for candle in data["TP"+str(self.TP)][j:]:
                    if i==int(self.raggio):
                        self.checkRaggio(dati_raggio)
                        break
                    low=float(candle["low"])
                    high=float(candle["high"])
                    close=float(candle["close"])
                    media=(low+high)/2
                    if close==media:
                        dati_raggio.append((0, candle["date"]))
                    else:
                        new_high=high-media
                        new_close=close-media
                        perc=new_close/new_high
                        dati_raggio.append((perc,candle["date"])) 
                    i+=1
                print(len(data["TP"+str(self.TP)]))
                if len(data["TP"+str(self.TP)])>j+int(self.raggio):
                    for candle in data["TP"+str(self.TP)][j+int(self.raggio):]:
                        dati_raggio=dati_raggio[1:]
                        low=float(candle["low"])
                        high=float(candle["high"])
                        close=float(candle["close"])
                        media=(low+high)/2
                        self.timestamp=int(candle["timestamp"])
                        if close==media:
                            dati_raggio.append((0,candle["date"]))
                        else:
                            new_high=high-media
        #                    new_low=0
                            new_close=close-media
                            perc=new_close/new_high
                            dati_raggio.append((perc,candle["date"]))              
                            
                        check, date = self.checkRaggio(dati_raggio)
                        if check:
                            self.dati_per_plot.append(float(candle["close"]))
                        else:
                            self.dati_per_plot.append(0)
                            
            with open(filename+".txt", "w") as f:
                for x in self.dati_per_plot:
                    f.writelines(str(x)+",")
#                f.writelines(self.dati_per_plot)
         
            plt.plot(np.array(self.dati_per_plot))
            plt.savefig(filename+".png", dpi = 300)
            plt.show()
            print(self.dati_per_plot)
            return self.dati_per_plot
        else:
#            try:
            print("retry and go", filename)
            self.data_extractor.createTPFromRawFile(self.TP)
#                self.drawAndSave()
#            except:
#                print("error")
#                return
            
            
if __name__ == "__main__":
    cr = TrendSpot()
    cr.TP=240
    cr.raggio=20
    cr.tolleranza=0.4
    date=cr.calcolaRaggio()
    print(date)
    