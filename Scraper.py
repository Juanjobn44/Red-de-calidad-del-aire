# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:27:00 2021

@author: Juanjo
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from itertools import zip_longest


def descargar(url):
    try: 
        html = requests.get(url)
    except ConnectionError as e:
        print('Error de descarga: ', e.reason, '\n')
        html = None
    return html
    


url = 'http://gestiona.madrid.org/azul_internet/html/web/DatosEstacion24Accion.icm?ESTADO_MENU=2_1'
html = descargar(url)


soup = BeautifulSoup(html.text, "html.parser")

horas_soup = soup.findAll("td",{'class':'txt07roj'})
horas = []
for i in horas_soup:
    horas.append(i.get_text().strip())




valores_soup = soup.findAll("td",{"class":"txt07neg"})
valores = []
for i in valores_soup:
    valores.append(i.get_text().strip())


nombres_soup = soup.findAll('td',{'class':'txt07azu'})
nombres = []
for i in nombres_soup:
    nombres.append(i.get_text().strip())


#Separamos entre contaminantes y parametros meteorológicos
cont = valores[:168]
cont_mat = np.array(cont).reshape(24,7)
horas_cont = horas[:24]
columns = ('TIN','NO','NO2','PM2.5','PM10','NOX','O3')
cont_df = pd.DataFrame(data=cont_mat, index=horas_cont, columns=columns)


param = valores[168:]
param_mat = np.array(param).reshape(24,7)
horas_param = horas[24:]
columns = ('VV','DV','TMP','HR','PRE','RS','LL')
param_df = pd.DataFrame(data=param_mat, index=horas_param, columns=columns)


#Importamos csv
#cont_df.to_csv('getafe_contaminantes.csv')
#param_df.to_csv('getafe_parametros.csv')





