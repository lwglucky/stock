#! usr/bin/python
#coding=utf-8
import numpy as np
from ctypes import *
import copy

class ObjLoader:
    def __init__(self):
        print "ObjLeader init";
    def LoadObj(self , filename):
        data = np.fromfile(filename,dtype=np.float);
        data = data.reshape(-1,3);
        ver = data[0:-1:2] ;
        norm = data[1:-1:2];
        norm = np.row_stack((norm,data[-1]));
        return ver , norm


if __name__ == '__main__':
    ver , norm = ObjLoader().LoadObj("dragon.dit");
    print ver.size , '-' , norm.size