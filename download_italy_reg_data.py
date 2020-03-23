#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:14:13 2020

@author: davide
"""

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import ssl
from selenium.webdriver.firefox.options import Options    
import urllib.request
import pandas as pd# specify the url
from selenium.webdriver.support.ui import Select

import random




urlpage = 'https://www.coeweb.istat.it/predefinite/tutto_merce_territorio.asp?livello=ATE07_AT3&riga=MERCE&territorio=S' 

merci=get_elements_byname('MERCE', link=urlpage, hide_browser=True)
anni=get_elements_byname('ANNO', link=urlpage, hide_browser=True)
paesi=get_elements_byname('PAESE', link=urlpage, hide_browser=True)




paesi_subset=paesi[0:222]
sub_anni = [ '2015', '2018']

df_tot=pd.DataFrame()   
for i in paesi_subset.code:
    c_temp = ('{}'.format(i))
    for j in merci.code:
        merc_temp=('{}'.format(j))
        dt=get_data(product_code=merc_temp, year='2018', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage, hide_browser=False)
        name=('/home/davide/pythonData/tradedata/prod{}c{}.csv'.format(j, i))
        dt.to_csv(name)
        df_tot= df_tot.append(dt, ignore_index=True, sort=False)
        print('product {} for country "{}" downloaded and appended'.format(j, i))
    name_a=('/home/davide/pythonData/tradedata/Allprodc{}.csv'.format(i))
    df_tot.to_csv(name_a)
df_tot=df_tot.drop_duplicates()


import gc
gc.collect()

import csv
merci.to_csv("/home/davide/pythonData/tradedata/a.csv")
 name=('/home/davide/pythonData/tradedata/prodick.csv')
merci.to_csv(name)


paesi_subset.code[0]



#prova

paesi_subset=paesi[0:18]
sub_anni = [ '2015', '2018']
merci_subset=merci


prova_tot=pd.DataFrame()   
i=0
while i !=len(paesi_subset.code):
    c_temp = paesi_subset.code[i]
    j=0
    while j != len(merci_subset.code):
        merc_temp=merci_subset.code[j]

        try:
            dt=get_data(product_code=merc_temp, year='2018', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage, hide_browser=False)
        except:
            print('connection problem, I try again...')
            continue
        
        name=('/home/davide/pythonData/prova/prod{}c{}.csv'.format(merc_temp, c_temp))
        dt.to_csv(name)
        prova_tot= prova_tot.append(dt, ignore_index=True, sort=False)
        print('product {} for country "{}" downloaded and appended'.format(merc_temp, c_temp))
        j+=1
    name_a=('/home/davide/pythonData/prova/Allprodc{}.csv'.format(c_temp))
    prova_tot.to_csv(name_a)
    i+=1
   
df_tot=df_tot.drop_duplicates()

#prova2
prova_tot=pd.DataFrame()   
i=0
j=0
options = Options()
options.headless = True
time.sleep(3)
driver = webdriver.Firefox(options=options)
while i !=len(paesi_subset.code):
    c_temp = paesi_subset.code[i]
    j=0
    while j != len(merci_subset.code):
        merc_temp=merci_subset.code[j]

        try:
            dt=get_data2(product_code=merc_temp, year='2018', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage)
        except:
            print('connection problem, I try again...')
            continue
        
        name=('/home/davide/pythonData/prova/prod{}c{}.csv'.format(merc_temp, c_temp))
        dt.to_csv(name)
        prova_tot= prova_tot.append(dt, ignore_index=True, sort=False)
        print('product {} for country "{}" downloaded and appended'.format(merc_temp, c_temp))
        j+=1
    name_a=('/home/davide/pythonData/prova/Allprodc{}.csv'.format(c_temp))
    prova_tot.to_csv(name_a)
    i+=1
driver.quit()













###da qui per def funct
#prova2
prova_tot=pd.DataFrame()   
i=0
j=0
options = Options()
options.headless = True
time.sleep(3)
driver = webdriver.Firefox(options=options)
while i !=len(paesi_subset.code):
    c_temp = paesi_subset.code[i]
    j=0
    while j != len(merci_subset.code):
        merc_temp=merci_subset.code[j]
        
        try:
            dt=get_data2(product_code=merc_temp, year='2018', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage)
        except:
            print('connection problem, I try again...')
            if try_count<5:
            try_count+=1
            continue
        
        name=('/home/davide/pythonData/prova/prod{}c{}.csv'.format(merc_temp, c_temp))
        dt.to_csv(name)
        prova_tot= prova_tot.append(dt, ignore_index=True, sort=False)
        print('product {} for country "{}" downloaded and appended'.format(merc_temp, c_temp))
        j+=1
        try_count=0
    name_a=('/home/davide/pythonData/prova/Allprodc{}.csv'.format(c_temp))
    prova_tot.to_csv(name_a)
    i+=1
driver.quit()


###da qui per def funct
#prova2
prova_tot=pd.DataFrame()   

i=0
j=0
options = Options()
options.headless = True
time.sleep(0)
driver = webdriver.Firefox(options=options)
while i !=len(paesi_subset.code):
    c_temp = paesi_subset.code[i]
    j=0
    while j != len(merci_subset.code):
        merc_temp=merci_subset.code[j]
        try:
            dt=get_data3(product_code=merc_temp, year='2015', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage)
            name=('/home/davide/pythonData/prova/prod{}c{}15.csv'.format(merc_temp, c_temp))
            dt.to_csv(name)
            prova_tot= prova_tot.append(dt, ignore_index=True, sort=False)
            print('product {} for country "{}" downloaded and appended'.format(merc_temp, c_temp))
            j+=1
        except:
            print('product {} for country "{}" returns empty list'.format(merc_temp, c_temp))
            j+=1
    name_a=('/home/davide/pythonData/prova/Allprod15c{}.csv'.format(c_temp))
    prova_tot.to_csv(name_a)
    i+=1
driver.quit()

paesi_subset=paesi[0:222]

merci_subset=merci
 prova_tot.to_csv('/home/davide/pythonData/prova/cty18-393.csv')
 
data_18= pd.read_csv('/home/davide/pythonData/prova/Allprod15c800.csv')
data_18=data_18.drop(['Unnamed: 0'],axis=1)
ITA_provTrade = data_18
ITA_provTrade= ITA_provTrade.append(prova_tot, ignore_index=True, sort=False)
 ITA_provTrade.to_csv('/home/davide/pythonData/prova/ITA_provTrade.csv')
