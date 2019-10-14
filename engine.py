# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 23:54:23 2019

@author: themr
"""
import os
import numpy as np
import talib as tl
import json
from datetime import datetime
import matplotlib.pyplot as plt
import csv

class Engine:
    
    def __init__(self, name, data_extractor):
        self.name=name
        self.last_timestamp = "0"

        self.data_extractor = data_extractor
        self.layers = []  #lista ordinata di oggetti di tipo methods: quindi il punto é che l´user istanzia un oggetto metodo
                            #che contiene al suo interno le istanze degli indicatori che confronta.
                            #quindi il motodo piú semplice e sintetico per rappresentare un layer è un metodo stesso
        self.results = {}   
        self.buy_results = []#qua vengono salvati i risultati ( lista di dizionari)
        self.sell_results = []
        self.layers_structure = []  #questo è una lista di dizionari, ognuno ha un set di metodi. Questi vanno iterati fino a che non si trova il valore
        self.completed_strategies=[]
        self.saved_file=""
        
    def addLayer(self, layer):  #questo layer, che é un method, deve arrivare dalle selezioni dell´user
        self.layers.append(layer)

        
    def findBuySignal(self, strategy):
        print("chiamata iniziale, riga 34")
        count = 1
        next_strategy = True
        while next_strategy==True:
            next_strategy, result, self.last_timestamp = strategy.searchSignal(self.last_timestamp, count)
            strategy_name="strategy"+str(count)
            count+=1
            self.results[strategy_name]=result
            self.results[strategy_name]["timestamp"]=self.last_timestamp
            self.buy_results.append({"timestamp":self.last_timestamp, "data":result, "succeded":next_strategy})
    
    
    def findSellSignal(self, strategy):
        print("chiamata sell signal, riga 50")
        self.last_timestamp=0
        self.data_extractor=DataExtractor("test.csv")
        count = 1
        next_strategy = True
        while next_strategy==True:
            next_strategy, result, self.last_timestamp = strategy.searchSignal(self.last_timestamp, count)
            strategy_name="strategy"+str(count)
            count+=1
            self.results[strategy_name]=result
            self.results[strategy_name]["timestamp"]=self.last_timestamp
            self.sell_results.append({"timestamp":self.last_timestamp, "data":result, "succeded":next_strategy})
    
    def compareBuyAndSell(self):
        for buy_signal in self.buy_results:
            timestamp_buy = buy_signal["timestamp"]
            for sell_signal in self.sell_results:
                timestamp_sell = sell_signal["timestamp"]
                if timestamp_sell>=timestamp_buy:
                   self.completed_strategies.append((timestamp_buy, timestamp_sell))
                break
    
#    def findPrices(self):
#        with open(self.data_extractor.)
#    def findSignal(self):       
#     
#        i=0
#        signal=True
#        if len(self.layers)==0:
#            return False
#        timestamp=0
#        
#        while True:
#            
#            set_layers = self.layers_structure[0]
#            
#            for layer in set_layers:
##                tp = layer.TP
#                
#                check, result = layer.execute()
#                last_timestamp = int(result["timestamp"])
#                if last_timestamp > timestamp:
#                    timestamp=last_timestamp
#                self.results.append(result) 
#                if check is False:
#                    print("il motore restituisce false, riga 64")
#                    return False                          
#           
#            self.layers_structure = self.layers_structure[1:]
##            signal, resultData = self.layers[i].execute()
##            self.results.append(resultData)
#            if not signal:
#                print("il motore restituisce false, riga 71")
#                return False
#            i+=1
#            if i>= len(self.layers):
#                print("il motore restituisce, riga 75")
#                print(signal)
#                return signal
            
    def saveResults(self):
        print("saving results, riga 80")
        with open(self.name+".json", "w") as f:
            json.dump(self.results, f)
        return self.name+".json"
#    def checkStrategy(self, strategy):
        
        
#qua sappiamo a questo punto se il risultato lancia un segnale positivo o no
#devo capire come, a partire da un indice, ricavare di nuovo il timestamp
    
    
class Strategy:
    
    def __init__(self, layers):
        self.layers = layers
        self.results = {}
#        
#    def addlayer(self, layer):
#        self.layers.append(layer)
#        self.layers_copy.append(layer)
#        
    def searchSignal(self, last_timestamp, count):
        self.results={}
        count_layer=1
        print("chiamata strategia N."+str(count))
        for layer in self.layers:
            self.results["layer"+str(count_layer)] = []
            
            actual_timestamp = last_timestamp
            new_timestamp=0
            first_method = []
            check_if_true=False
            for method in layer:
                print("la strategia N."+str(count)+" chiama un metodo, riga 111")
                validity, result, timestamp = method.execute(actual_timestamp)
                if validity:
                    check_if_true=True
                first_method.append((int(timestamp), result))
                print("il metodo chiamato dalla strategia N "+str(count)+" ha restituito:, riga 113")
                print(validity, result, timestamp)
#                self.results["layer"+str(count)].append(result)
                new_timestamp = result["timestamp"]
            if int(new_timestamp)>int(last_timestamp):
                last_timestamp=new_timestamp
                print("e' stato aggiornato il timestamp, riga 119")
                    
            if not check_if_true:
                print("la strategia N "+str(count)+" ha ricevuto un valore finale negativo, torna false, riga 117")
                for x in first_method:
                    
                    self.results["layer"+str(count_layer)].append(x[1])
                return False, self.results, last_timestamp
            
            first_method.sort(key=lambda x: x[0])
            
            for x in first_method:
                self.results["layer"+str(count_layer)].append(x[1])
            self.results["layer"+str(count_layer)].append({"last_timestamp":last_timestamp})
            count_layer+=1
#        last_timestamp = self.results[self.layers[-1].name][-1]["timestamp"]
        print("la strategia N "+str(count)+" ha avuto successo, torna true, riga 127")
        return True, self.results, last_timestamp
        
#        
#    def remove(self, method):
#        group_dict = self.layers[0]
#        for key in group_dict:
#            group_dict[key].remove(method)
#            if len(group_dict[key])==0:
#                self.layers.remove(group_dict)
#                break
#            break
#        if len(self.layers)==0:
#            self.layers = self.layers_copy.copy()
#            return True
#        return False
#        
    
    

class PriceCross():
    
    def __init__(self, indicator1, indicator2, crossType, TP): #viene istanziato con due array di dati da due indicatori
        self.indicator1= indicator1  #istanza dell´indicatore
        self.indicator2 = indicator2
        self.ind1=indicator1.values  #array dell´indicatore
        self.ind2=indicator2.values 
        self.crossType = crossType   #"above" o "below" a seconda che si cerchi un cross che sale o che scende di ind1 su ind2
        self.TP=TP
#    def getData(self, timestamp):
#        
        
    def execute(self, last_timestamp):      
        print("lanciato execute dell metodo, riga 160")
        self.indicator1.getData(last_timestamp, self.TP)
        self.ind1=self.indicator1.getOutput2()
        self.indicator2.getData(last_timestamp, self.TP)
        self.ind2=self.indicator2.getOutput2()
        
        i=1
        diz={}
        while True:
#            print("check indici")
#            print(len(self.ind1))
#            print(len(self.ind2))
#            print(i)
            if i>=len(self.ind1)  or len(self.ind1)<=1 or i>=len(self.ind2):
                timestamp = self.indicator1.diz2["timestamp"][i-1]
                print("il metodo restituisce false, riga 175")
                return False, {"result": "{} didn´t cross {} -- timeperiod: {}".format(self.indicator1.name, self.indicator2.name, self.TP), "timestamp": self.indicator1.diz2["timestamp"][i-1]}, timestamp
            
            if  self.ind1[i-1]-self.ind2[i-1] < 0 and self.ind1[i]-self.ind2[i] > 0 and self.crossType=="above":
                diz = {"ind1":self.indicator1.name, 
                       "ind2":self.indicator2.name, 
                       "timeperiod":self.TP,
                       "time-index":i, 
                       "method-name": "Price Cross", 
                       "result": "{} crossed above {} ".format(self.indicator1.name, self.indicator2.name),
                     #  "date": self.indicator1.diz["date"].item(i),
                       "timestamp": self.indicator1.diz2["timestamp"][i]}
                timestamp = self.indicator1.diz2["timestamp"][i]
                print("il metodo restituisce true, riga 187")
                return True, diz, timestamp          #torna true se ind1 passa sopra a ind2
            
            if  self.ind1[i-1]-self.ind2[i-1] > 0 and self.ind1[i]-self.ind2[i] < 0 and self.crossType=="below":
                diz = {"ind1":self.indicator1.name, 
                       "ind2":self.indicator2.name,
                       "timeperiod":self.TP,
                       "time-index":i, 
                       "method-name": "Price Cross", 
                       "result": "{} crossed below {}".format(self.indicator1.name, self.indicator2.name),
                     #  "date": self.indicator1.diz["date"].item(i),
                       "timestamp": self.indicator1.diz2["timestamp"][i]}      
                timestamp = self.indicator1.diz2["timestamp"][i]
                print("il metodo restituisce true, riga 199")
                return True, diz, timestamp       #torna flase se ind1 passa sotto a ind2 (ovvero ind2 passa sopra a ind1)
            i+=1
            
        
        

#tutti gli indicatori
#allora: il periodo generale è dato dal data_object. 
class SMAClass:
    def __init__(self, data_extractor, timeperiod):
        
        self.timeperiod = timeperiod
        self.data_extractor = data_extractor
        self.values = np.zeros(1)
        self.name = "SMA indicator"+str(timeperiod)
        self.data_list = data_extractor.data
        self.value_type="close"
       # self.diz= self.setDataList()
        self.diz2= {}
        
          
    def getData(self, timestamp, TP):
        print("metodo getData dell indicatore, riga 221")
        if int(timestamp) > int(self.data_extractor.timestamp):
            print("aggiornato timestamp: vecchio="+str(timestamp)+" nuovo=")
            timestamp=self.data_extractor.updateFile(timestamp)
            print(timestamp)
        else:
            print("il timestamp non è maggiore, riga 228")
            print(str(timestamp)+"   "+str(self.data_extractor.timestamp))
        filename=self.data_extractor.updated_file
        if filename == "":
            filename=self.data_extractor.file
        print("il file da cui generare le candele ha nome: , riga 234")
        print(filename)
#        if not self.data_extractor.file_opened:
        self.data_extractor.createTPFromRawFile(filename, TP, timestamp)
#            self.data_extractor.file_opened=True
        
        print("apri il file "+ "TP"+str(TP)+".json nell indicatore, riga 239")
        print("file size, rga 240")
        print(str(os.path.getsize("TP"+str(TP)+".json")))
        with open("TP"+str(TP)+".json") as f:
            data = json.load(f)
#            print(data)
            n=len(data["TP"+str(TP)])
            print(n)
            i=0
#            diz ={"date": np.empty(), 
#                  "timestamp": np.zeros(n),
#                  "open":np.zeros(n),
#                  "close":np.zeros(n), 
#                  "high":np.zeros(n), 
#                  "low":np.zeros(n), 
#                  "volume":np.zeros(n), 
#                  "average":np.zeros(n),
#                  "direction":np.zeros(n)}
            diz ={"date": [], 
                  "timestamp": [],
                  "open": [],
                  "close":[], 
                  "high": [], 
                  "low": [], 
                  "volume": [], 
                  "average": [],
                  "direction": []}
            print("aggiungi i valori dell indicatore nei numpy arrays, riga 245")
            for candle in data["TP"+str(TP)]:
#                print(candle)
#                print(candle["date"])
#                np.append(diz["date"], candle["date"])
#                np.append(diz["timestamp"], candle["timestamp"])
#                np.append(diz["open"], candle["open"])
#                np.append(diz["close"], candle["close"])
#                np.append(diz["low"], candle["low"])
#                np.append(diz["high"], candle["high"])
#                np.append(diz["volume"], candle["volume"])
#                np.append(diz["average"], candle["average"])
#                np.append(diz["direction"], candle["direction"])
                diz["date"].append(candle["date"])
                diz["timestamp"].append(float(candle["timestamp"]))
                diz["open"].append(float(candle["open"]))
                diz["close"].append(float(candle["close"]))
                diz["low"].append(float(candle["low"]))
                diz["volume"].append(float(candle["volume"]))
                diz["average"].append(float(candle["average"]))
                diz["direction"].append(float(candle["direction"]))
                

#                diz["date"].flat[i]=candle["date"]
#                diz["timestamp"].flat[i]=candle["timestamp"]
#                diz["open"].flat[i]=float(candle["open"])
#                diz["close"].flat[i]=(float(candle["close"]))
#                diz["low"].flat[i]=(float(candle["low"]))
#                diz["volume"].flat[i]=(float(candle["volume"]))
#                diz["average"].flat[i]=(float(candle["average"]))
#                diz["direction"].flat[i]=(float(candle["direction"]))
                i+=1  
            print("converti in numpy array - inizio, riga 293")        
            diz["date"]=np.array(diz["date"])
            diz["timestamp"]=np.array(diz["timestamp"])
            diz["open"]=np.array(diz["open"])
            diz["close"]=np.array(diz["close"])
            diz["low"]=np.array(diz["low"])
            diz["volume"]=np.array(diz["volume"])
            diz["average"]=np.array(diz["average"])
            diz["direction"]=np.array(diz["direction"])
            print("converti in numpy array - fine, riga 301")
            print("crea il file myarray.csv, riga 302")
            np.savetxt("myArray.csv", diz["open"])
            
            print("salva il diz2")
            self.diz2=diz
            return diz, timestamp
        
    def setDataList(self):
#        self.data_list=data
          
        n=len(self.data_list)
        diz ={"date": np.zeros(n), 
              "timestamp": np.zeros(n),
              "open":np.zeros(n),
              "close":np.zeros(n), 
              "high":np.zeros(n), 
              "low":np.zeros(n), 
              "volume_btc":np.zeros(n), 
              "volume_usd":np.zeros(n)}
        i=0
        for x in self.data_list:
            #diz["date"].flat[i]=x.get("date")
            diz["timestamp"].flat[i]=(float(x.get("timestamp")))
            diz["open"].flat[i]=(float(x.get("open")))
            diz["close"].flat[i]=(float(x.get("close")))
            diz["low"].flat[i]=(float(x.get("low")))
            diz["volume_btc"].flat[i]=(float(x.get("volume_btc")))
            diz["volume_usd"].flat[i]=(float(x.get("volume_usd")))
            i+=1
        return diz
        
    def storeData(self):
        with open("store.json", "w") as f:
            json.dump(self.data_list, f)         
        
 
    def getDataFromDateToDate(self, begin, end):
        self.data_list = self.data.selectPeriodFromDates(begin, end)
        
    def getOutput(self):
        self.values = tl.SMA(self.diz[self.value_type], timeperiod=self.timeperiod)
        return self.values
    
    def getOutput2(self):
        print("è stato chiamato getOutput2, riga 337")
        
        self.values = tl.SMA(self.diz2[self.value_type], timeperiod=self.timeperiod)
        print("queste sono le values restituite dell indicatore:, riga 340")
        print(self.values)
        return self.values

##classe data

##classe motore
## ogni coppia deve avere lo stesso timelapse
#ogni volta che viene scelta una valuta e/o modificato il timelapse, viene:
#1)  istanziata una nuova Data class se necessario aprire un nuovo file
#2)  estratto un nuovo timelapse

#i dati vengono memorizzati in self.data ma anche è possibile salvarli in un file json
#self.data è una lista di dizionari, che per ogni candlestich hanno tutti i dati
#l'ideale sarebbe la lista di tutte le transazioni, dalla quale ricavare tutti i possibili timeperiods 
#con un nuovo apposito metodo

class DataExtractor:
    def __init__(self, file):
        self.file=file
        self.data= ""#self.extractData()
        self.TP_files = {}
        self.TP_files_csv = {}
        self.updated_file = ""
        self.timestamp = "0"
        self.file_opened=False
    
    
    def updateFile(self, timestamp): 
        
        print("update del file")
        data=""
        filename=""
        line=""
        if self.updated_file=="":
            print("prima volta, apro il file principale, riga 380")
            filename=self.file
        else:
            filename="updated_file.json"
            self.updated_file="updated_file.json"
            print("è stato aggiornato il nome del file a upgrade_file.json, riga 385")
        print("apro il file "+filename)
        with open(filename) as f:            
            line = f.readline()
            if line.split(",")[0]=="":
                return self.timestamp
            actual_timestamp = (line.split(",")[0])
            actual_timestamp=int(actual_timestamp)
            print("sta leggendo il file, riga 395")
            print("timestamp trasmesso:, riga 396")
            print(timestamp)
            print("timestamp attuale/iniziale del file:")
            print(actual_timestamp)
            while actual_timestamp<int(timestamp):
                line = f.readline()
    #                if line=="":
    #                    break
                actual_timestamp = int(line.split(",")[0])  
            
            data=f.readlines()
    
            print("file letto")
            print("timestamp a fine lettura:, riga 409")
            print(actual_timestamp)
            self.timestamp=actual_timestamp
            print("timestamp aggiornato, riga 412")
            print("grandezza del data estratto dal file: , riga 413:")
            print(len(data))
        self.updated_file="updated_file.json"
        filename="updated_file.json"
        with open(filename, "w") as f:
            print("sta scrivendo il file, riga 418")
            print(filename)
            for x in data:
                f.write(x)
            print("è stato scritto il file, linea 422")
        return self.timestamp#self.updated_file#, end
        

    def createTPFromRawFile(self, file, tpValue, timestamp):   #questo dovrà essere poi il self.file, così si usa sempre lo stesso timelapse
        print("chiamato createTPFfromRawFile")
        if not "TP"+str(tpValue) in self.TP_files or int(timestamp)>=int(self.timestamp):
#            self.timestamp=timestamp
            json_content={}
            csv_content = [["timestamp","date","open","close","high","low","volume","average","direction"]]
            print("apertura del file principale, nome file: , riga 439") 
            print(file)
            with open(file) as f:
                candle_data = []      
                first_line=f.readline()
                data = first_line.split(",")
                last_timestamp = data[0] 
#                date = datetime.fromtimestamp(int(last_timestamp))
                candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
                json_content["TP"+str(tpValue)] = []    
                
                for i, line in enumerate(f):
                    data = line.split(",")
                    actual_timestamp=data[0]
                    actual_tp = (float(actual_timestamp) - float(last_timestamp))/60 #number of minutes
                    checkTP = actual_tp / tpValue
                    
                    if checkTP>=1:   #se é il momento di creare una candela
                        last_timestamp=actual_timestamp  #aggiorna il timestamp al punto attuale                   
                        candlestick, candlestick_csv = self.createCandlestick(candle_data)  #chiama il metodo che crea la candela
                        json_content["TP"+str(tpValue)].append(candlestick)
                        csv_content.append(candlestick_csv)
                        candle_data.clear()
    
                    candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
            print("il file principale è stato trasformato in candele, riga 462")
            with open("TP"+str(tpValue)+".json", 'w', encoding='utf-8') as json_file:
                json.dump(json_content, json_file, ensure_ascii=False, indent=4)              #salva il file
                print("le candele sono stata scritte in un nuovo file, riga 465")
                print("TP"+str(tpValue)+".json")
            self.TP_files["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"
            
            with open("TP"+str(tpValue)+".csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(csv_content)            
            
            self.TP_files_csv["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"

            with open("TP"+str(tpValue)+"_from_dictionary.csv", "w") as csv_file:
                fields = ["timestamp","date","open","close","high","low","volume","average","direction"]
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(json_content["TP"+str(tpValue)])
        return self.TP_files["TP"+str(tpValue)]
    
    def createFile(self, file, tpValue):   #questo dovrà essere poi il self.file, così si usa sempre lo stesso timelapse
        print("chiamato createTPFfromRawFile")
        if not "TP"+str(tpValue) in self.TP_files:# or timestamp!=self.timestamp:
#            self.timestamp=timestamp
            json_content={}
            csv_content = [["timestamp","date","open","close","high","low","volume","average","direction"]]
            print("apertura del file principale, nome file: , riga 477") 
            print(file)
            with open(file) as f:
                candle_data = []          
                first_line = f.readline()
                print("first line, riga 516")
                print(first_line)
                data = first_line.split(",")
                last_timestamp = data[0] 
                last_timestamp = last_timestamp.replace("\"" , "")
                print(last_timestamp)
#                date = datetime.fromtimestamp(int(last_timestamp))
                candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
                json_content["TP"+str(tpValue)] = []    
                
                for i, line in enumerate(f):
                    line = line.replace("\"", "")
                    data = line.split(",")
                    actual_timestamp = data[0]
                    actual_tp = (float(actual_timestamp) - float(last_timestamp))/60 #number of minutes
                    checkTP = actual_tp / tpValue
                    
                    if checkTP>=1:   #se é il momento di creare una candela
                        last_timestamp = actual_timestamp  #aggiorna il timestamp al punto attuale                   
                        candlestick, candlestick_csv = self.createCandlestick(candle_data)  #chiama il metodo che crea la candela
                        json_content["TP"+str(tpValue)].append(candlestick)
                        csv_content.append(candlestick_csv)
                        candle_data.clear()
    
                    candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
            print("il file principale è stato trasformato in candele, riga 415")
            with open("TP"+str(tpValue)+".json", 'w', encoding='utf-8') as json_file:
                json.dump(json_content, json_file, ensure_ascii=False, indent=4)              #salva il file
                print("le candele sono stata scritte in un nuovo file, riga 418")
                print("TP"+str(tpValue)+".json")
            self.TP_files["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"
            
            with open("TP"+str(tpValue)+".csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(json_content["TP"+str(tpValue)])
                
            
        return self.TP_files["TP"+str(tpValue)]
    def checkTPFile(self, tpValue): 
#        if len(self.TP_files)==0:
#            return False
        if "TP"+str(tpValue) in self.TP_files:
            return True
        else:
            return False    
    
    
    def createCandlestick(self, candle_data):
        candlestick={}
        timestamp=int(candle_data[0]["timestamp"])
        date = datetime.fromtimestamp(timestamp)
        openprice = candle_data[0]["price"]
        close = candle_data[-1]["price"]
        
        numb_of_trades=0
        volume = 0
        sum_of_prices = 0
        high=0
        low=10000000
        
        for trade in candle_data:
            
            price = float(trade["price"])
            amount = float(trade["amount"])
            volume+=amount
            sum_of_prices+=price
            numb_of_trades+=1
            
            if price>high:
                high=price
            if price<low:
                low=price
        
        average = sum_of_prices / numb_of_trades
        direction = int(float(openprice)-float(close))
        
        candlestick["timestamp"] = timestamp
        candlestick["date"] = str(date)
        candlestick["open"] = openprice
        candlestick["close"] = close
        candlestick["high"] = high
        candlestick["low"] = low
        candlestick["volume"] = volume
        candlestick["average"] = average
        candlestick["direction"] = direction
        candlestick_csv = [timestamp, str(date), openprice, close, high, low, volume, average, direction]
        return candlestick, candlestick_csv
    
        #quando vorró adattare questa parte dovró cambiare: questo va bene per un file giä diviso in candlesticks
    def extractData(self):
        with open(self.file) as f:       
            trades=f.readlines() 
        
        btc_list=[]
        for line in range(2,len(trades)):      
            data=trades[line].split(",")
            date=data[0]
            timestamp= datetime.strptime(data[0], "%Y-%m-%d")
            timestamp= datetime.timestamp(timestamp)
#            print(timestamp)
            
            #potrei in realtà creare una lista di dizionari, con la data messa come chiave 
            btc_list.append({"date": date, 
                             "timestamp":timestamp,
                             "open": float(data[1]), 
                             "high": float(data[2]), 
                             "low": float(data[3]), 
                             "close": float(data[4]), 
                             "volume_btc": float(data[5]), 
                             "volume_usd": int(data[6].replace("\n", ""))})
#        print(btc_list)
#        self.data=btc_list
        return btc_list
            
    def selectPeriodFromDates(self, begin, end):    
        timestamp_begin = datetime.strptime(begin, "%Y-%m-%d")
        timestamp_end = datetime.strptime(end, "%Y-%m-%d")
        timestamp_begin = datetime.timestamp(timestamp_begin)
        timestamp_end = datetime.timestamp(timestamp_end)
        indice_iniziale = self.searchDates(self.data, timestamp_begin , 0, len(self.data))
        indice_finale = self.searchDates(self.data,timestamp_end , 0, len(self.data))
        return self.data[indice_iniziale:indice_finale]
  
    def selectPerdiodFromTimestamp(self, begin, end):
        timestamp_begin = datetime.strptime(begin, "%Y-%m-%d")
        timestamp_end = datetime.strptime(end, "%Y-%m-%d")
        timestamp_begin = datetime.timestamp(timestamp_begin)
        timestamp_end = datetime.timestamp(timestamp_end)
        indice_iniziale = self.searchDates(self.data, timestamp_begin , 0, len(self.data))
        indice_finale = self.searchDates(self.data,timestamp_end , 0, len(self.data))
        return self.data[indice_iniziale:indice_finale] 
    
    ##########################################################
    def createTimePeriod(self, timeperiod, begin, end):
        #da implementare quando avrò i files con tutte le transazioni:
        #creare i candlesticks per il timeperiod richiesto, con i relativi dati, nel timelapse richiesto
        return 0
    ##########################################################################
    
    #funzione ricorsiva per la ricerca logaritmica di un timestamp specifico, 
    #restituisce l`indice della lista con il valore più vicino per eccesso
    def searchDates(self, A, date, i,j):
        if i<j:
            m=(j+i)//2
            if A[m]["timestamp"]==date:
                return m
            if A[m]["timestamp"]>date:
                return self.searchDates(A, date, i, m)
            else:
                return self.searchDates(A, date, m+1, j)
        else:
            return i
        
    def extraxtAllDataInJson(self, filename):
        with open(filename, "w") as f:
            for x in self.data:
                json.dump(x, f) 
                
                
                
                
def drawResults(file):
    diz = {}
    with open(file) as f:
        diz = json.load(f)
    n=1   
    strategy = "strategy" + str(n)
    draw_array = []
    while strategy in diz:
        
        draw_array.append(int(diz[strategy]["timestamp"]))
#        layers = diz[strategy]
#        n_layer = 1
#        method = "layer"+str(n_layer)
#        layer_array = []
#
#        while method in layers:
#            for d in layers[method]:
#                layer_array.append(d["timestamp"])
#                
#            n_layer+=1
#            method = "layer"+str(n_layer)           
#        draw_array.append(layer_array)     
        n+=1        
        strategy = "strategy"+str(n)
    print(draw_array)
#    a=[]
#    
#    for x in draw_array:
#        for y in x:
#            a.append(y)
#    print(a)
#    np_array = np.array(a)  
    np_array = np.array(draw_array)
    plt.plot(np_array)
    plt.show()
  

###########################################################################
###########################################################################
###########################################################################


class VolumeGroup:
    
    def __init__(self):
        self.values = []
        

class Volume:
    
    def __init__(self, data_extractor, TP):
        self.timeperiod = TP
        self.data_extractor = data_extractor
        self.values = np.zeros(1)
        self.name = "Volume"
        self.data_list = data_extractor.data
        self.value_type = "volume"
        self.groups = []
        self.volumes_tuples=[]
        self.volume_originale=[]
        
          
    def getData(self, timestamp):
        
        print("apri il file "+ "TP"+str(self.timeperiod)+".json nell indicatore, riga 736")
        with open("TP"+str(self.timeperiod)+".json") as f:
            data = json.load(f)
#            print(data)
            n=len(data["TP"+str(self.timeperiod)])
            print(n)

            print("aggiungi i valori dell indicatore nei numpy arrays, riga 743")
            for candle in data["TP"+str(self.timeperiod)]:
                tupla=(float(candle["timestamp"]),float(candle["volume"]))
                self.volumes_tuples.append(tupla)
        self.volume_originale=self.volumes_tuples.copy()
        self.volumes_tuples.sort(key=lambda tupla: tupla[1])
            
        return self.volumes_tuples
    
    def createGroups(self):
        
        tupla1 = self.volumes_tuples[0]
        tupla2 = self.volumes_tuples[1]
        self.volumes_tuples.remove(tupla1)
        self.volumes_tuples.remove(tupla2)

        first_group = VolumeGroup()
        
        if tupla1[0]>tupla2[0]:
            first_group.values.append(tupla2)
            first_group.values.append(tupla1)
        else:
            first_group.values.append(tupla1)
            first_group.values.append(tupla2)    
            
        self.groups.append(first_group)
        
        for tupla in self.volumes_tuples:
            self.insertGroup(tupla)
            
        return self.groups
        
    def insertGroup(self, tupla):
               
            if tupla[0] < self.groups[0].values[0][0]:
                new_group = VolumeGroup()
                new_group.values.append(tupla)
                new_group.values.append(self.groups[0].values[-1])
                self.groups.insert(0,new_group)
                return

            for group in self.groups:
                if group.values[0][0]<tupla[0]<group.values[-1][0]:
                    for i in range(len(group.values)):
                        if group.values[i][0]>tupla[0]:
                            group.values.insert(i, tupla)
                            return
            
            group = self.groups[-1]
            new_group = VolumeGroup()
            new_group.values.append(group.values[-1])
            new_group.values.append(tupla)
            self.groups.append(new_group)
            return
            
    def convertToNP(self):  
        lista=[]
        lista_time=[]
        for group in self.groups:
            time=group.values[0][0]
            group.values[0]=(time,0)
            time=group.values[-1][0]
            group.values[-1]=(time,0)
            for value in group.values:
                lista.append(value[1])
                lista_time.append(value[0])
        np.array(lista)
        return lista,lista_time
            
    def printGraph(self, lista):
        
        plt.plot(lista)
        plt.show()        
        
        
        
##############################################################
        ######################################################
        ######################################################
        #############################################################################
class VolumeExtractor:
    
    def __init__(self, data_extractor, timeperiod):
        self.min_distance = 30
        self.timeperiod = timeperiod
        self.data_extractor = data_extractor
        self.values = np.zeros(1)
        self.name = "Volume"
       # self.data_list = data_extractor.data
        self.value_type = "volume"
        self.volumes_tuples=[]
        self.volume_blocks = []
    
    def getData(self):
 
        with open("TP"+str(self.timeperiod)+".json") as f:
            data = json.load(f)
    #            print(data)
           # n=len(data["TP"+str(self.timeperiod)])

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
                    if ((y.last-timestamp)/60)/self.timeperiod>=self.min_distance:
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
                    if ((timestamp-y.first)/60)/self.timeperiod>=self.min_distance:
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
                         
                elif y.first!=None and (0<((timestamp-y.first)/60)/self.timeperiod<self.min_distance):
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
                
                elif y.last!=None and (0<((y.last-timestamp)/60)/self.timeperiod<self.min_distance):
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
                    if ((timestamp-y.first)/60)/self.timeperiod>=self.min_distance and ((y.last-timestamp)/60)/self.timeperiod>=self.min_distance:# and j<(len(self.volume_blocks)-1):
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

                
                elif y.first!=None and ((timestamp-y.first)/60)/self.timeperiod>=self.min_distance:
                    y.last=timestamp
                    y.candles.append(x)
                    new_block=VolumeBlock()
                    new_block.first=timestamp
                    self.volume_blocks.append(new_block)
                    check=True
                    break
                
                elif y.last!=None and ((y.last-timestamp)/60)/self.timeperiod>=self.min_distance:
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
       
    def printGraph(self, lista):
        
        plt.plot(lista)
        plt.savefig('plot_name.png', dpi = 300)
        plt.show()
        
        
class VolumeBlock:
    
    def __init__(self):
        self.first = None
        self.last = None
        self.candles = []
if __name__ == "__main__":
    
#crea il data_extractor
    
    data_extractor = DataExtractor("test.csv")

#crea strategie

    sma = SMAClass(data_extractor, 30)
    sma.value_type="low"
    sma.timeperiod=30
    
    sma2 = SMAClass(data_extractor, 20)
    sma2.value_type="low"
    sma2.timeperiod=20
    
    sma3 = SMAClass(data_extractor, 100)
    sma3.value_type="low"
    sma3.timeperiod=100
    
    sma4 = SMAClass(data_extractor, 50)
    sma4.value_type="low"
    sma4.timeperiod=50    
    
    met1 = PriceCross(sma, sma2, "above", 100)
    met2 = PriceCross(sma2, sma3, "above", 50)
    met3 = PriceCross(sma3, sma4, "above", 100)
    
    layer1 = {met1, met2}
    layer2 = {met3}
    
    strategy = Strategy([layer1,layer2])
    data_extractor = DataExtractor("test.csv")

#crea strategie

    sma = SMAClass(data_extractor, 30)
    sma.value_type="low"
    sma.timeperiod=30
    
    sma2 = SMAClass(data_extractor, 20)
    sma2.value_type="low"
    sma2.timeperiod=20
    
    sma3 = SMAClass(data_extractor, 100)
    sma3.value_type="low"
    sma3.timeperiod=100
    
    sma4 = SMAClass(data_extractor, 50)
    sma4.value_type="low"
    sma4.timeperiod=50 
    met4 = PriceCross(sma, sma2, "below", 20)
    met5 = PriceCross(sma2, sma3, "above", 50)
    met6 = PriceCross(sma3, sma4, "below", 30)
    
    layer3 = {met4, met5}
    layer4 = {met6}
    
    strategy2 = Strategy([layer3,layer4])
    
    engine = Engine("motore1", data_extractor)
    engine.findBuySignal(strategy)
    print(engine.results)
    nome_file = engine.saveResults()
    drawResults("motore1.json")
#    
    engine.findSellSignal(strategy2)
    print(engine.results)
    nome_file = engine.saveResults()
    drawResults("motore1.json")
    data_extractor.createFile("test3.csv", 1440)
    
    
    engine.compareBuyAndSell()
    print("ùùùùùùùùùùùùùùùùùùùùùùùùùùù")
    print(engine.completed_strategies)
    print(engine.sell_results)
    print("ùùùùùùùùùùùùùùùùùùùùùùùùùùù")
#    volume = Volume(data_extractor, 1440)
#    volume.getData(0)
#    lista1=[]
#    for x in volume.volume_originale:
#        lista1.append(x[1])
#    volume.printGraph(np.array(lista1))
#    volume.createGroups()
#    lista,lista_time=volume.convertToNP()
#    volume.printGraph(lista)
   # print(lista_time)
    
    volume2=VolumeExtractor(data_extractor, 1440)
    volume2.getData()
    volume2.createGroups()
    lista, lista_time=volume2.convertToNP()
    volume2.printGraph(lista)
    print(len(volume2.volume_blocks))
#    for x in volume2.volume_blocks:
#        print(x.first)
#        print(x.last)
#        
#    print(engine.buy_results)
  #  print(lista_time)
