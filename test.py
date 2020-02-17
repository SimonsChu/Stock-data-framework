# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 16:03:51 2019

@author: zhu hanfeng
"""
#~~~~~~~~~~~~~~~~~~Test Part~~~~~~~~~~~~

#1.1
StockData=StockData() 

#1.2
StockData.read(symbols=['300123.SZ','300127.SZ']).head()

#1.3
StockData.get_data_by_symbol(symbol='300123.SZ',start_date='20101011',end_date='20101020').head()

#1.4
StockData.get_data_by_date(adate='20131106',symbols=['300123.SZ','300127.SZ','600055.SH']).head()

#1.5
StockData.get_data_by_field(field='open',symbols=['600000.SH','600055.SH','600036.SH']).tail()

#2.1
StockData.format_date('300123.SZ')['TRADE_DT']

#2.2
StockData.plot('300123.SZ',['open','volume'])

#2.3
StockData.adjust_data(symbol='000001.SZ')[['adj_open','adj_high','adj_low','adj_close']]


#2.4
StockData.resample(symbol='000001.SZ',freq='5d')

#3.1
StockData.moving_average(symbol='000001.SZ',field='adj_close',window=5)
StockData.moving_average(symbol='000001.SZ',field='adj_close',window=20)
StockData.moving_average(symbol='000001.SZ',field='adj_close',window=60).plot()

#3.2
StockData.ema(symbol='000001.SZ',field='adj_close',window=5)
StockData.ema(symbol='000001.SZ',field='adj_close',window=20)
StockData.ema(symbol='000001.SZ',field='adj_close',window=60).plot()

#3.3
StockData.atr(symbol='000001.SZ',window=5)
StockData.atr(symbol='000001.SZ',window=20)
StockData.atr(symbol='000001.SZ',window=60)

#3.4
StockData.rsi(symbol='000001.SZ',field='adj_close',window=5)
StockData.rsi(symbol='000001.SZ',field='adj_close',window=20)
StockData.rsi(symbol='000001.SZ',field='adj_close',window=60).plot()

#3.5
StockData.macd(symbol='000001.SZ',field='adj_close',short_period=12,long_period=26,M=9)









