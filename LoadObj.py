#! usr/bin/python
#coding=utf-8
import numpy as np

class ObjLoader:
    def __init__(self):
        print "ObjLeader init";
    def LoadObj(self , filename):
        f = open(filename, "r");
        line = f.readline();
        while line:
            print line;
            line = f.readline();

        f.close();

if __name__ == '__main__':
    ObjLoader().LoadObj("AIRBOAT.OBJ");