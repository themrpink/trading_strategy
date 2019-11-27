# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:50:32 2019

@author: themr
"""
import engine 


"""
motore specifico per la strategia "sum and buy"
in pratica prende un oggetto indicatore che ha delle sue proprietà e criteri che stabiliscono quando lanciare un segnale di buy
a quel punto ogni buy lui parte alla ricerca di un sell, sia se si raggiunge il prezzo target sia se si scende sotto una soglia,
che è data dal prezzo di acquisto +- una percentuale di tolleranza specifica di ogni indicatore.
Se raggiunge il target ottiene un +1, se vende allo stop loss ottiene un -1
lui somma tutti questi valori per vedere se per un intero TP l'indicatore con quei target e stop loss dati fornisce dei risultati
positivi (cioè richiesti) nella maggior parte dei casi oppure no
"""
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
        #il target price lo calcola incluse le commissioni
        price_target= self.price + self.price*self.required_return + (self.price*self.fees)
        self.price_target+= price_target*self.fees
        
    def exitePriceTollerance(self, percentage):
        self.stop_tolerance=1-percentage
        
    """
    cerca per tutti i TP  passati come argomento, per un indicatore dato, che questo si verifichi, che dopo il segnale di buy si
    verifichi un sell e salva il punteggio e tutti i dettagli delle informazioni
    
    i dati sono restituiti come:
        
        {dizionario[indicatore+TP] : (sum_results, [lista_risultati_operazioni]), dizionario[indicatore+TP]: ecc ecc}
        
        quindi per ogni TP abbiamo una tupla, che contiene la somma dei risultati dell´indicatore per quel TP
        e una lista di dizionari, uno per ogni operazione di buy and sell effettuata in quel TP, con i seguenti dati:
            lista_risultati_operazioni = [..., {sum_value(+-1), buy_price, sell_target, buy_timestamp, sell_price, sell_timestamp, indicator_name}, ...]
    """
    def search(self, indicator, TP_list=None):
        if TP_list==None:
            TP_list=self.mainTPs            
        diz_results={}       
        self.indicator=indicator 
        sum_results=0         
        lista_risultati_operazioni=[]
        for TP in TP_list:
            name = indicator.name+str(TP)           
            filename=self.data_extractor.createTPFromRawFile(TP)
            candle_extractor = engine.CandleExtractor(filename)
            data, = candle_extractor.creaDiz(TP, self.timestamp)          
            for i in range(len(data)):
                row=data.iloc[i]
                if self.indicator.foundSignal(row):
                    self.price = row["price"]
                    timestamp_buy = row["timestamp"]
                    data_for_result = data[data["timestamp"]>row["timestamp"]]  #prendere il data_for_result però dalla data del row attuale in poi                  
                    sum_result, timestamp_sell, price_sell = self.itHappened(data_for_result, indicator)
                    sum_results+=sum_result
                    diz = {"sum":sum_result, 
                           "buy price":self.price, 
                           "sell target":self.price_target, 
                           "buy timestamp": timestamp_buy, 
                           "sell price": price_sell, 
                           "sell timestamp": timestamp_sell,
                           "indicator": self.indicator.name}
                    lista_risultati_operazioni.append(diz)
                    break
            diz_results[name]= (sum_results, lista_risultati_operazioni)
            sum_results=0
            lista_risultati_operazioni=[]
        return diz_results

        
    def itHappened(self, data):       
        for i in range(len(data)): 
            row=data.iloc[i]
            if self.indicator.fails(row, self.price):
                return -1, row["timestamp"], row["price"]
            if self.indicator.succeeds(row, self.price_target):
                return 1, row["timestamp"], row["price"]
        return -1, row["timestamp"], row["price"]
            
            
            
        #se dal punto in cui ci troviamo, il prezzo raggiunge in target richiesto prima che il prezzo
        #sia sceso al di sotto del prezzo iniziale, considera l´operazione riuscita
        #torna +1
        #altrimenti -1
        
        