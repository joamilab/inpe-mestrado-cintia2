#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:53:18 2018
Last Modified: 19/04/2020
@author: joamila
"""

import matplotlib.pyplot as plt
import datetime
import os
import pandas as pd
from sklearn.manifold import Isomap

from extractfeatures import getPathFile

def plotSpectra(spectra):    
    plt.figure(1, figsize=(10,8))
    
    for index, spectrum in spectra.iterrows():
        plt.plot(spectrum[2], spectrum[3], label=spectrum[1])
    
    plt.legend(loc="upper right", fontsize="x-small", framealpha=0.5, markerfirst=False)    
    plt.xlabel('wavelength')
    plt.ylabel('flux')
    plt.title('Supernovae Spectra (after preprocessing)')
    
    pathFile = getPathFile()
    name_figure = "Spectra_" + str(datetime.datetime.now()) + ".png"
    
    plt.savefig(pathFile + '/Images/' + name_figure)
    
    plt.show()
    
    
def applyIsomap(spectra):
    spectraFlux = []
    
    for spectrum in spectra:
        if spectrum != 0:
            spectrumDf = pd.DataFrame(spectrum)
            spectraFlux.append(spectrumDf.iloc[:,0])
            
    iso = Isomap(n_components=2, n_jobs=-1).fit_transform(spectraFlux)
    isoDf = pd.DataFrame(iso)
    
    return isoDf.iloc[:,0], isoDf.iloc[:,1]
    

def plotScatter(xs, ys, rna, patterns): 
    
    patternsDf = pd.DataFrame(patterns)
    
    colors_dict = {'Tipo Ia': 'red', 'Tipo Ib': 'blue', 'Tipo Ic': 'green', 
                   'Tipo II': 'purple', 'Tipo Não Identificado': 'gray'}
    
    colors = []
    sn_types = []
    for index, pattern in patternsDf.iterrows():
        colors.append(colors_dict[pattern[3]])
        sn_types.append(pattern[3])
        
    if rna == 'Ia':
        numberFig = 2
    elif rna == 'Ib':
        numberFig = 3
    elif rna == 'Ic':
        numberFig = 4
    else:
        numberFig = 5
    
    plt.figure(numberFig, figsize=(10,8))
    
    index = 0
    plots = []
    sn_types_aux = []
    for y in ys:
        plot_scatter = plt.scatter(xs[index], y, color=colors[index])
        if sn_types[index] not in sn_types_aux:
            sn_types_aux.append(sn_types[index])
            plots.append(plot_scatter)
        
        index = index+1
    plots.reverse()
    sn_types_aux.reverse()
    
    plt.legend((plots), (sn_types_aux), loc="upper right", title="Types")
    plt.title('RNA ' + rna + ': scatter plot of spectra after classification.') 
    plt.xlabel('first component isomap')
    plt.ylabel('second component isomap')

    pathFile = getPathFile()
    name_figure = "Scatter_" + rna + "_" + str(datetime.datetime.now()) + ".png" 
    
    plt.savefig(pathFile + '/Images/' + name_figure)
    
    if rna == 'II':
        plt.show()
