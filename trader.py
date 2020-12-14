# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 21:30:23 2020

@author: themr
"""
import queue
import pandas as pd
import matplotlib.pyplot as plt
import sys, time, threading
"""
cosa deve fare questo trend:
    controlla l´andamento giornaliero dei prezzi, negli ultimi dieci giorni
    puó controllare il prezzo, i guadagni rispetto al precedente, se quindi siamo in perdita
    o in crescita di media
    io passo un prezzo e un timestamp (il timestamp posso fare il check prima, ma conviene 
                                       farlo qua centralizzato a ogni timestamp)
    quindi prendo un timestamp, e controllo se rispetto all ultimo accettato sono
    
    """
#monitora il prezzo
class Trend:
        def __init__(self, first_day=0, first_price=0):
            #al momento della creazione del trend si ha un primo timestamp e un primo prezzo
            self.daily_gains=[]        #contains the daily gains related to the previous day
            self.days.append(0)
            self.last_day=first_day
            self.last_timestamp=first_day
            self.time_range_h=24  #in hours
            self.time_range_ms=self.time_range_h*3600  #in milliseconds
            self.actual_trend=0
            self.days_considered=10
            self.last_price=first_price
            
        def check_time_ms(self, timestamp):
            if timestamp-self.last_timestamp <= self.time_range_ms:
                self.last_timestamp=timestamp    
                return True
            return False
        
        
        def add_day(self, price):
            gain=price-self.last_price
            self.last_price=price
            if len(self.daily_gains)==self.days_considered:
                self.daily_gains.pop(0)
            self.daily_gains.append(gain)
    
        def check_trend():
            tot=0
            for gain in self.daily_gains:
                tot+=gain
                
            if tot>0:
                return True
            else:
                return False
                
        
                
        
            
            
class Portfolio:
    def __init__(self, capital=1000, risk=0.02):
        self.capital=capital
        self.risk=risk
        self.trade_amount=self.capital*self.risk
        self.available_capital=1000
    def update_capital(self, amount):
        self.capital+=amount
        self.trade_amount=self.capital*self.risk
        
        
"""those values are important to set"""
class Trade:
    def __init__(self, row, portfolio, target=5, stop=3, fee=0.26, filename="result.csv"):
        self.time, self.price = row
        self.target=target
        self.stop=stop
        self.fee=fee
        self.target_price=self.price*(1+(target/100))
        self.stop_price=self.price-(self.price*(stop/100))
        self.filename=filename
        self.portfolio=portfolio
        self.volume=portfolio.trade_amount/self.price
        
    
    def print_all(self):
        print("time: {}".format(self.time))
        print("price: {}".format(self.price))
        print("target price:  {}".format(self.target_price))
        print("stop price: {}".format(self.stop_price))

    def check(self, row):
        price=float(row[1])
        time=int(row[0])
        
        if self.portfolio.capital<=10:
            return -2
        """
        what should I do: 
            i have to save into the trades record file all the relevant data about the closed
            trade. That is: time of buy, price of buy, volume bought, target, time of sell,
            price of sell, volume sold.
            Where do I get this info from and how do I structure it?
            I parse it into a string. Half of the values I have available fron the header
            of the class. The price and time I have gratis from the arguments. The volume I can 
            easily calculate, than join all in a string
            
            then i must upgrade the portfolio, because I need to know if I finish money.
            that`s also an option I have to check and communicate to the main processes and 
            write to the log file.
        """

        
        if price>=self.target_price or price<=self.stop_price:
            

            #value at sold price ((sell value))
            amount=self.volume*price
            #volume sold
            sold_volume=amount/price
            #buy value - sell value
            gain=price*self.volume - self.price*self.volume
            
            list_to_join=[str(self.time),
                          str(self.price), 
                          str(self.volume), 
                          str(self.portfolio.trade_amount),
                          str(self.target),         
                          str(time), 
                          str(price), 
                          str(sold_volume),
                          str(amount),
                          str(gain)]  

            string_to_save=",".join(list_to_join)    
            
            #save to file
            with open(self.filename, "a") as f:
                f.write(string_to_save+"\n")     
            f.close()
            
            #update the portfolio
            self.portfolio.update_capital(gain)
            if gain>0:
                return 1
            elif gain <=0:
                return 0
        
        else:
            return -1

            
    def stop(self):
        with open("logfile.txt", "a") as f:
            f.write("reached end of file before trade close\n")     
        f.close()
 
portfolio = Portfolio()

def main(filename="nov2017_oggi_5min.csv", csvmode="OHLCVT"):
    
   # portfolio=Portfolio()
   # filename="test.csv"
    open("result.csv", 'w').close()
    open("logfile.txt", 'w').close()
    
    one_hour=3600 #millisenconds
    
    """this is important to set"""
    hours=1
    interval=one_hour*hours
    
    #OHLCVT (Open, High, Low, Close, Volume, Trades) 
    #TPV=Time Price Volume
    price_column=""
    if csvmode=="TPV":
        trade_file=pd.read_csv(filename, sep=",", header=1, names=["timestamp", "price", "volume"])
        price_column="price"
    elif csvmode=="OHLCVT":
        trade_file=pd.read_csv(filename, sep=",", header=1, names=["timestamp", "open", "high", "low", "close", "volume", "trades"])
        price_column="open"
    else:
        print("{}: unknown data format".format(csvmode))
        return False
    

    trade_file.plot(x="timestamp", y=price_column)
    plt.savefig("price_chart.pdf")
    temp_timeframe=0
    trades_list= []
    print("searching for trades...")
    trend=True #if False = neagativa, True = positive
    for index, row in trade_file.iterrows():
        timestamp=row['timestamp']
        row=(row['timestamp'],row[price_column])
        trades_copy=trades_list.copy() 
        
        for trade in trades_list:
            check=trade.check(row)
            if check==-2:
                with open("logfile.txt", "a") as f:
                    f.write("not enough capital left in portfolio (<10)\n")
                f.close()
                print("closing because of capital extinction")
                return False
            
            elif check==-1:
                continue
            
            else:
                trades_copy.remove(trade)
                if check==0:
                    interval=int(interval*2)
                elif check==1:
                    interval=int(interval/2)
        trades_list=trades_copy.copy()
        
        if timestamp>=temp_timeframe+interval:
            #print("added trade")
            new_trade=Trade(row, portfolio)
            trades_list.append(new_trade)
            temp_timeframe=timestamp
        
           
    # if len(trades_list)>0:
    #     for trade in trades_list:
    #         trade.stop()
    
    return True
            
            
    
    
def final_balance():
    result=pd.read_csv("result.csv", names=["timestamp buy", 
                                       "price buy",
                                       "volume buy",
                                       "amount buy"
                                       "target ",
                                       "time sell",
                                       "price sell",
                                       "volume sell",
                                       "amount sell",
                                       "gain"])
    
    
    positive_gain_number=result.query("gain >= 0")['gain'].count()
    positive_gain_value=result.query("gain >= 0")['gain'].sum()
    print("positive_gain_number: {}".format(positive_gain_number))
    print("positive_gain_value: {}".format(positive_gain_value))
    print()
    negative_gain_number=result.query("gain < 0")['gain'].count()
    negative_gain_value=result.query("gain < 0")['gain'].sum()
    print("negative_gain_number: {}".format(negative_gain_number))
    print("negative_gain_value: {}".format(negative_gain_value))
    print()
    #print(result.head(n=5))
    gains=result["gain"]
    final=gains.sum(skipna=True)
    print("result final gain is: {}".format(final))
    print("portfolio end capital: {}".format(portfolio.capital))
    result.plot(x="time sell", y="gain", kind="scatter")
    plt.savefig("gains_chart.pdf")
    
    
    
def animated_loading():
    chars = "/—\|" 
    for char in chars:
        sys.stdout.write('\r'+'loading...'+char)
        time.sleep(.1)
        sys.stdout.flush() 
        
mainfilename="nov2017_oggi_5min.csv"
csvmode="OHLCVT"
      
the_process = threading.Thread(name='process', target=main, args=[mainfilename, csvmode])
the_process.start()
while the_process.is_alive():
    animated_loading()
#if __name__ == "__main__":