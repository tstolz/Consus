# -*- coding: utf-8 -*-
"""
Created on Fri May 15 10:50:12 2015

@author: Thomas Stolz
mailto: thomas.stolz@tum.de
"""

import matplotlib.pyplot as plt
import numpy as np
from types import FunctionType

def indices(row, inds):
    return [row[i] for i in inds]
    
def select(row, inds, vals):
    for i in xrange(len(inds)):
        if row[inds[i]]!=vals[i]:
            return False
    return True

def exclude(row, inds, vals):
    for i in xrange(len(inds)):
        if row[inds[i]]==vals[i]:
            return False
    return True
    
def create_plot_lists(points):
    p = np.array(points)
    return p[p[:,0].argsort()].T
    
def averaged_plot_lists(points):
    'expects points to consist of x and y values'
    xvals=[]
    ylists=[]
    yvals=[]
    yerrs=[]    
    for p in points:
        if p[0] not in xvals:
            xvals.append(p[0])
            ylists.append([p[1]])
        else:
            ylists[xvals.index(p[0])].append(p[1])
    for i in xrange(len(xvals)):
        yvals.append(np.mean(ylists[i]))
        yerrs.append(np.std(ylists[i])/np.sqrt(len(ylists[i])))
    p = np.array([xvals, yvals, yerrs])
    return p[:,p[0,:].argsort()]
                

def prepare_plot_data(data_list, function_list):
    '''takes a list with rows of data and returns a list with data containers. 
    function_list has the following form:

        [[(select_columns, args), (preselect_rows, args), (postprocessing, args)], ... ]
        
    select_columns: takes a row of data (1D list) and returns a 'plot point'. 
                    If instead a tuple or list of indices is given, the default
                    function 'indices' (see above) is used.
    preselect_rows: takes a row and decides whether to actually include it in 
                    the plot (returns true or false). Ex.: select, exclude
    postprocessing: takes the list of plot points and creates a data container
                    for pyplot. Default is 'create_plot_lists'. 'averaged_plot_lists' 
                    is an interesting option to average over all points with same
                    x values.'''
    
    plots=[]
    for func in function_list:
        points=[]
        for row in data_list:
            #preselection
            if bool(func[1]) and (type(func[1]) == list or type(func[1])==tuple):
                if type(func[1][0]) == FunctionType:
                    if not func[1][0](row, *func[1][1]):
                        continue
            elif type(func[1])== FunctionType:
                if not func[1][0](row):
                    continue
            #select plot data from row
            if (type(func[0]) == list or type(func[0])==tuple) and bool(func[0]):
                if type(func[0][0]) == FunctionType:
                    points.append(func[0][0](row, *func[0][1]))
                elif type(func[0][0]) == int:
                    points.append(indices(row, func[0]))                    
            elif type(func[0])== FunctionType:
                points.append(func[0](row))
        #postprocessing
        if len(func)<3:
            plots.append(create_plot_lists(points))
        elif bool(func[2]) and (type(func[2]) == list or type(func[2])==tuple):
            if type(func[2][0]) == FunctionType:
                    plots.append(func[2][0](points, *func[2][1]))
        elif type(func[2]) == FunctionType:
            plots.append(func[2](points))
        else:
            plots.append(create_plot_lists(points))    
    return plots
    
        
def plot_it(plots, structure):
    '''Plots lines of data as returned by 'prepare_plot_data'. 'structure' has the
    following form:
        
        [[[(plot_type, kwargs_dict, index), ...],...],...]
            
    Every element of the outer list stands for a new figure, next comes a list
    of subfigures, and finally a list of lines. Each line consists of a list or
    tuple of plot_type, kwargs, and (optional) index. It can also just be a plot_type
    to choose standard settings. Optional plotting options can be given in the
    kwargs_dict, which has to be a dictionary with the correct argument names as
    described in the matplotlib documentation. Index chooses a specific line of 
    'plots', if not given the next element is taken.'''
        
    figures =[]
    subplots = []
    line_objects = []
    k=0
    for fig in structure:
        figures.append(plt.figure())
        #calculate number of rows and columns for the subplots
        #assume a screen aspect ratio of approx 3:2
        x=np.sqrt(len(fig)/1.5)
        cols=np.ceil(1.5*x)-1
        rows=np.ceil(x)
        for i in xrange(len(fig)):
            sub=fig[i]
            subplots.append(plt.subplot(rows,cols,i+1))
            for line in sub:
                if bool(line) and (type(line) == list or type(line) == tuple):
                    if len(line)==3:
                        j=line[2]
                    else:
                        j=k
                        k+=1
                    line_objects.append(line[0](*plots[j], **line[1]))
                elif type(line)==FunctionType:
                    line_objects.append(line(*plots[k]))
                    i+=1
                else:
                    line_objects.append(plt.plot(*plots[k]))
                    k+=1
            plt.legend()
    plt.show()
    return figures, subplots, line_objects
    
if __name__ == "__main__":
    from utility import *
    
    data=load(sep=',')
    print data
    function_list=[[(2,4), (select, [[3], [70e6+i*2e6]]), averaged_plot_lists] for i in range(11)]+[[(3,4),(select, [[2],[62e-9]]), averaged_plot_lists]]+[[[4],(select, [[2,3],[62e-9,70e6+i*2e6]]),create_plot_lists] for i in xrange(11)]
    structure=[[[(plt.errorbar,{"label": "%d MHz" % (70+i*2)}) for i in range(11)]],[[(plt.errorbar, {"marker":"o", "linestyle":"None"})]],[[(plt.hist, {"label":"%d MHz" % (70+i*2)})] for i in xrange(11)]]
    plots=prepare_plot_data(data, function_list)
    figs, subs, lines = plot_it(plots, structure)
    
    