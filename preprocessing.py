#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:56:30 2018
Last Modified: 16/04/2020
@author: joamila
"""

import pandas as pd
import numpy as np
import os
from scipy import interpolate, signal

#Interpola todos os espectros, cada um em 1000 pontos
#Interpolate all the spectra, each one in 1000 points
def interpolate1000Points(spectrum):
    x = spectrum.iloc[:,0]
    y = spectrum.iloc[:,1] 
    
    f = interpolate.interp1d(x,y,kind='linear') 

    interval = (x.iloc[-1]-x.iloc[0])/1000
    
    if (interval>1):
        xinterp = np.arange(x.iloc[0], x.iloc[-1], interval)

        if xinterp[len(xinterp)-1] > x.iloc[-1]:
           xinterp[len(xinterp)-1] =  x.iloc[-1]
        yinterp = f(xinterp)
    else:
        xinterp = x
        yinterp = y
    
    data = {'Comprimento': xinterp, 'FluxoInterp': yinterp}
    spectrumInterpolate = pd.DataFrame(data, columns=['Comprimento', 'FluxoInterp'])
    
    return spectrumInterpolate

#Normaliza os valores de fluxo de cada espectro entre 0 e 1
#Normalize the flux values of each spectrum between 0 and 1    
def normalize(spectrum):
    flux = spectrum.iloc[:,1]
    
    fluxMax = max(flux)
    fluxMin = min(flux)
    
    fluxNormalized = []
    for measure in flux:
        fluxNormalized.append((measure-fluxMin)/(fluxMax-fluxMin))
    
    data = {'Comprimento': spectrum.iloc[:,0], 'FluxoNorm': fluxNormalized}
    spectrumNormalized = pd.DataFrame(data, columns=['Comprimento', 'FluxoNorm'])
    
    return spectrumNormalized

#Filtra cada espectro duas vezes usando o filtro de Savitzky-Golay
#Filter each spectrum two times with the Savitzky-Golay's filter
def doubleFiltration(spectrum):
    flux = spectrum.iloc[:,1]
    
    #Filtra duas vezes
    fluxFiltered = signal.savgol_filter(signal.savgol_filter(flux, 71, 9), 71, 9)
    
    data = {'Comprimento': spectrum.iloc[:,0], 'FluxoFiltr': fluxFiltered}
    spectrumFiltered = pd.DataFrame(data, columns=['Comprimento', 'FluxoFiltr'])
    
    return spectrumFiltered

#Ajusta os valores de comprimento de onda de cada espectro seguindo as informações de redshift
#Fit the wavelength values of each spectrum with the redshift values   
def fitRedshift(spectrum, redshift):
    wavelength = spectrum.iloc[:,0]
    
    wavelengthFitted = []
    for measure in wavelength:
        wavelengthFitted.append(measure/(redshift+1))
    
    data = {'Comprimento': wavelengthFitted, 'Fluxo': spectrum.iloc[:,1]}
    spectrumFitted = pd.DataFrame(data, columns=['Comprimento', 'Fluxo'])
    
    return spectrumFitted

#Aplica ajuste de redshift, interpolação, normalização e dupla filtragem
#Preprocess each spectrum: fit redshift, interpolate, normalize, double filtration
def preprocess(folder, redshifts):
    listOfFiles = os.listdir(folder)

    supernovae = []
    names = []
    wavelength = []
    flux = []
    
    for file in listOfFiles:
        print(file)
        nameFile = file.split('.csv')
        names.append(nameFile[0])
        
        title = file.split('-')
        size = len(title)
        if size == 4:
           supernova = title[0]+'-'+title[1]+'-'+title[2] 
        elif size == 3:
            supernova = title[0]+'-'+title[1]
        elif size == 2 or size == 1:
            supernova = title[0] 
            
        supernovae.append(supernova)
        
        for index, row in redshifts.iterrows():
            if supernova == row['Name Disc.']:
                redshift = row['Redshift']
                break
        
        os.chdir(folder)
        fil = pd.read_csv(file)
        
        fitted = fitRedshift(fil, redshift)
        interpolated = interpolate1000Points(fitted)
        normalized = normalize(interpolated)
        filtered = doubleFiltration(normalized)
    
        wavelength.append(pd.Series(filtered['Comprimento']))
        flux.append(pd.Series(filtered['FluxoFiltr']))
        
    data = {
            'Supernova':  supernovae,
            'NameOfFile': names,
            'Wavelength': wavelength,
            'Flux': flux
            }
    
    spectraDf = pd.DataFrame(data, columns=['Supernova', 'NameOfFile', 'Wavelength', 'Flux'])
     
    return spectraDf