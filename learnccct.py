# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:35:42 2020

@author: themr
"""

import ccxt

#print(ccxt.exchanges) 
"""
#questa intanto è una lista di exchange da usare. Potrebbe esserci
un primo loop, su tutti gli exchange, vedere il prezzo del bitoin/eth, per esempio
e capire anche come reagisce se non è disponibile e in caso come gestire
gli errori. Poi tutto questo andrebbe gestito in parallelo su
più macchine che interrogano contemporaneamente più macchine.

potrei anche scrivere un tale servizio in c per poi usarlo in python?
secondo me sì.

"""
print("")



def getPairs_from_exchange(exchange):
    curr_list = []
    markets=exchange.load_markets()
    for i in markets:
        if i.find("/")>=0:
            curr_list.append((i.split("/")[0],i.split("/")[1]))    
    return curr_list

def getPairs_from_market(markets):
    curr_list = []
    for i in markets:
        if i.find("/")>=0:
            curr_list.append((i.split("/")[0],i.split("/")[1]))    
    return curr_list

def sort_currencies_pairs_by_left(curr_list, curr):
    curr_list.sort(key=lambda tup: tup[0]) 
    return curr_list

def sort_currencies_pairs_by_right(curr_list, curr):
    curr_list.sort(key=lambda tup: tup[1]) 
    return curr_list
exchange = ccxt.okcoin () # default id
okcoin1 = ccxt.okcoin({ 'id': 'okcoin1' })
okcoin2 = ccxt.okcoin ({ 'id': 'okcoin2' })

id = 'btcchina'
#btcchina = eval ('ccxt.%s ()' % id)
coinbasepro = getattr (ccxt, 'coinbasepro')
# print(type(coinbasepro()))
c_describe=coinbasepro().describe()


k = ccxt.kraken()
k_describe =k.describe()

curr_list  = []
k_markets=k.load_markets()
for i in k_markets:
    if i.find("/")>=0:
        curr_list .append((i.split("/")[0],i.split("/")[1]))
print(curr_list )
l=sort_currencies_pairs_by_right(curr_list, "USD")
print("")
print(l)
print("")
#(k.markets['BTC/USD'] )
print(k.fetch_ticker('BTC/USD')["info"])
# from variable id
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
print(type(exchange_class()))
exchange = exchange_class({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'timeout': 30000,
    'enableRateLimit': True,
})
