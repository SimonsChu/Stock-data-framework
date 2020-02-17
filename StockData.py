# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:43:33 2019

@author: zhu hanfeng
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class StockData(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~Part1:~~~~~~~~~~~~~~~~~~~~~
    
    #E1.1  StockData.__init__(path)
    def __init__(self):
        self.path= 'D:/training/data'
        
    #E1.2  StockData.read(symbols)
    def read(self,symbols):
        
        OHLC=pd.DataFrame()
        
        for i in range(len(symbols)):
            df=pd.read_csv(self.path+'/'+symbols[i]+'.csv')
            OHLC=pd.concat([OHLC,df])
            OHLC1=OHLC[['TRADE_DT','S_INFO_WINDCODE','S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW','S_DQ_CLOSE']]
            OHLC1.columns=['date','symbols','open','high','low','close']
       
        return OHLC1
             
    #E1.3  StockData.get_data_by_symbol(symbol, start_date, end_date)
    def get_data_by_symbol(self,symbol,start_date,end_date):
        
        df=pd.read_csv(self.path+'/'+symbol+'.csv')
        OHLC2=df[['TRADE_DT','S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW','S_DQ_CLOSE']].sort_values('TRADE_DT')
        OHLC2.columns=['date','open','high','low','close']
        OHLC2=OHLC2.set_index('date').loc[start_date:end_date]
        
        return OHLC2
    
    #E1.4  StockData.get_data_by_date(adate, symbols)
    def get_data_by_date(self,adate,symbols):
        
        OHLC3=StockData.read(symbols)
        OHLC3=OHLC3.loc[OHLC3['date']==int(adate)]
        OHLC3=OHLC3.set_index('symbols')
        del OHLC3['date']
        
        return OHLC3
    
    #E1.5  StockData.get_data_by_filed(field, symbols)
    def get_data_by_field(self,field,symbols):
        
        OHLC=StockData.read(symbols)
        OHLC=OHLC[['symbols','date',str(field)]]
        OHLC4=pd.DataFrame(OHLC['date'])
        
        for i in range(len(symbols)):
            df=OHLC.loc[OHLC['symbols']==symbols[i]]
            df=df[['date',str(field)]]
            df.columns=['date',symbols[i]]
            OHLC4=pd.merge(OHLC4,df,how='outer',on='date').sort_values('date')
            OHLC4=OHLC4.set_index('date')
        return OHLC4

#~~~~~~~~~~~~~~~~~~~~~Part2:~~~~~~~~~~~~~~~~~~~~~~~~~
        
    #E2.1 StockData.format_date(symbol)
    def format_date(self,symbol):
        df=pd.read_csv(self.path+'/'+symbol+'.csv')
        datetime=pd.to_datetime(df['TRADE_DT'],format="%Y%m%d")
        
        df['TRADE_DT']=datetime
        df=df.sort_values('TRADE_DT')
        
        return df
    
    #E2.2 StockData.plot(symbol, field) 
    def plot(self,symbol,field):
        df=StockData.format_date(symbol)
        df=df[['TRADE_DT','S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW','S_DQ_CLOSE','S_DQ_VOLUME']]
        df.columns=['date','open','high','low','close','volume']
        
        fig=plt.figure()
        ax1=fig.add_subplot(1,2,1)
        ax2=fig.add_subplot(1,2,2)
        
        ax1.plot(df['date'],df[field[0]],linestyle='--',color='r')
        ax1.set_title(str(field[0]) + ' price with date'  )
        ax2.bar(df['date'],df[field[1]],color='r',alpha=0.9)
        ax2.set_title(str(field[1]) +  ' with date'  )
    
    #E2.3 StockData.adjust_data(symbol)
    def adjust_data(self,symbol):
        
        df=StockData.format_date(symbol)
        df=df.sort_values('TRADE_DT',ascending=False)
        df=df.reset_index()
        df['adj_factor']=(1/(1+df['S_DQ_PCTCHANGE']/100)).cumprod().shift(1)
        df['adj_factor'].iloc[0]=1
        last_price=df[['S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW','S_DQ_CLOSE']].iloc[0]
    
        df['adj_open']=(df['adj_factor']*last_price[0])
        df['adj_high']=(df['adj_factor']*last_price[1])
        df['adj_low']=df['adj_factor']*last_price[2]
        df['adj_close']=df['adj_factor']*last_price[3]
        df=df.sort_values('TRADE_DT')
        
        return df
    
    #E2.4 StockData.resample(symbol, freq)
    def resample(self,symbol,freq):
        df=StockData.format_date(symbol)
        df=df.set_index('TRADE_DT')
        df=df[['S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW','S_DQ_CLOSE','S_DQ_VOLUME','S_DQ_AMOUNT','S_DQ_AVGPRICE']]
        df=df.resample(freq).last()
        
        df['S_DQ_OPEN']=df['S_DQ_OPEN'].resample(freq).first()
        df['S_DQ_HIGH']=df['S_DQ_HIGH'].resample(freq).max()
        df['S_DQ_LOW']=df['S_DQ_LOW'].resample(freq).min()
        df['S_DQ_VOLUME']=df['S_DQ_VOLUME'].resample(freq).sum()
        df['S_DQ_AMOUNT']=df['S_DQ_AMOUNT'].resample(freq).sum()
        df['S_DQ_AVGPRICE']=df['S_DQ_AVGPRICE'].resample(freq).mean()
        
        return df

#~~~~~~~~~~~~~~~~~~~~~~Part3:~~~~~~~~~~~~~~~~~~~
        
    #E3.1 StockData.moving_average(symbol，field，window)
    def moving_average(self,symbol,field,window):
        
        df=StockData.adjust_data(symbol)
        df=df[['adj_open','adj_high','adj_low','adj_close','TRADE_DT']].set_index('TRADE_DT')
        MA=df[field].rolling(window).mean()
        
        return MA
    
    #E3.2 StockData.ema(symbol, params)
    def ema(self,symbol,field,window):
        
        df=StockData.adjust_data(symbol)
        df=df[['adj_open','adj_high','adj_low','adj_close','TRADE_DT']].set_index('TRADE_DT')
        EMA=df[field].copy()
        
        for i in range(len(df[field])):
            if i==0:
                EMA[i]=df[field][i]
            if i>0:
                EMA[i]=((window-1)*EMA[i-1]+2*df[field][i])/(window+1)
        
        return EMA
    
    
    #E3.3 StockData.atr(symbol, params)
    def atr(self,symbol,window):
        
        df=StockData.adjust_data(symbol)
        df=df[['adj_open','adj_high','adj_low','adj_close','TRADE_DT']].set_index('TRADE_DT')
        ATR=pd.Series(index=df.index)
        
        for i in range(1,len(df['adj_high'])):
            Temp=max(df['adj_high'][i]-df['adj_low'][i],np.abs(df['adj_close'][i-1]-df['adj_high'][i-1]))
            ATR[i]=max(Temp,np.abs(df['adj_close'][i]-df['adj_low'][i-1]))
        
        ATR=ATR.rolling(window).mean()
        return ATR
    
    #E3.4 StockData.rsi(symbol, params)
    def rsi(self,symbol,window,field):
        df=StockData.adjust_data(symbol)
        df=df[['adj_open','adj_high','adj_low','adj_close','TRADE_DT']].set_index('TRADE_DT')
        
        RSI=pd.Series(index=df.index)
        up_avg=0
        down_avg=0
        first_t=df[field][:window+1]
        
        for i in range(1,len(first_t)):
            if first_t[i]>=first_t[i-1]:
                up_avg+=first_t[i]-first_t[i-1]
            else:
                down_avg+=first_t[i-1]-first_t[i]
        up_avg=up_avg/window
        down_avg=down_avg/window
        rs=up_avg/down_avg
        RSI[window]=100-100/(1+rs)
        
        for j in range(window+1,len(df[field])):
            up=0
            down=0
            if df[field][j]>=df[field][j-1]:
                up=df[field][j]-df[field][j-1]
                down=0
            else:
                up=0
                down=df[field][j-1]-df[field][j]
            up_avg=(up_avg*(window-1)+up)/window
            down_avg=(down_avg*(window-1)+down)/window
            rs=up_avg/down_avg
            RSI[j]=100-100/(1+rs)
        return RSI
    
    
    #E3.5 StockData.macd(symbol, params)
    def macd(self,symbol,short_period,long_period,M,field):
        df=StockData.adjust_data(symbol)
        df=df[['adj_open','adj_high','adj_low','adj_close','TRADE_DT']].set_index('TRADE_DT')
     
        ema1=StockData.ema(symbol,field,short_period)
        ema2=StockData.ema(symbol,field,long_period)
        diff=ema1-ema2
        dea=pd.Series(index=df.index)
        
        for i in range(len(diff)):
            if i==0:
                dea[i]=diff[i]
            if i>0:
                dea[i]=((M-1)*dea[i-1]+2*diff[i])/(M+1)
        
        MACD=diff-dea

        return MACD
        
  

