
#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
import commondef as comm
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine
import os,datetime,sys,getopt
import types


class StockBase:
    stockcode = None
    engine = None
    def __init__(self):
        print ("stockbase __init__ \n")
        self.stockcode = self.GetStockBase()

    def GetStockBase(self ):
        constr = comm.GetDbConnectionStr();
        print ("GetDayStockData:" + constr)
        self.engine = create_engine(constr)
        stocks = ts.get_stock_basics()
        stocks.insert(0, 'stockcode', stocks.index)
        print(stocks)
        stocks.to_sql('stockbase', self.engine, if_exists='replace', index=False)
    #    stocks.to_csv('/CSV/' +'stockbase.CSV')
        df = ts.get_industry_classified()
        df.insert(0, 'stockcode', df.index)
        df.to_sql('stockindustry', self.engine, if_exists='replace', index=False)
    #    df.to_csv('/CSV/' + 'stockindustry.CSV')
        df = ts.get_hs300s()
        df.to_sql('hs300s', self.engine, if_exists='replace', index=False)
        df = ts.get_sz50s()
        df.to_sql('sz50s', self.engine, if_exists='replace', index=False)
        df = ts.get_concept_classified()
        df.to_sql('concept_classified', self.engine, if_exists='replace', index=False)
        return stocks

    def GetDayStock(self ):
        now = datetime.datetime.now()
        day = now.strftime('%Y-%m-%d')
        for (code, name) in zip(self.stockcode.index, self.stockcode['name']):
            print (code, '-', name)
            df = ts.get_hist_data(code,  start='2012-04-01', end=day, retry_count=50)
            if type(df) is types.NoneType:
                continue
            df.insert(0, 'DT', df.index)
            df.to_sql(code + '_D' , self.engine, if_exists='replace', index=False)
            print ('          ', code, '-  data end')

    def StockTickData(self,code , stockdf):
        for dt in stockdf.DT:
            print ('            tick:' + code + '--'+ dt)
            ddf = ts.get_tick_data(code, dt)
            if type(ddf) is types.NoneType:
                continue
            ddf.insert(0, 'date', ddf.time)
            ddf.date = dt
            ddf.to_sql(code + '_tick', self.engine, if_exists='append', index=False)

    def InitialStock(self):
        now = datetime.datetime.now()
        day = now.strftime('%Y-%m-%d')
        for (code,name) in zip(self.stockcode.index , self.stockcode['name']):
            print (code , '-' , name)
            for kt in ['D', 'W' , 'M' ,'5', '15' , '30' , '60']:
                df = ts.get_hist_data(code , ktype = kt , start='2012-01-01' , end=day , retry_count=50  )
                if  type(df) is types.NoneType:
                    continue
                df.insert(0,'DT',df.index)
                df.to_sql(code+'_'+kt , self.engine , if_exists='replace' , index=False)
                print ('          '+kt+':' , code, '-  data end')
                if kt=='D':
                    self.StockTickData(code ,df)

        for (code) in ['sh','sz','sz50','zxb','cyb']:
            for kt in ['D', 'W', 'M', '5', '15', '30', '60']:
                df = ts.get_hist_data(code, ktype=kt, start='2012-01-01', end=day, retry_count=50)
                if  type(df) is types.NoneType:
                    continue
                df.insert(0, 'DT', df.index)
                df.to_sql(code + '_' + kt, self.engine, if_exists='replace', index=False)
                print ('          ' + kt + ':', code, '-  data end')


    def AppendStock(self):
        now = datetime.datetime.now()
        day = now.strftime('%Y-%m-%d')
        for (code,name) in zip(self.stockcode.index , self.stockcode['name']):
            print (code , '-' , name)
            for kt in ['D', 'W' , 'M' ,'5', '15' , '30' , '60']:
                df = ts.get_hist_data(code , ktype = kt , start=day , end=day , retry_count=8   )
                if  type(df) is types.NoneType:
                    continue
                df.insert(0,'DT',df.index)
                df.to_sql(code+'_'+kt , self.engine , if_exists='append' , index=False)
     #           df.to_csv('/CSV/' + code + '_' + kt + '.CSV')
                print ('          '+kt+':' , code, '-  data end')
                if kt=='D':
                    self.StockTickData(df,df)

        for (code) in ['sh','sz','sz50','zxb','cyb']:
            for kt in ['D', 'W', 'M', '5', '15', '30', '60']:
                df = ts.get_hist_data(code, ktype=kt, start=day, end=day, retry_count=50)
                if  type(df) is types.NoneType:
                    continue
                df.insert(0, 'DT', df.index)
                df.to_sql(code + '_' + kt, self.engine, if_exists='append', index=False)
                print ('          ' + kt + ':', code, '-  data end')

if __name__ == '__main__':
    print (len(sys.argv))
    if (len(sys.argv)>=2):
        print ('inital DB!!!!')
        StockBase().InitialStock()
    elif (len(sys.argv)==1):
       print('append db')
       StockBase().AppendStock()

#End