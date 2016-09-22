
#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
import commondef as comm
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
        df = ts.get_industry_classified()
        df.insert(0, 'stockcode', df.index)
        df.to_sql('stockindustry', self.engine, if_exists='replace', index=False)
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
                print ('          '+kt+':' , code, '-  data end')
if __name__ == '__main__':
    print (len(sys.argv))
    if (len(sys.argv)==2):
       print ('inital DB')
       StockBase().InitialStock()
    elif (len(sys.argv)==1):
       print('append db')
       StockBase().AppendStock()

#End