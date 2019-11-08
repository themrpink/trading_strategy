# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 23:03:01 2019

@author: themr
"""
import pandas as pd
class User:
    
    def __init__(self):
        self.name = ""
        self.saldo = 0
        self.operations = []
        self.risultati=[]
        self.ricavi=[]
        self.win = []
        self.lose = []
        self.safe__percent_limit=0   #in percentuale
        self.safe_amount_limit=0     #valore preciso
        self.valuta="euro"
        self.investimento=0
        self.commissioni=0
        self.dati_result=[]    
        
        
    def calcola(self, dati, file):
        indice_buy=0
        indice_sell=0
        dati.sort(key=lambda x:(x[0], x[1]))
        print(dati)
        for x in dati:
            self.dati_result.append([])
            
            ##############################################
#        df_csv = pd.read_csv(file, names=['timeframe', 'price', 'volume'], header=1)
        #####################################################
        with open(file, "r") as f:
            
        
            for line in f:
                data=line.replace("\"", "")
                data=data.replace("\\n", "")
                data=data.split(",")
                time=int(data[0])
                price=data[1]
                if indice_buy<len(dati) and time==int(dati[indice_buy][0]):
                    print("ok")
                    self.dati_result[indice_buy].insert(0, (time,price))
                    indice_buy+=1
                    
                if indice_sell<len(dati) and time==int(dati[indice_sell][1]):
                    self.dati_result[indice_sell].append((time, price))                    
                    i=0
                    for j,sell in enumerate(dati[indice_sell+1:]):
                        if int(sell[1])==self.dati_result[indice_sell][1][0]:
                            self.dati_result[indice_sell+1+j].append(self.dati_result[indice_sell][1])
                            i+=1
                    indice_sell+=i+1                
#                    if i==0:
#                        indice_sell+=1
                        
        with open("saved_result.txt","w") as f:
            for line in self.dati_result:
                f.write(str(line))
        

    def calcolaInvestimento(self):       
        for x in self.dati_result:
            self.investimento=int(self.investimento)
            if int(self.investimento)>0:
                prezzo_buy=x[0][1]
                quantita=float(self.investimento)/float(prezzo_buy)
                prezzo_sell=x[1][1]
                saldo_operazione=quantita*float(prezzo_sell)
                ricavo=saldo_operazione-float(self.investimento)
                self.investimento+=ricavo
                self.operations.append(saldo_operazione)
                self.ricavi.append(ricavo)
        return self.operations