# trading_strategy

Program to develop and backtest trading strategies from transactions data.

The user can choose between various indicators, developed from scratch or implemented from the lib TA-lib.
Each indicator has various ways to interact with the other. Each interaction between indicators produces sell or buy signals.
Each indicator operates on personalized timeframes.

It makes possible to test various layers of personalized indicators interactions, each with its own priorities.
A set of layers of interactions between indicators is a strategy. A strategy can be evaluated following various approaches:
"buy and sell", "buy and wait", etc, each developing its own behaviour in relation to the various buy and sell signals produced bay the indicators.

It also implements an user portfolio.

how to use:
lauch interfaccia_buy_and_sell.py.
Then:
  open a csv file with transactions data;
  chose a time period;
  create the data;
  create indicators and layers, both for the buy and the sell signals;
  launch the strategy.

The code is still unstable. 
Visual interface implemented with PyQt-lib.

Next steps:
- reorganize dthe code and write the documentation
- implement a better use of Pandas to import files content.
- add new indicators
- find and list the bugs
- start adding machine learning approach to optimize the portfolio management
- develop a maching learning approach to optimize the strategies
