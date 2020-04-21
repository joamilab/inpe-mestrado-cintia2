#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:36:18 2018
Last Modified 17/04/2020
@author: joamila
"""
import pandas as pd
import sys

from preprocessing import preprocess 
from extractfeatures import interpolateInterval4000a7000, extractInputs, generateFileTest
from datavisualization import applyIsomap, plotSpectra

#Executa todas as tarefas de pré-classificação por tipos
#Executes all tasks of types pre-classification
def pipeline():
    fileRedshift = sys.argv[1]
    
    if not fileRedshift.endswith(".csv"):
        print('The redshifts file needs to have extension .csv. Try again!')
        return 0

    redshifts =  pd.read_csv(fileRedshift)    
    
    folderInput = sys.argv[2]
    
    print('Preprocessing...\n')
    spectra = preprocess(folderInput, redshifts)
    
    print('Visualizing data...\nClose figure to keep CINTIA 2 running!\n')
    plotSpectra(spectra)
      
    print('Interpolating...\n')
    spectraInterp = interpolateInterval4000a7000(spectra)
    
    print('Extracting inputs...\n')
    spectraInterv = extractInputs(spectraInterp)
    if len(spectraInterv) >= 10:
        x_ia, y_ia = applyIsomap(spectraInterv['IntervalIa'])
        x_ib, y_ib = applyIsomap(spectraInterv['IntervalIb'])
        x_ic, y_ic = applyIsomap(spectraInterv['IntervalIc'])
        x_ii, y_ii = applyIsomap(spectraInterv['IntervalII'])
    
        isomap_data = [x_ia, y_ia, x_ib, y_ib, x_ic, y_ic, x_ii, y_ii]
    else:
        isomap_data = []
    
    print('Generating files...\n')   
    patterns, pathFile = generateFileTest('II', spectraInterv)
    generateFileTest('Ia', spectraInterv)
    generateFileTest('Ib', spectraInterv)
    generateFileTest('Ic', spectraInterv)
    
    return patterns, pathFile, isomap_data