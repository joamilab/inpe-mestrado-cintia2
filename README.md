# CINTIA 2
Classificador Inteligente de Supernovas do Tipo Ia - v2.1

## O que é
A CINTIA 2 é um classificador de Supernovas em tipos Ia, Ib, Ic e II (com ênfase no Tipo Ia) que usa redes neurais artificiais como ferramenta de classificação; e espectros de luz das Supernovas como dados de entrada.

A CINTIA 2 foi desenvolvida na dissertação de Mestrado de Francisca Joamila Brito do Nascimento, intitulada **CLASSIFICAÇÃO INTELIGENTE DE SUPERNOVAS UTILIZANDO HIERARQUIA DE REDES NEURAIS ARTIFICIAIS**, programa de Computação Aplicada do Instituto Nacional de Pesquisas Espaciais (INPE).

Agradecimentos à Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - Brasil (CAPES) pelo suporte financeiro, Código de Financiamento 001. 

### Dados usados
Os dados usados para treinar e testar o classificador foram obtidos em: [The Open Supernova Catalog](https://sne.space)

*GILLOCHON, J.; PARRENT, J.; KELLEY, L. Z.; MARGUTTI, R. An open catalog for supernova data. The Astrophysical Journal, v. 835, n. 1, p. 64, 2017.*

### Como citar
Se usar a CINTIA 2, por favor, cite os seguintes trabalhos:

*NASCIMENTO, F.J.B. Classificação inteligente de supernovas utilizando hierarquia de redes neurais artificiais. Dissertação (Mestrado em Computação Aplicada) — Instituto Nacional de Pesquisas Espaciais (INPE), São José dos Campos, 2019.*

*NASCIMENTO, F. J. B.; ARANTES FILHO, L. R.; GUIMARãES, L. N. F. Intelligent classification of supernovae using artificial neural networks. Inteligencia Artificial, v. 22, n. 63, p. 39–60, 2019.*

*DO NASCIMENTO, F. J. B.; ARANTES FILHO, L. R.; GUIMARÃES, L. N. F.. CINTIA 2: uma hierarquia de redes neurais artificiais binárias para classificação inteligente de supernovas. REVISTA BRASILEIRA DE COMPUTAÇÃO APLICADA, v. 11, p. 31-41, 2019.*

### Acessar dissertação
A dissertação está disponível na [Biblioteca Digital do INPE](http://urlib.net/rep/8JMKD3MGP3W34R/3T3PTLP?ibiurl.backgroundlanguage=pt-BR)

## Como usar o software
### Pré-requisitos
* Sistema Operacional Linux (o software foi testado nas distribuições Ubuntu e Endless);
* Python 3.6 ou maior;
* Bibliotecas *pandas*, *matplotlib*, *sklearn*

### Como preparar as entradas
As entradas do software são um arquivo de redshifts e uma pasta com um ou mais espectros.

O arquivo com os valores de redshift deve ter a extensão .csv e possuir pelo menos duas colunas:
* 'Name Disc.' -> nome da Supernova;
* 'Redshift'   -> valor do redshift.

Os espectros devem estar dentro de uma mesma pasta e possuirem extensão .csv. Cada arquivo deve ter duas colunas:
* primeira coluna: valores de comprimento de onda;
* segunda coluna: valores de fluxo.

### Como executar
Na linha de comando ir até a pasta **/cintia2/** e executar:

`python cintia2.py <caminho-arquivo-redshift> <caminho-pasta-espectros>`

### Dados de teste fornecidos
A pasta **set_test** disponibilizada aqui já fornece uma pasta com alguns espectros e uma planilha com valores de redshift previamente preparados.

Todos os dados foram obtidos no The Open Supernova Catalog, citado anteriormente.

### Dados de saída
Além da classificação, o software também produz gráficos como saída. A classificação será salva na pasta *Logs*, enquanto os gráficos serão salvos na pasta *Images*.
