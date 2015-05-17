# -*- coding: utf-8 -*-
"""
Created on Fri May 08 14:53:22 2015

@author: Thomas Stolz
mailto: thomas.stolz@tum.de
"""

import numpy as np
import cPickle as pickle

def saveCSV(data,name='data.csv',sep=';'):
    f = open(name,"w")
    for line in data:
        f.writelines(["%s%s" % (entry,sep) for entry in line])
        f.write("\n")
    f.close()

def savePickle(data,name='data.p'):
    f = open(name, "wb")
    pickle.dump(data,f)
    f.close()
    

def loadPickle(name='data.p'):
    f = open(name, "rb")
    data=pickle.load(f)
    f.close()
    return data


def loadCSV(name='data.csv',sep=';'):
    f = open(name, "r")
    data=[]
    for line in f.readlines():
        data.append([])
        for s in line.split(sep)[:-1]:
            try:
                data[-1].append(float(s))
            except:
                data[-1].append(s)
    f.close()
    return data

def average(data, column, cond_cols):
    #average over all values in column (integer) 
    #where the values in cond_cols (tuple of integers) are the same
    values=[]
    cond_values=[]
    for l in data:
        cond = [l[i] for i in cond_cols]
        if cond in cond_values:
            values[cond_values.index(cond)].append(l[column])
        else:
            cond_values.append(cond)
            values.append([])
            values[-1].append(l[column])
    result=[]
    for i in xrange(len(values)):
        result.append(cond_values[i])
        result[-1].append(np.mean(values[i]))
        result[-1].append(np.std(values[i])/np.sqrt(len(values[i])))
    return result
    
    