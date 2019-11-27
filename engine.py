# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 23:54:23 2019

@author: themr
"""
import math
import os
import numpy as np
import talib as tl
import json
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import traceback
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
#import pandas_datareader as web
from mpl_finance import candlestick_ohlc

class Engine:
    
    def __init__(self, name, data_extractor):
        self.name=name
        self.last_timestamp = "0"
        
        self.data_extractor = data_extractor
        self.layers = []  #lista ordinata di oggetti di tipo methods: quindi il punto é che l´user istanzia un oggetto metodo
                            #che contiene al suo interno le istanze degli indicatori che confronta.
                            #quindi il metodo piú semplice e sintetico per rappresentare un layer è un metodo stesso
        
        """
        dizionario di dizionari delle strategie->layers->metodi.
        contiene un dizionario per ogni strategia:
            -ciascuno di questi contiene un dizionario di layer. 
                -Ogni layer contiene una lista di dizionari 
                    -Ogni dizionario contiene i risultati di un metodo
                    -un timestamp alla fine della lista se il layer è andato a buon fine
            
        I risultati di ogni metodo sono dizionari in varie forme, ma in generale {risultato, timestamp, inicatori, TP, nome del metodo, ecc}
        
        ###Struttura###      
          {
               "strategia1": 
                   {
                      "nome layer1": 
                                      [ 
                                        {"dati risultati metodo1"}, 
                                        {"dati risultati metodo2"}, 
                                        {}...
                                      ],
                
                      "nome layer2": 
                                      [ 
                                        {"dati risultati metodo1"}, 
                                        {"dati risultati metodo2"}, 
                                        {}..
                                      ],
                          
                       "..."
                     },
                       
                "strategia2": {...}
          }
               
        """
        self.results = {}   
        #
        """
        self.buy_results è nella forma: 
            lista di dizionari di tutte le strategie (riuscite o meno)
            i dizionari sono nella forma {timestamp, succeded(True/False), strategy name}
        """
        self.buy_results = []#qua vengono salvati i risultati ( lista di dizionari)
        """
        self.sell_results è analogo a self.buy_results
        """
        self.sell_results = []
#        self.layers_structure = []  #questo è una lista di dizionari, ognuno ha un set di metodi. Questi vanno iterati fino a che non si trova il valore
        
        """
        lista di tuple (timestamp buy, timestamp sell)
        """
        self.completed_strategies=[]
        self.saved_file=""
        """
        lists_for _plot è una [lista di liste]:
        -ogni lista contenuta in essa è a sua volta una [lista di tuple], tante quante sono gli indicatori del metodo.
            -Ogni tupla è della forma ("nome indicatore", [lista con tutti i valori dell´indicatore] )
            
            
                [ 
                    [
                        [
                            ("nome indicatore1", [valori indicatore]),
                            ("nome indicatore2", [valori indicatore]),
                         
                        ]
                    ],
                        
                    [
                       [
                            ("nome indicatore1", [valori indicatore]),
                            ("nome indicatore2", [valori indicatore]),
                         
                        ]       
                    ]
                ] 
        """
        self.lists_for_plot=[]
        
#    def addLayer(self, layer):  #questo layer, che é un method, deve arrivare dalle selezioni dell´user
#        self.layers.append(layer)

        
    def findBuySignal(self, strategy):
#        print("chiamata iniziale, riga 34")
        count = 1
        next_strategy = True
        while next_strategy==True:
            next_strategy, result, self.last_timestamp, list_for_plot = strategy.searchSignal(self.last_timestamp, count)
            if count==1:
                self.lists_for_plot.append(list_for_plot)
            strategy_name="buy_strategy"+str(count)
            count+=1
            self.results[strategy_name]=result
            self.results[strategy_name]["timestamp"]=self.last_timestamp
#            if next_strategy:
            self.buy_results.append({"timestamp":self.last_timestamp, "succeded":next_strategy, "strategy":strategy_name})
        self.data_extractor.updated_file=""
    
    
    def findSellSignal(self, strategy):
#        print("chiamata sell signal, riga 50")
#        self.last_timestamp=0
        count = 1
        next_strategy = True
        while next_strategy==True:
            next_strategy, result, self.last_timestamp, list_for_plot = strategy.searchSignal(self.last_timestamp, count)
            if count==1:
                self.lists_for_plot.append(list_for_plot)
            strategy_name="sell_strategy"+str(count)
            count+=1
            self.results[strategy_name]=result
            self.results[strategy_name]["timestamp"]=self.last_timestamp
#            if next_strategy:
            self.sell_results.append({"timestamp":self.last_timestamp, "succeded":next_strategy, "strategy":strategy_name})
        self.data_extractor.updated_file=""
        """
        qual era il concetto? io compro entro un certo punto di vista:
        lui cerca entro un certo periodo di tempo il momento per vendere. 
        io vedo le seguenti possibilità:
            per il live trading:
            - vendi se il prezzo raggiunge una certa percentuale
            - oppure se scende sotto a un certo prezzo
            - oppure non vendere e corri il rischio
            per le statistiche:
            - cerca il prezzo migliore e dopo quanto è successo (sarà poi possibile controllare se ci sono altre condizioni favorevoli identificabile, tramite incrocio di dati)
            - cerca il prezzo medio       
            
        devo quindi iniziare a pensare ai risultati. Intanto mi sa che la cosa migliore è salvare i dati.
        dividere il tempo in blocci da 5 minuti. Mi sembra ragionevole. Oppure anche in secondi, ma meglio dividere. 
        5 minuti sono 300 secondi, questo è un intervallo di timestamp ragionevole, e i dati che ho si devono adattare al mio
        standard, in modo che tutto corrisponda. Certo salvo anche una copia con tutti i dati precisi, cioè una lista
        o una tabella di tutti i segnali nello specifico timestamp, ma subito li converto in candele da 5 minuti
        a ogni candela quindi possono corrispondere  infiniti dati. Risultati di ogni tipo. Anche a ogni risultato posso corrispondere
        candele, e altri risultati, e ogni tipo di informazione.
        
        una cosa: impossibile nel trading lavorare con valori precisi e assoluti. Prendere un livello e sperare che questo venga
        rispettato. sono punti di attrazione e repulsione magnetica, ma non sono perfetti, né precisi. Quindi devo adottare
        un modo flessibile, elastico, che tenga conto della forza elestatica dei prezzi.
        
        
        """
    def buyAndWait(self, strategy, time_distance, limit=0.02):
        time_distance = int(time_distance)*3600  #tempo da aggiungere al timestamp entro il quale cercare occasioni di vendita
        all_rows=[]
        buy_prices=[]
        self.last_timestamp=0
        self.findBuySignal(strategy)
        file = self.data_extractor.file
        print(file)
        sell_timeframes=[]
        print("buy results")
        print(self.buy_results)
        """
        per i dati in buy results. Per tutti quelli che hanno avuto successo, cioè per ogni segnale positivo di buy, lui diciamo
        che compra e poi vede quello che succede. Per ogni segnale lui apre il file, e già qua vediamo che potrei usare un dataframe
        
        """
        print(file)

#        df = pd.read_csv(file, sep="," ,header=None)
#        df.colums=["timestamp", "price", "volume"]
#        df['timestamp'] = df['timestamp'].astype(int)
#        df['price'] = df['price'].astype(int)
#        df['volume'] = df['volume'].astype(int)
#        
#        print(df)

        
        for result in self.buy_results:
            if result["succeded"]:
                timestamp = int(result["timestamp"])
                with open (file, "r") as f:
                     csv_reader = csv.reader(f, delimiter=',')
                     for row in csv_reader:                       
                         if len(row)==1:
                             row=row[0].split(",")
                         if int(row[0])>=timestamp:
                             print(timestamp)
                             buy_price=float(row[1])  #questi buy price devo salvarli per poi associarli con il sell price finale
                             print(buy_price)
                             buy_prices.append((timestamp,buy_price))
                             tuple_list, rows = self.wait(buy_price, timestamp, file, timestamp+time_distance)
                             sell_timeframes.append(tuple_list)
                             all_rows.append(rows)
                             break
#        print(sell_timeframes)
#        print(all_rows)
        tot_price=0
        numb_of_prices=0
        for timeframe in sell_timeframes: #per ogni lista di tuple (di un buy signal)
            numb_of_prices+=1   #conta i rows
            max_price = (0,0)   #azzera il max price
            for tupla in timeframe: #per ogni tupla del buy signal
                price = tupla[1]    #seleziona il prezzzo
                if price > max_price[1]:    #se è maggiore del massimo (relativo a questo buy signal)
                    max_price=tupla        #nuovo max price
            tot_price+=max_price[1]     #tiena la somma di tutti i max prices di tutti i buy signals
        if numb_of_prices!=0:
            average_max_price = tot_price/numb_of_prices #fa la media di tutti i valori massimi di tutti i buy signals
        print("average max price")
        print(average_max_price)
        
        """
        restituisce le tuple di tuple ( (buy_timestamp, buy_price), (sell_timestamp, price_timestamp) )
        """
        results=[]      #segnali generati se il prezzo raggiunge una certa percentuale
        for i,buy in enumerate(buy_prices):
            sell_price= buy[1]*limit+buy[1]
            try:
                #se fallisce non ha trovato segnali e la lista è vuota
                sell_signal=[x for x in sell_timeframes[i] if x[1] >= sell_price if x[1]<buy[1]][0]
                results.append((buy, sell_signal))
            except:
                #all_rows lista i (corrispondente al buy attuale) -1 perchè delle lista vogliaom l'ultimo
                #(perchè non ha trovato un sell quindi vende all'ultimo row) e 1 perchè del row vogliamo il prezzo
                results.append((buy, (buy[0]+time_distance,float(all_rows[i][-1][1]))))
        
        sell_signals=[]
        for rows in all_rows:
            for row in rows:
                if average_max_price <= float(row[1]):
                    sell_signals.append(row)
                    print(row)
                    break
        
        print("results")
        print(results)
        
        self.data_extractor.updated_file=""
        print("lunghezza buy prices e contenuto")
        print(len(buy_prices))
        print(buy_prices)
        print(len(self.buy_results))
        print("lunghezza sell signals e contenuto")
        print(len(sell_signals))
        print(sell_signals)
        return sell_signals, results
                    
    """
    restituisce la lista di tuple con tutti i dati (timestamp, prezzo)
    successivi al timestamp dato (che sarebbe il timestamp di un buy signal) presi dal file di dati
    e la lista di tutte le righe del file dopo il timestamp dato, e il tutto entro il tempo massimo impostato
    dall'utente
    """
    def wait(self, buy_price, timestamp, file, time_distance):
        tuple_list = []
        rows=[]
        with open (file, "r") as f:
             csv_reader = csv.reader(f, delimiter=',')
             for row in csv_reader:
                 if len(row)==1:
                     row=row[0].split(",")
                 if int(row[0])>=timestamp:
                     break            
             for row in csv_reader:
                 if len(row)==1:
                     row=row[0].split(",")
                 rows.append(row)   #salva tutte le righe successive al timestamp del buy signal
                 if int(row[0])>=time_distance:                    
                     break
                 tupla = (int(row[0]), float(row[1]))
                
                 tuple_list.append(tupla)   #salva la tupla con timestamp e prezzo 
        return tuple_list, rows
            
    
    
    
    def compareBuyAndSell(self):
        self.signals=[]
        check=False
        for buy_signal in self.buy_results:
            if buy_signal["succeded"]:
                timestamp_buy = buy_signal["timestamp"]
                for sell_signal in self.sell_results:
                    if sell_signal["succeded"]:
                        timestamp_sell = sell_signal["timestamp"]
                        if timestamp_sell>=timestamp_buy:
                           self.completed_strategies.append((timestamp_buy, timestamp_sell))
                           self.signals.append(timestamp_sell)
                           check=True
                           break
            if check:
                check=False
            else:
                self.signals.append(0)
        self.data_extractor.signals=self.signals
        print("lunghezza1")
        print(len(self.buy_results))
        print("lunghezza2")
        print(len(self.signals))
        
    def saveResults(self):
        print("saving results, riga 80")
        with open(self.name+".json", "w") as f:
            json.dump(self.results, f)
 
        with open(self.name+"_buy_results.txt", "w") as f:
            for x in self.buy_results:
                f.write(str(x))       
            
        with open(self.name+"_sell_results.txt", "w") as f:
            for x in self.sell_results:
                f.write(str(x))      
            
        with open(self.name+"_compared.txt", "w") as f:
            for x in self.completed_strategies:
                f.write(str(x))
        print(self.lists_for_plot)
        return self.name+".json",self.name+"_compared.txt"
    
    
    
    def sumAndSignal(self):
        
        return
    
    
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
#        self.final_timestamp=0
        lists_for_plot=[]
#        print("chiamata strategia N."+str(count))
        for layer in self.layers:
            self.results["layer"+str(count_layer)] = []
            
            actual_timestamp = last_timestamp
            new_timestamp=0
            first_method = []
            check_if_true=False
            for method in layer:
#                print("la strategia N."+str(count)+" chiama un metodo, riga 111")
                validity, result, timestamp, list_for_plot = method.execute(actual_timestamp)
#                if int(timestamp)>int(self.final_timestamp):
#                    self.final_timestamp=timestamp
                lists_for_plot.append(list_for_plot)    
                if validity:
                    check_if_true=True
                first_method.append((int(timestamp), result))
#                print("il metodo chiamato dalla strategia N "+str(count)+" ha restituito:, riga 201")
#                print(validity, result, timestamp)
#                self.results["layer"+str(count)].append(result)
                new_timestamp = result["timestamp"]
                
                if int(new_timestamp)>int(last_timestamp) and validity:
                    last_timestamp=new_timestamp
#                    print("e' stato aggiornato il timestamp, riga 119")
                    
            if not check_if_true:
#                print("la strategia N "+str(count)+" ha ricevuto un valore finale negativo, torna false, riga 117")
                for x in first_method:                    
                    self.results["layer"+str(count_layer)].append(x[1])
                return False, self.results, last_timestamp, lists_for_plot
            
            first_method.sort(key=lambda x: x[0])
            
            for x in first_method:
                print(x[1])
                self.results["layer"+str(count_layer)].append(x[1])
            self.results["layer"+str(count_layer)].append({"last_timestamp":last_timestamp})
            count_layer+=1
#        last_timestamp = self.results[self.layers[-1].name][-1]["timestamp"]
#        print("la strategia N "+str(count)+" ha avuto successo, torna true, riga 127")
        return True, self.results, last_timestamp, lists_for_plot

    

class PriceCross():
    
    def __init__(self): #viene istanziato con due array di dati da due indicatori
        self.indicator1 = ""#indicator1  #istanza dell´indicatore
        self.indicator2 =""# indicator2
        self.ind1= ""#indicator1.values  #array dell´indicatore
        self.ind2= ""#indicator2.values 
        self.crossType =""# crossType   #"above" o "below" a seconda che si cerchi un cross che sale o che scende di ind1 su ind2
        self.TP=""#TP
#    def getData(self, timestamp):
#        
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.ind1= ""
        self.ind2= ""
        self.resultObject=""
        
    def execute(self, last_timestamp):      
        self.ind1=self.indicator1.getData(last_timestamp, self.TP)
#        self.ind1=self.indicator1.getOutput2()
        self.ind2=self.indicator2.getData(last_timestamp, self.TP)
#        self.ind2=self.indicator2.getOutput2()
        list_for_plot = [(self.indicator1.name,self.ind1), (self.indicator2.name,self.ind2)]
        i=1
        i_df=self.indicator1.df.index[0]
        diz={}
        while True:

            if i>=len(self.ind1)  or len(self.ind1)<=1 or i>=len(self.ind2) or len(self.ind2)<=1:
                print("ok no crossed")
                timestamp= int(self.indicator1.df.at[i_df+i-1, "timestamp"])
#                timestamp = self.indicator1.diz2["timestamp"][i-1]
                return False, {"result": "{} didn´t cross {}".format(self.indicator1.name, self.indicator2.name), 
#                               "timestamp": self.indicator1.diz2["timestamp"][i-1],
                               "timestamp": timestamp,
                               "ind1":self.indicator1.name, 
                               "ind2":self.indicator2.name,
                               "timeperiod":self.TP,
                               "method-name": "Price Cross"}, timestamp, list_for_plot
            
            if  not math.isnan(self.ind1[i-1]) and not math.isnan(self.ind1[i]) and not math.isnan(self.ind2[i-1]) and not math.isnan(self.ind2[i]) and self.ind1[i-1]-self.ind2[i-1] < 0 and self.ind1[i]-self.ind2[i] >= 0 and self.crossType=="above":
#                print("ok above")
                diz = {"ind1":self.indicator1.name, 
                       "ind2":self.indicator2.name, 
                       "timeperiod":self.TP,
                       "time-index":i, 
                       "method-name": "Price Cross", 
                       "result": "{} crossed above {}".format(self.indicator1.name, self.indicator2.name),
                     #  "date": self.indicator1.diz["date"].item(i),
                       "timestamp": int(self.indicator1.df.at[i_df+i, "timestamp"])}

                timestamp= int(self.indicator1.df.at[i_df+i, "timestamp"])

                return True, diz, timestamp, list_for_plot          #torna true se ind1 passa sopra a ind2
            
            if not math.isnan(self.ind1[i-1]) and not math.isnan(self.ind1[i]) and not math.isnan(self.ind2[i-1]) and not math.isnan(self.ind2[i]) and self.ind1[i-1]-self.ind2[i-1] > 0 and self.ind1[i]-self.ind2[i] <= 0 and self.crossType=="below":
#                print("ok below")
                diz = {"ind1":self.indicator1.name, 
                       "ind2":self.indicator2.name,
                       "timeperiod":self.TP,
                       "time-index":i, 
                       "method-name": "Price Cross", 
                       "result": "{} crossed below {}".format(self.indicator1.name, self.indicator2.name),
                     #  "date": self.indicator1.diz["date"].item(i),
#                       "timestamp": self.indicator1.diz2["timestamp"][i]
                        "timestamp": int(self.indicator1.df.at[i_df+i, "timestamp"])}   
                timestamp= int(self.indicator1.df.at[i_df+i, "timestamp"])
                return True, diz, timestamp, list_for_plot       #torna false se ind1 passa sotto a ind2 (ovvero ind2 passa sopra a ind1)
            i+=1
            
        

class SMAClass:
    def __init__(self, data_extractor):
        
        self.timeperiod = 30
        self.data_extractor = data_extractor
        self.values = np.zeros(1)
        self.name = "SMA"#+str(timeperiod)
#        self.data_list = data_extractor.data
        self.value_type="close"
       # self.diz= self.setDataList()
#        self.diz2= {}
#        self.array=[]
        self.df=""
        self.resultObject=""

    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.values = np.zeros(1)
        self.df=""
        
        
    def getData(self, timestamp, TP):
#        self.timeperiod=TP
        TP=int(TP)

#        filename=self.data_extractor.file
        self.data_extractor.createTPFromRawFile(TP)
        c = CandleExtractor("TP"+str(TP)+"_from_dictionary.csv")
#        c = CandleExtractor("TP"+str(TP)+".json")
        self.df, timestamp=c.creaDiz( TP, timestamp)

        self.values = tl.SMA(self.df[self.value_type].astype(float).values, timeperiod=self.timeperiod)
        
        if self.resultObject=="":
            self.df["date"]=pd.to_datetime(self.df["timestamp"], unit="s")
            self.resultObject=ResultsToPlot()
            self.resultObject.x = self.df["date"]
            self.resultObject.y = self.values
            self.resultObject.name=self.name
            self.data_extractor.result_objects.append(self.resultObject)
        return self.values.tolist()


"""
estrae i dati dal file csv come dataframe, converte i timestamp in interi
restituisce con creaDiz (nome rimasto dal vecchio metodo che restituiva un dizionario)
il dataframe dei valori successivi al timestamp dato
"""
class CandleExtractor:
    def __init__(self, filename):
        self.filename=filename
        
    def creaDiz(self, TP, timestamp):       
        df = pd.read_csv("TP"+str(TP)+"_from_dictionary.csv")
        df['timestamp'] = df['timestamp'].astype(int)  
       # mask = df['timestamp'].values > timestamp
        df = df[df["timestamp"]>timestamp]
        return df, timestamp #df[mask]

        
        
        
class DataExtractor:
    def __init__(self, file, ts_start=0, ts_end=0, filename="new_file.csv"):
        self.file=file
#        self.data= ""#self.extractData()
        self.TP_files = {}
        self.TP_files_csv = {}
#        self.updated_file = ""
#        self.timestamp = "0"
#        self.file_opened=False
        self.ts_start=float(ts_start)
        self.ts_end=float(ts_end)
#        self.setFile()
        self.filename=filename
        self.indicators_results=[]  # = engine.list_for_plot
        self.createdFiles=[]    #contiene i nomi del file csv già creati
        self.signals=[]
        self.result_objects=[]
    
    
    def setFile(self):
        print("lanciato il setFile")
        if self.ts_end==0:
            return

        try:
#            df=pd.read_csv(self.file,sep=",", header=None)
#            print(df)
#    #        df['timestamp'] = df['timestamp'].astype(int)  
#            df=df[[0]>self.ts_start]
            
            with open(self.file, "r") as f:
                line=f.readline()#.strip()
                ts=line.split(",")[0]
                ts=float(ts.replace("\"", ""))
                while ts<self.ts_start:
                    line=f.readline()#.strip()
                    ts=line.split(",")[0]
                    ts=float(ts.replace("\"", ""))
                print("trovato inizio")
                
                with open(self.filename, "w") as nf:
                    while ts<self.ts_end-1:
                        nf.write(line.replace("\\n", ""))
                        line=f.readline()
                        ts=line.split(",")[0]
                        ts=float(ts.replace("\"", ""))
                    print("creato "+self.filename)      
            self.file=self.filename
            return True
        
        except:
            traceback.print_exc()
            print("errore nella creazione del file")
            return False
        
       

    def createTPFromRawFile(self, tpValue):   #questo dovrà essere poi il self.file, così si usa sempre lo stesso timelapse
        print("chiamato createTPFfromRawFile")
        if not "TP"+str(tpValue) in self.TP_files:# or int(timestamp)>=int(self.timestamp):
#            self.timestamp=timestamp
            
            json_content={}
            csv_content = [["timestamp","date","open","close","high","low","volume","average","direction"]]
#            print("apertura del file principale, nome file: , riga 439") 
#            print(file)
            
            with open(self.file) as f:
                candle_data = []      
                first_line=f.readline()
#                first_line=first_line.replace("\"\n","")
                data = first_line.split(",")
#                print(data)
                last_timestamp = data[0].replace("\"", "")
                
#                date = datetime.fromtimestamp(int(last_timestamp))
                candle_data.append({"timestamp":last_timestamp, "price":data[1], "amount":data[2]})
#                print(candle_data)
                json_content["TP"+str(tpValue)] = []    
                
                for line in f:
#                    line=line.replace("\"","")
#                    line=line.replace("\\n","")
#                    print(line)
                    data = line.replace("\"", "").split(",")
#                    data = data[0]
                    actual_timestamp=data[0]
                    actual_tp = (int(actual_timestamp) - int(last_timestamp))/60 #number of minutes
                    checkTP = actual_tp / tpValue
                    
                    if checkTP>=1:   #se é il momento di creare una candela
                        last_timestamp=actual_timestamp  #aggiorna il timestamp al punto attuale                   
                        candlestick, candlestick_csv = self.createCandlestick(candle_data)  #chiama il metodo che crea la candela
                        json_content["TP"+str(tpValue)].append(candlestick)
                        csv_content.append(candlestick_csv)
                        candle_data.clear()
    
                    candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
#            print("il file principale è stato trasformato in candele, riga 587")
            with open("TP"+str(tpValue)+".json", 'w', encoding='utf-8') as json_file:
                json.dump(json_content, json_file, ensure_ascii=False, indent=4)              #salva il file
                print("le candele sono state scritte in un nuovo file, riga 589")
#                print("TP"+str(tpValue)+".json")
            self.TP_files["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"
            
            with open("TP"+str(tpValue)+".csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(csv_content)            
            
            self.TP_files_csv["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"

            with open("TP"+str(tpValue)+"_from_dictionary.csv", "w", newline='') as csv_file:
                fields = ["timestamp","date","open","close","high","low","volume","average","direction"]
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(json_content["TP"+str(tpValue)])
                self.createdFiles.append("TP"+str(tpValue)+"_from_dictionary.csv")
        return self.TP_files["TP"+str(tpValue)]

    
    def createFile(self, file, tpValue):   #questo dovrà essere poi il self.file, così si usa sempre lo stesso timelapse
        print("chiamato createFile")
#        if not "TP"+str(tpValue) in self.TP_files:# or timestamp!=self.timestamp:
#            self.timestamp=timestamp
        json_content={}
        candles=[]
        csv_content = [["timestamp","date","open","close","high","low","volume","average","direction"]]
        print("apertura del file principale, nome file: , riga 477") 
        print(file)
        with open(file, "r") as f:
            candle_data = []          
            first_line = f.readline()
            if first_line[0].replace("\"", "")!="1":
                first_line = f.readline()
            print("first line, riga 516")
            print(first_line)
            data = first_line.replace("\"", "")
            data = data.replace("\\n", "")
            data = data.split(",")
            last_timestamp = data[0] 
            last_timestamp = last_timestamp.replace("\"" , "")
            print(last_timestamp)
#                date = datetime.fromtimestamp(int(last_timestamp))
            candle_data.append({"timestamp":last_timestamp, "price":data[1], "amount":data[2]})
            json_content["TP"+str(tpValue)] = []    
            
            for line in f:
                line = line.replace("\"", "")
                line = line.replace("\\n", "")
                data = line.split(",")
                actual_timestamp = data[0]
                actual_tp = (float(actual_timestamp) - float(last_timestamp))/60 #number of minutes
                checkTP = actual_tp / tpValue
                
                if checkTP>=1:   #se é il momento di creare una candela
                    last_timestamp = actual_timestamp  #aggiorna il timestamp al punto attuale                   
                    candlestick, candlestick_csv = self.createCandlestick(candle_data)  #chiama il metodo che crea la candela
                    json_content["TP"+str(tpValue)].append(candlestick)
                    candles.append(candlestick)
                    csv_content.append(candlestick_csv)
                    candle_data.clear()

                candle_data.append({"timestamp":data[0], "price":data[1], "amount":data[2]})
        print("il file principale è stato trasformato in candele, riga 415")
        

        with open("TP"+str(tpValue)+"_GRAPH.json", 'w', encoding='utf-8') as json_file:
            json.dump(json_content, json_file, ensure_ascii=False, indent=4)              #salva il file
            print("le candele sono stata scritte in un nuovo file, riga 418")
            print("TP"+str(tpValue)+".json")
#        self.TP_files["TP"+str(tpValue)] = "TP"+str(tpValue)+".json"
        
        with open("TP"+str(tpValue)+"_from_dictionary_GRAPH.csv", "w", newline='') as csv_file:
            fields = ["timestamp","date","open","close","high","low","volume","average","direction"]
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(json_content["TP"+str(tpValue)])
        csv_name="TP"+str(tpValue)+"_from_dictionary_GRAPH.csv"
        with open("TP"+str(tpValue)+"_GRAPH.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(json_content["TP"+str(tpValue)])
                          
        return candles, csv_name
    
    
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
            amount = float(trade["amount"].strip().replace("\"", ""))
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
        candlestick["open"] = float(openprice)
        candlestick["close"] = float(close)
        candlestick["high"] = float(high)
        candlestick["low"] = float(low)
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
        
#    def extraxtAllDataInJson(self, filename):
#        with open(filename, "w") as f:
#            for x in self.data:
#                json.dump(x, f) 

                
                
def drawResults(file, operation):
    diz = {}
    with open(file) as f:
        diz = json.load(f)
    n=1   
    strategy = operation+"_strategy" + str(n)
    draw_array = []
    
    while strategy in diz:     
        draw_array.append(int(diz[strategy]["timestamp"]))  
        n+=1        
        strategy = operation+"_strategy"+str(n)
      
    print(draw_array)
  
    np_array = np.array(draw_array)
    plt.plot(np_array)
    plt.savefig(operation+".png", dpi = 300)
    plt.show()
    

class Drawer:
    def __init__(self, data_extractor):
        self.data_extractor = data_extractor
#        self.candleFile=""
    
    def drawCandles(self, TP):
#        if "TP"+str(TP) in self.data_extractor.TP_files:
            
        filename = self.data_extractor.file
        _, csv_name=self.data_extractor.createFile(filename, TP)
        df = pd.read_csv(csv_name)
        print(df["date"])
        # Converting date to pandas datetime format
        df['date'] = pd.to_datetime(df['date'])
        df["date"] = df["date"].apply(mdates.date2num)

        # Creating required data in new DataFrame OHLC
        ohlc= df[['date', 'open', 'high', 'low','close']].copy()    
        f1, ax = plt.subplots(figsize = (10,5))
        # plot the candlesticks
        candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # Saving image
        plt.savefig('OHLC HDFC.png')

        plt.show()  
        
    def drawGraph(self, TP):
        filename = self.data_extractor.file
        candles,_=self.data_extractor.createFile(filename, TP)
        panda_array = pd.DataFrame(candles)
#        pd.to_datetime(panda_array['date'])
        plt.plot(panda_array['close'])
        plt.show()

    def drawStrategy(self, start, end):
#        filename = self.data_extractor.file
#        candles,_=self.data_extractor.createFile(filename, 240)
#        panda_array = pd.DataFrame(candles)
##        pd.to_datetime(panda_array['date'])
#        plt.plot(panda_array['close'])
#        x_list=range(int(start), int(end))
        colors=["b", "r", "g", "c", "y", "m", "k"]
        count=1
        labels=[]
        lab=[]
        fig, ax1 = plt.subplots()
        data=""
        try:
            with open("saved_trendspot.txt", "r") as f:
                data=f.read()
                data=data.split(",")
                data.reverse()
            li = np.array(data)
            print("dimensioni array trenspot:  , engine.837")
            print(len(li))
        except:
            pass
        print(self.data_extractor.indicators_results)
        for x in self.data_extractor.indicators_results:
            if x[0][0][0]!="TrendSpot":
                print(x)
                for y in x:
                    for z in y:
                        color=colors[(count-1)%7]                    
                        if count==1:                        
                            a,=ax1.plot(range(len(z[1])), z[1], color, label=z[0]) #abbiamo z[0] e z[1] perchè è una tupla (nome indicatore, risultati dell´indicatore)
                            ax1.tick_params(axis='x', labelcolor=color)
                            count+=1
                            labels.append(a)
                            lab.append(z[0])
                        else:
                            ax2=ax1.twiny()                       
                            lab.append(z[0])
                            print("test")
                            l=range(len(z[1]))
                            a,=ax2.plot(l,z[1], color, label=z[0])
                            labels.append(a)
                            ax2.tick_params(axis='x', labelcolor=color)
                        count+=1
        if data!="":
            ax2 = ax1.twiny()
            lab.append("trend")
            a,=ax2.plot(range(len(li)),li,colors[(count-1)%7], label="trendSpot")
            labels.append(a)
            plt.plot([100], [300], marker='o', markersize=5, color="red")
        plt.legend(labels, lab)
        fig.tight_layout()
        plt.show()
        
class ResultsToPlot:
    def __init__(self):
        self.name=""
        self.x=[]
        self.y=[]
        self.print_just_points=False
        
    def plot(self):
        if self.print_just_points:
            plt.plot(self.x, self.y, "ro")  
            print(self.x, self.y)
        else:
            plt.plot(self.x, self.y)
        
##        TP=240
#        self.timeperiod=20
#        timestamp=0
#        self.value_type="close"
##        c = CandleExtractor("TP"+str(TP)+"_from_dictionary.csv")
##        c = CandleExtractor("TP"+str(TP)+".json")
#
#        self.df, timestamp=self.creaDiz( TP, timestamp)
#    def do(self):
#        self.values = tl.SMA(self.df[self.value_type].astype(float).values, timeperiod=self.timeperiod)
#        
#        self.df["date"]=pd.to_datetime(self.df["timestamp"], unit="s")
##        self.resultObject=ResultsToPlot()
#        self.x = self.df["date"]
#        self.y = self.values
#        print(self.x)
#        print(len(self.values))
#        return self.x, self.y
#        
#    def creaDiz(self, TP, timestamp):       
#        df = pd.read_csv("TP"+str(TP)+"_from_dictionary.csv")
#        df['timestamp'] = df['timestamp'].astype(int)  
#        mask = df['timestamp'].values > timestamp
#
#        return df[mask], timestamp 

#if __name__ == "__main__":
#    
#    ax, ay = ResultsToPlot(240).do()
#    bx, by = ResultsToPlot(120).do()
#    plt.plot(ax,ay)
#    plt.plot(bx, by)
#    plt.show()
    
#
##crea il data_extractor
#
#data_extractor = DataExtractor("test.csv")
#
##crea strategie
#
#sma = SMAClass(data_extractor, 30)
#sma.value_type="low"
#
#sma2 = SMAClass(data_extractor, 20)
#sma2.value_type="low"
#
#sma3 = SMAClass(data_extractor, 100)
#sma3.value_type="low"
#
#sma4 = SMAClass(data_extractor, 50)
#sma4.value_type="low" 
#
#met1 = PriceCross(sma, sma2, "above", 100)
#met2 = PriceCross(sma2, sma3, "above", 50)
#met3 = PriceCross(sma3, sma4, "above", 100)
#
#layer1 = {met1, met2}
#layer2 = {met3}
#
#strategy = Strategy([layer1,layer2])
#
#
#
#
##    data_extractor = DataExtractor("test.csv")
##
###crea strategie
##
#sma = SMAClass(data_extractor, 30)
#sma.value_type="low"
#sma.timeperiod=30
#
#sma2 = SMAClass(data_extractor, 20)
#sma2.value_type="low"
#sma2.timeperiod=20
##    
##    sma3 = SMAClass(data_extractor, 100)
##    sma3.value_type="low"
##    sma3.timeperiod=100
##    
##    sma4 = SMAClass(data_extractor, 50)
##    sma4.value_type="low"
##    sma4.timeperiod=50 
##    met4 = PriceCross(sma, sma2, "below", 20)
##    met5 = PriceCross(sma2, sma3, "above", 50)
##    met6 = PriceCross(sma3, sma4, "below", 30)
##    
##    layer3 = {met4, met5}
##    layer4 = {met6}
##    
##    strategy2 = Strategy([layer3,layer4])
#
##    engine = Engine("motore1", data_extractor)
##    
##    lista = engine.buyAndWait(strategy, 9432000)
#  
##    engine.findBuySignal(strategy)
##    print(engine.results)
##    nome_file = engine.saveResults()
#
##    
##    lista = engine.findSellSignal(strategy2)
##    print(lista)
##    print(engine.results)
##    nome_file = engine.saveResults()
##    drawResults("motore1.json", "buy")
##    drawResults("motore1.json", "sell")
##    data_extractor.createFile("test3.csv", 1440)
##    
##    
##    engine.compareBuyAndSell()
##    print("ùùùùùùùùùùùùùùùùùùùùùùùùùùù")
##    print(engine.completed_strategies)
##    print("BUY")
##    print(engine.buy_results)
##    print("SELL")
##    print(engine.sell_results)
##    print("ùùùùùùùùùùùùùùùùùùùùùùùùùùù")
##
##    
#volume2=VolumeExtractor(data_extractor, 1440,20)
#volume2.getData()
#volume2.createGroups()
#lista, lista_time=volume2.convertToNP()
#volume2.printGraph(lista)
#print(len(volume2.volume_blocks))
