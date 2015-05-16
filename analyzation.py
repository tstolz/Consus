# -*- coding: utf-8 -*-
"""
Created on Fri May 08 10:50:51 2015

@author: Thomas Stolz
mailto: thomas.stolz@tum.de
"""

import os
import Tkinter as tk
import tkFileDialog as tkf
from types import FunctionType

def datei():
    root=tk.Tk()
    root.title("data analysis")
    dateien=list(tkf.askopenfilenames())
    root.destroy()
    return dateien

def files_from_folder(ending='.txt'):
    root=tk.Tk()
    root.title("data analysis")
    folder=tkf.askdirectory()
    root.destroy()
    dateien=[]
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(ending):
                dateien.append(os.path.join(root, f))
    return dateien

def manual_input(N=1, quantity='value', convert_to=unicode):
    r = []
    for i in xrange(N):
        raw=raw_input('Enter '+quantity+':')
        try:
            val=convert_to(raw)
        except:
            val=raw
        r.append(val)
    return r

def iterate(from_line_index, from_function_index, function_list, arg_list, data_list=[[]]):
    j=from_function_index
    i=from_line_index
    for function in function_list[j:]:
        #sometimes we want to use previous results for the next function call
        #we can just put the corresponding function into the argument list
        #the next lines check for a function and replace it by the last returned value
        arg_list_for_call=[]
        for arg in arg_list[j]:
            if type(arg)==FunctionType and arg in function_list:
                arg_list_for_call.append(data_list[i][function_list.index(arg)])
            else:
                arg_list_for_call.append(arg)
        value = function(*arg_list_for_call)
        if type(value) == list:
            # speichere die aktuelle Zeile, iteriere über die Liste, schreibe das nächste Element in 		# die aktuelle Zeile, arbeite die restlichen Funktionen ab, hänge die gespeicherte 		# Zeile an
            for element in value[:-1]: 
                data_list[i].append(element)
                # rekursion
                data_list=iterate(i,j+1,function_list, arg_list,data_list)
                i=len(data_list)
                data_list.append(data_list[-1][:j])	
            data_list[i].append(value[-1])
        else:
            data_list[i].append(value)
        j+=1
    return data_list
    
    
if __name__ == "__main__":
    
#-------------TEST SECTION
    def test0():
        return 0
    
    def test1():
        return [1,2,3,4,5,6]
    
    def test2(arg1,arg2):
        print arg1, arg2
        return 7
        
    def test3():
        return [8,9,10]
        
#    arg_list=[(),(),(test0, test1), ()]
#    function_list=[test0, test1, test2, test3]
# ----------------END TEST
            
    
    from analysis import *
    arg_list=[(),(files_from_folder),(files_from_folder),(files_from_folder,aomFreq)]
    function_list=[files_from_folder,pulseLength,aomFreq, center_deviation]
    
    data_list=iterate(0,0, function_list, arg_list)

        