#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-

import tushare as ts
from sqlalchemy import create_engine

class StockBase:
    def __init__(self):
        print "stockbase __init__ \n"
    def GetSotckBase(self):
        engine = create_engine('mysql://user:lwglucky518518@ec2-54-222-205-139.cn-north-1.compute.amazonaws.com.cn/stock?charset=utf8')
        stocks  = ts.get_stock_basics();
        print stocks
        stocks.to_sql('stockbase', engine)


if __name__ == '__main__':
    StockBase().GetSotckBase();

#End