# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:27:30 2020

@author: themr
"""

import ccxt

kraken = ccxt.kraken()

ticker_data = []

# fetch the BTC/USDT ticker for use in converting assets to price in USDT
bitcoin_ticker = kraken.fetch_ticker('BTC/EUR')

# calculate the ticker price of BTC in terms of USDT by taking the midpoint of the best bid and ask
bitcoinPriceUSDT =  float(bitcoin_ticker['bid'])

# fetch the tickers for each asset on HitBTC
# this will take as long as 5 minutes
for trading_pair in kraken.load_markets():
    base = trading_pair.split('/')[0]
    quote = trading_pair.split('/')[1]
    if quote == 'XBT':
        pair_ticker = kraken.fetch_ticker(trading_pair)
        pair_ticker['base'] = base
        ticker_data.append(pair_ticker)

prices = []

# create the price tickers for each asset, removing unnecessary data
for ticker in ticker_data:
    price = {}
    price['symbol'] = ticker['base']
    price['price'] = ((float(ticker['info']['ask']) + float(ticker['info']['bid'])) / 2) * bitcoinPriceUSDT
    prices.append(price)
print(price)
# additional processing is required for assets without BTC pairs
# additional pr