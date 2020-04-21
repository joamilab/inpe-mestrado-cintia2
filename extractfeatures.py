#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 11:12:00 2018
Last Modified: 19/04/2020
@author: joamila
"""

import csv
import numpy as np
from scipy import interpolate
import pandas as pd
import os

#Interpola espectro a cada 8 pontos
#Interpolates spectrum every 8 points 
def interpolateSpectrum(spectrum):

    f = interpolate.interp1d(spectrum[2],spectrum[3])

    xinterp = np.arange(4000.0, 7000.0, 8)
    yinterp = f(xinterp)
    
    data = {
            'Wavelength': xinterp,
            'Flux': yinterp
            }
    
    interpolateInterval = pd.DataFrame(data, columns=['Wavelength', 'Flux'])
    
    return interpolateInterval

#Seleciona espectros com comprimento de onda entre 4000 e 7000 e interpola
#Selects spectra with wavelenght between 4000 and 7000 for interpolate
def interpolateInterval4000a7000(spectra):
    wavelength_interp = []
    flux_interp = []
    
    for index, row in spectra.iterrows():
        wavelength = row[2]
        
        if wavelength.iloc[0]<=4000 and wavelength.iloc[-1]>=7000:
            interp = interpolateSpectrum(row)
            wavelength_interp.append(interp.iloc[:,0])
            flux_interp.append(interp.iloc[:,1]) 
        else:
            wavelength_interp.append(0)
            flux_interp.append(0)
            print(str(row[1]) + ' not contains the interval 4000-7000 Angstroms.\n\tSorry, I cannot classify this spectrum.')
        
    spectra['WavelengthInterpolated'] = wavelength_interp
    spectra['FluxInterpolated'] = flux_interp
        
    return spectra

def extractInterval(spectrum, limitInf, limitUpp, classifier):
    values = []
    
    wavelength = spectrum[4]
    flux = spectrum[5]
    
    i = 0
    if limitUpp != limitInf:
        for w in wavelength:
            if w >= float(limitInf) and w <= float(limitUpp):
               values.append(flux[i]) 
            elif w > float(limitUpp):
                break
            i = i+1
    else:
        for w in wavelength:
            if (w >= 4000.0 and w<=5000.0) or (w>=6000.0 and w<=7000.0):
                values.append(flux[i])
            elif w > 7000.0:
                break
            i = i+1

    return values 

            
#Extrai entradas dos espectros
#Extract inputs from spectra
def extractInputs(spectra):
    intervalIa = []
    intervalIb = []
    intervalIc = []
    intervalII = []
    
    for index, spectrum in spectra.iterrows():
        if not(isinstance(spectrum['WavelengthInterpolated'], int)):
            intervalIa.append(extractInterval(spectrum, 5000.0, 6500.0, 'Ia'))
            intervalIb.append(extractInterval(spectrum, 5500.0, 7000.0, 'Ib'))
            intervalIc.append(extractInterval(spectrum, 5500.0, 6500.0, 'Ic'))
            intervalII.append(extractInterval(spectrum, 0, 0, 'II'))
        else:
            intervalIa.append(0)
            intervalIb.append(0)
            intervalIc.append(0)
            intervalII.append(0)
        
    spectra['IntervalIa'] = intervalIa
    spectra['IntervalIb'] = intervalIb
    spectra['IntervalIc'] = intervalIc
    spectra['IntervalII'] = intervalII
        
    return spectra


#Descobre o caminho do arquivo
#Get file's path
def getPathFile():
    pathFileAux = os.path.abspath(__file__)
    pathFolders = pathFileAux.split('/')
    
    amountFolders = len(pathFolders)
    count = 1
    pathFile = '/'
    
    while count < amountFolders-2:
        pathFile = pathFile + pathFolders[count] + '/'
        count = count + 1
    pathFile = pathFile + pathFolders[amountFolders-2]
    
    return pathFile

             
#Gera arquivo com os padrões para a classificação
#Generates a file with the patterns for classification 
def generateFileTest(rna, spectra):
    pathFile = getPathFile()
    
    rootFolder = pathFile + '/M' + rna
    fileOut = rootFolder + '/EntradaRNA_' + rna + '_Teste.csv'
    
    listOfParams = []
    patterns = []
    
    typeInterv = 'Interval' + rna
    
    i = 0
    for index, spectrum in spectra.iterrows(): 
        if rna == 'Ia':
            interval = spectrum[6]
        elif rna == 'Ib':
            interval = spectrum[7]
        elif rna == 'Ic':
            interval = spectrum[8]
        elif rna == 'II':
            interval = spectrum[9]
        
        if not(isinstance(interval, int)):
            parameters = []
            pattern = []
        
            for flux in interval:
                parameters.append(flux)
        
            parameters.extend(['', '', spectrum[0], '', '', '', '', '', spectrum[1]])
            listOfParams.append(parameters)
    
            pattern.extend([i+1, spectrum[0], spectrum[1]])
            patterns.append(pattern)
        
            i = i+1
    
    amountOfPatterns = [len(spectra[typeInterv])]
    with open(fileOut, 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(amountOfPatterns)
        for row in listOfParams:
            wr.writerow(row)
        wr.writerow(amountOfPatterns)
    
    return patterns, pathFile