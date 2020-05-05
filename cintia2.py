#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classificador Inteligente de Supernovas do tipo Ia v2
                          CINTIA 2
Last Modified: 19/04/2020

                                *********************

Desenvolvida no programa de Pós-Graduação em Computação Aplicada
do Instituto Nacional de Pesquisas Espacias (São José dos Campos - SP, Brasil)

Título da dissertação: CLASSIFICAÇÃO INTELIGENTE DE SUPERNOVAS UTILIZANDO 
HIERARQUIA DE REDES NEURAIS ARTIFICIAIS
Defesa em 10/05/2019
Autora: Francisca Joamila Brito do NASCIMENTO (joamila.brito@gmail.com)
Orientador: Dr. Lamartine N.F. GUIMARÃES

Módulo de pré-processamento desenvolvido de acordo com:
    Luis Ricardo ARANTES FILHO (Classificação Inteligente de Supernovas utilizando
    Sistemas de Regras Nebulosas. Dissertação (Mestrado em Computação
    Aplicada) — Instituto Nacional de Pesquisas Espaciais (INPE), São José dos
    Campos, 2018.)
    
CIntIa v1 desenvolvida por:
    Marcelo MÓDOLO (Classificação Automática de Supernovas Usando Redes
    Neurais Artificiais. Tese (Doutorado em Computação Aplicada) — Instituto
    Nacional de Pesquisas Espaciais (INPE), São José dos Campos, 2016.)

Os dados usados para treinar o classificador foram obtidos em:
    The Open Supernova Catalog: https://sne.space

Agradecimentos à Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - 
Brasil (CAPES) pelo suporte financeiro, Código de Financiamento 001.    
                                         
                       ****************************

Developed at Instituto Nacional de Pesquisas Espacias 
Applied Computing Graduate Program 
São José dos Campos - SP, Brasil

Master thesis title: INTELLIGENT CLASSIFICATION OF SUPERNOVAE USING A HIERARCHY 
OF ARTIFICIAL NEURAL NETWORKS
Author: Francisca Joamila Brito do NASCIMENTO (joamila.brito@gmail.com)
Supervisor: Dr. Lamartine N.F. GUIMARÃES

Preprocess module developed in accordance with:
    Luis Ricardo ARANTES FILHO (Classificação Inteligente de Supernovas utilizando
    Sistemas de Regras Nebulosas. Dissertação (Mestrado em Computação
    Aplicada) — Instituto Nacional de Pesquisas Espaciais (INPE), São José dos
    Campos, 2018.)

CIntIa v1.0 developed by:
    Marcelo MÓDOLO (Classificação Automática de Supernovas Usando Redes
    Neurais Artificiais. Tese (Doutorado em Computação Aplicada) — Instituto
    Nacional de Pesquisas Espaciais (INPE), São José dos Campos, 2016.)
    
The data used to train the classifier were obtained in:
    The Open Supernova Catalog: https://sne.space
    
Thanks to Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - 
Brasil (CAPES) for the financial support, Financing Code 001.   

"""
import csv, datetime, os
import pandas as pd

from preclass_types import pipeline
from datavisualization import plotScatter

#Executa módulo especificado (Ia, Ib, Ic ou II)
#Runs specified module (Ia, Ib, Ic or II)
def runModule(module, pathFile):
   print('Running module ' + module + '...\n')

   os.chdir(os.path.join(pathFile, 'M' + module))
   cmd = os.path.join(pathFile, 'M' + module + '/Modulo' + module)
   os.popen(cmd).read()
   
   pathLabeled = os.path.join(pathFile, 'M' + module + '/Classificacao_ModuloEntradaRNA_' + module + '_.csv')
   
   try:
       labeled = pd.read_csv(pathLabeled, delimiter=';')
   except:
       print("\nSorry, an error happened. I cannot classify the supernovae. :(\n")
       return
   
   types = []
   for index, row in labeled.iterrows():
       if row['Saida'] > 0.5:
           types.append(1)
       else:
           types.append(0)
   
   return types

#Salva relatório de classificação
#Saves a log about the classification
def saveLog(patterns, pathFile):
    date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    
    fileOutput = os.path.join(pathFile, 'Logs/log_' + date + '.csv')

    with open(fileOutput, 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(['Padrao', 'Supernova', 'Espectro', 'Classificacao'])
        for row in patterns:
            wr.writerow(row)
            
    print('Results saved!\n')

#Executa classificador e salva relatório
#Runs classifier and saves log
def runClassifier(patterns, pathFile, isomap_data):
    print('Classifying...\n')
    
    classIa = runModule('Ia', pathFile)
    classII = runModule('II', pathFile)
    classIb = runModule('Ib', pathFile)
    classIc = runModule('Ic', pathFile)

    classeSalva = []
    classGeneral = []
    
    for position in range(len(patterns)):
        classPattern = []
        classPattern.extend([position+1, patterns[position][1], patterns[position][2]])
        
        if classIa[position] == 1:
            classPattern.append('Tipo Ia')
        elif classII[position] == 1:
            classPattern.append('Tipo II')
        elif classIb[position] == 1:
            classPattern.append('Tipo Ib')
        elif classIc[position] == 1:
            classPattern.append('Tipo Ic')
        else:
            classPattern.append('Tipo Não Identificado')
        
        classGeneral.append(classPattern)
        
        classeSalva.append([position+1, patterns[position][1], patterns[position][2],
                              classIa[position], classIb[position], classIc[position],
                              classII[position]])
        
    fileOutput = os.path.join(pathFile, 'Logs/Votacao.csv')
    with open(fileOutput, 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(['Padrao', 'Supernova', 'Espectro', 'Class Ia', 'Class Ib', 'Class Ic', 'Class II'])
        for row in classeSalva:
            wr.writerow(row)
        
    if len(classGeneral) >= 10:
        print('Visualizing data...\nClose figures to keep CINTIA 2 running!\n')

        plotScatter(isomap_data[0], isomap_data[1], 'Ia', classGeneral)
        plotScatter(isomap_data[2], isomap_data[3], 'Ib', classGeneral)
        plotScatter(isomap_data[4], isomap_data[5], 'Ic', classGeneral)
        plotScatter(isomap_data[6], isomap_data[7], 'II', classGeneral)
    
    print('\n')
    print('------------CLASSIFICATION------------')
    for padrao in classGeneral:
        print('Pattern: ' + str(padrao[0]))
        print('Supernova: ' + padrao[1])
        print('Spectrum: ' + padrao[2])
        print('Classification: ' + padrao[3])
        print('\n')
    
    saveLog(classGeneral, pathFile)
    
    print('I am glad to have helped you.\nNow, I am going to rest. Bye!\n')
    
     
#Principal
#Main
def main():
    print("\nHello, I am CINTIA 2! \nI am helping you to classify some Supernovae.\nStay with me.\n")
    patterns, pathFile, isomap_data = pipeline()
    
    if patterns != 0:
        runClassifier(patterns, pathFile, isomap_data)

#Execução do programa
#Runs software
main()
