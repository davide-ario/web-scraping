#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:14:13 2020

@author: davide
"""
#the next functions are defined to donwload trade regional data (as a panel dataset) from the istat website
# Url target
urlpage = 'https://www.coeweb.istat.it/predefinite/tutto_merce_territorio.asp?livello=ATE07_AT3&riga=MERCE&territorio=S'

#packages to import
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
from bs4 import BeautifulSoup as BSoup

#define function to collect the name and code of countries, goods and year in the dataset
def get_elements_byname(name, link, hide_browser):
    #name = the name of the input field in the html structure; link = the url target; hide_browser=True for hidden browser
    options = Options()
    options.headless = hide_browser

    driver = webdriver.Firefox(options=options)
    driver.get(link)
    ab=driver.find_element_by_name(name)
    ab_option = ab.find_elements_by_tag_name('option')
    data_temp=[]
    for ab_elem in ab_option:
        des = ab_elem.text
    #    link = result.find_element_by_tag_name('a')
        cod = ab_elem.get_attribute("value")
        # append dict to array
        data_temp.append({"description" : des, "code": cod})
    data_temp=pd.DataFrame(data_temp)
    driver.quit()
    return(data_temp)

# examples
# Url target
urlpage = 'https://www.coeweb.istat.it/predefinite/tutto_merce_territorio.asp?livello=ATE07_AT3&riga=MERCE&territorio=S'
# 1. download the list and code of available goods
merci=get_elements_byname('MERCE', link=urlpage, hide_browser=True)
# 2. download the list and code of available year, showing browser activity
anni=get_elements_byname('ANNO', link=urlpage, hide_browser=False)
# 3. download the list and code of available countries
paesi=get_elements_byname('PAESE', link=urlpage, hide_browser=True)



# this is a fast function to copy data from any html table
def get_table():
##download table from opened page and select rows
    bs_obj = BSoup(driver.page_source, 'html.parser')
    table= bs_obj.find_all('table')
    body= table[1].find('tbody')
    rows= body.find_all('tr')
    #create empty variables
    file_data = []
    file_header = []
    ##download header (column names)
    file_header = []
    th_row=rows[0].find_all('th')
    i=0
    while i!= len(th_row):
        col_name = th_row[i].get_text().strip()
        file_header.append(col_name)
        i+=1
    i=0
    ##download data
    file_data=[]
    i=0
    while i != len(rows):
        j=0
        file_row=[]
        row_td= rows[i].find_all('td')
        while j != len(row_td):
            datum_text = row_td[j].get_text().replace('.','').strip()
            file_row.append(datum_text)
            j+=1
        file_data.append(file_row)
        i+=1
    i=0
    ##drop empty rows
    file_data=[x for x in file_data if x != []]
    #createdataset
    df = pd.DataFrame(file_data)
    df.columns=file_header
    return(df)


# this function: navigate the browser to selct the product, partner country, year and quarter selected; donwload the data and return a panel dataset.
# product_code and country_code are defined in the results of  merci=get_elements_byname('MERCE', link=urlpage, hide_browser=True) and paesi=get_elements_byname('PAESE', link=urlpage, hide_browser=True)
# year and quarter are the selected time variables
#cumulated is == True for cumulated period, as define in the istat website
def get_data(product_code, country_code, year,  quarter,  link, cumulated):
    #connect to the url specified by the link
    driver.get(link)
    #
#    time.sleep(1+random.randint(1,7))

    #select product
    merce = Select(driver.find_element_by_name('MERCE'))
    merce.select_by_value(product_code)
    #select year
    anno = Select(driver.find_element_by_name('ANNO'))
    anno.select_by_value(year)
    #select partner country
    paese = Select(driver.find_element_by_name('PAESE'))
    paese.select_by_value(country_code)
    # select quarter
    paese = Select(driver.find_element_by_name('MESE'))
    paese.select_by_value(quarter)
    #select cumulated or single
    if cumulated == True    :
        cum = "input[type='radio'][value='C']"
    else:
        cum = "input[type='radio'][value='M']"
    driver.find_element_by_css_selector(cum).click()
    #open page with selected data
    driver.find_element_by_name('B2').click()
    # copy table into a panel dataset
    df=get_table()
    #define a dictionary for the id fields "PROVINCE"
    dict_prv =  {v: k for k, v in df.PROVINCE.items()}
    #create the id variable to reshape the data
    df["id"]=df["PROVINCE"].map(dict_prv).fillna(df["PROVINCE"])
    # define trade partner, sector, quarter and cumulated variables
    df["PARTNER"]=country_code
    df["SECTOR"]=product_code
    df["QUARTER"]=quarter
    if cumulated == True:
        df["PERIOD"]='c'
    else:
        df["PERIOD"]='m'
    # dataset  from wide to long
    df= pd.wide_to_long(df, stubnames=["IMP", "EXP"], i="id", j="ANNO" )
    # define anno and id (province) variables
    df["ANNO"]= df.index.get_level_values('ANNO')
    df["id"]= df.index.get_level_values('id')

    return(df)

#Example
#download export and import values for the product CL291 (autovehicles) with partner country 4 (Germany) in year 2015, for each nuts3 district area in Italy
#be aware, istat website download data from the selected year t to t-3. Selecting 2015, the function will provide results for year from 2013 to 2015.
Car_trade_with_Germany=get_data(product_code='CL291', country_code='4', year='2015', quarter='4', cumulated=True,  link=urlpage)


###########################################################
#Using the previous functions we can easily download all the data we need into a panel dataset.
#the following code create:
#1. one csv file with name prod#c#15  located in the directory '/home/davide/pythonData/example/' (you can change it with your path) for each product, country and year selected
#2. one csv file with name Allprod15c#  located in the directory '/home/davide/pythonData/example/' (you can change it with your path) for all the products and the already downloaded countries in the year you selected
# using the csv file as a backup, is possible to stop and resume the download of the data from the last downloaded country or product

#We select all the country, year and goods we want to push into our dataset
paesi_subset=paesi[0:222]
merci_subset = merci[0:10]

#we create our python dataset
example_sub=pd.DataFrame()
#we open the browser connection with the hidden option
options = Options()
options.headless = True
time.sleep(0)
driver = webdriver.Firefox(options=options)
#we start to iterate over our variable
i=0
j=0
while i !=len(paesi_subset.code):
    c_temp = paesi_subset.code[i]
    j=0
    while j != len(merci_subset.code):
        merc_temp=merci_subset.code[j]
        try:
            dt=get_data(product_code=merc_temp, year='2015', country_code=c_temp, quarter='4', cumulated=True,  link=urlpage)
            #the following code create a csv file with name prod#c#15  located in the directory '/home/davide/pythonData/example/' (you can change it with your path) for the product, country and year selected
            name=('/home/davide/pythonData/example/prod{}c{}15.csv'.format(merc_temp, c_temp))
            dt.to_csv(name)
            example_sub= example_sub.append(dt, ignore_index=True, sort=False)
            print('product {} for country "{}" downloaded and appended'.format(merc_temp, c_temp))
            j+=1
        except:
            print('product {} for country "{}" returns an empty list'.format(merc_temp, c_temp))
            j+=1
    #the following code creates a csv file with name Allprod15c#  located in the directory '/home/davide/pythonData/example/' (you can change it with your path) for all the product with the already processed country in the selected year
    name_a=('/home/davide/pythonData/example/Allprod15c{}.csv'.format(c_temp))
    example_sub.to_csv(name_a)
    i+=1
driver.quit()
