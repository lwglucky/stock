#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-

DBURL = 'ec2-54-222-205-139.cn-north-1.compute.amazonaws.com.cn'
SQLNAME = 'lwglucky'
DBNAME =  'stocktest' # 'stocktest'  # 'stocku'
DBPWD = 'lwglucky518518'

def GetDbConnectionStr():
    str = "mysql://root:%s@%s/%s?charset=utf8" % (DBPWD, DBURL,DBNAME)
    return str