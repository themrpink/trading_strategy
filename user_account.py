# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 23:03:01 2019

@author: themr
"""

class User:
    
    def __init__(self):
        self.name = ""
        self.saldo = 0
        self.operations = []
        self.win = []
        self.lose = []
        self.safe__percent_limit=0   #in percentuale
        self.safe_amount_limit=0     #valore preciso
        self.valuta="euro"
        self.investimento=0
        self.commissioni=0
        
        
    def calcola(self, dati, file):
        indice_buy=0
        indice_sell=0
        dati.sort(key=lambda x:(x[0], x[1]))
        print(dati)
        self.dati_result=[]
        for x in dati:
            self.dati_result.append([])
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
            prezzo_buy=x[0][1]
            quantita=self.investimento/prezzo_buy
            prezzo_sell=x[1][1]
            ricavo=quantita*prezzo_sell
            saldo_operazione=ricavo-self.investimento
            self.operations.append(saldo_operazione)
            return self.operations