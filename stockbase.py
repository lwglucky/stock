
#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
import commondef as comm
import tushare as ts
from sqlalchemy import create_engine

class StockBase:
    def __init__(self):
        print "stockbase __init__ \n"
    def GetSotckBase(self):
        constr = comm.GetDbConnectionStr() ;
        print constr;
        engine = create_engine(constr);

        df = ts.get_tick_data('600848', date='2015-12-22');
        df.to_sql('tick_data', engine);

        df = ts.get_hist_data('000875')
        df.to_excel( 'data/day/000875.xlsx'    )

        stocks  = ts.get_stock_basics();
        print stocks
        stocks.to_csv('data/day/000875.csv')
        stocks.to_sql('stockbase', engine)


if __name__ == '__main__':
    StockBase().GetSotckBase();

#End