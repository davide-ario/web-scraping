#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:04:43 2020

@author: davide
"""
#import packages (because we are working with dynamic websites, the installation of geckodriver is needed)
from bs4 import BeautifulSoup as BSoup
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import ssl
from selenium.webdriver.firefox.options import Options
import pandas as pd# specify the url
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import itertools


#the next 2 functions are created to select the data in the zefix calendar
def month_selection(month_to_select, cal_number):
#cal number = the calendar I want to select, 0 is the first (from date), 1 is the second (to date)
    #indexing start from 0 = january
    month_to_select=month_to_select-1
    selected_month=int(Select(driver.find_elements_by_class_name('pika-select-month')[cal_number]).first_selected_option.get_attribute('value'))

    if month_to_select>selected_month:
        n_next=month_to_select-selected_month
        i=0
        while i!=n_next:
            driver.find_elements_by_class_name('pika-next')[cal_number].click()
            i+=1
    elif month_to_select<selected_month:
        n_prev=selected_month-month_to_select
        i=0
        while i!=n_prev:
            driver.find_elements_by_class_name('pika-prev')[cal_number].click()
            i+=1
    else:
        print('month already selected')

def select_data(data, cal_number):
    if cal_number=="from":
        cal_number=0
    elif cal_number=="to":
        cal_number=1
    data=data.split('.')
    target= '/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[{}]/fieldset/div/input'.format(cal_number+2)
    datapicker= driver.find_element_by_xpath(target)
    datapicker.click()
    #select the year
    y=driver.find_elements_by_class_name('pika-select-year')
    y=Select(y[cal_number])
    y.select_by_value(data[2])
    #select the month (devo usare freccie perche' il selezionatore diretto da problemi)
    month_selection(int(data[1]), cal_number)
    #select the day of the month and insert date (!!be aware!! con 0)
    #datapicker.click()
    table=driver.find_elements_by_class_name('pika-table')[cal_number]
    day=(table.find_elements_by_class_name('pika-button'))
    day[int(data[0])-1].click()

#Example
# select_data("30.06.2018", 1)

#this is a fast function to copy the data from the html table
def get_table_zefix():
##download table from the opened html page and select rows
    bs_obj = BSoup(driver.page_source, 'html.parser')
    body= bs_obj.find('tbody')
    rows= body.find_all('tr')
    file_header=('ditta', 'estratto', 'idi', 'forma', 'sede', 'cantone', 'tipo')
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


# this function downloads the selected data
#canton is the name of the canton as defined in zefix website
#mutation is the type of mutation reported in the trade register, as defined in the zefix website
def zefix_data(urlpage, canton, mutation, from_data, to_data ):
    #time.sleep(5)
    try:
        driver.get(urlpage)
       #set italian language and extended search, waiting the page is loaded
        myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/div[1]/section/nav[2]/ul/li[3]/a')))
        myElem.click()
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[12]/a/div[1]/span[2]').click()
    except TimeoutException:
        print("Loading took too much time!")
    #select canton
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/div[1]/span').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/input[1]').send_keys(canton + Keys.ENTER)
    #select type of mutation (!!be aware!!! to use german definition of type of mutation; differently the search does not return the right results )
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/div[1]/span').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/input[1]').send_keys(mutation + Keys.ENTER)
    ## clear the input fields of the calendars data
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input').clear()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[3]/fieldset/div/input').clear()
    #insert the date in the first datapicker (date from)
    select_data(from_data, "from")
    #insert the date in the second datapicker (date to), be aware, it need some second for insertion
    select_data(to_data, "to")
    #time.sleep(3)
    #click search button
    driver.find_element_by_id('submit-search-btn').click()
    #waiting the website to give us an answer....
    time.sleep(7)
    data = pd.DataFrame()
    try:
        #select 100 result for each page
        cont=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[1]/zefix-pagination/nav/div[3]/div[2]/span[4]')))
        cont.click()
        #select the number of pages on which I need to iterate
        number_pages= int(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[1]/zefix-pagination/nav/div[1]/span[2]').text[1:])
        ##iterate over all the pages
        p=0
        while p != number_pages:
            input_page=driver.find_element_by_id('input-page-nr')
            result = get_table_zefix()
            data=data.append(result)
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[1]/zefix-pagination/nav/div[1]/div[3]').click()
            p+=1
        del p
        return(data)

    except:
        print('no result for this search or too much time for results')


# these scripts download the list of cantons and mutations reported in the zefix website
urlpage = 'https://www.zefix.ch/en/search/shab/welcome'
options = Options()
options.headless = False
time.sleep(0)
driver = webdriver.Firefox(options=options)
list_canton=driver.find_element_by_id('ui-select-choices-0').text
list_mutation=driver.find_element_by_id('ui-select-choices-3').text
driver.quit()

list_canton = list_canton.split('\n')
list_canton = [i[5:] for i in list_canton]
#this is the list of cantons I can insert in my zefix_data function
list_canton=['Aargau',
 'Appenzell I. Rh.',
 'Appenzell A. Rh.',
 'Bern',
 'Basel-Landschaft',
 'Basel-Stadt',
 'Fribourg',
 'Genève',
 'Glarus',
 'Graubünden',
 'Jura',
 'Luzern',
 'Neuchâtel',
 'Nidwalden',
 'Obwalden',
 'St. Gallen',
 'Schaffhausen',
 'Solothurn',
 'Schwyz',
 'Thurgau',
 'Ticino',
 'Uri',
 'Vaud',
 'Brig (Oberwallis)',
 'St-Maurice (Bas Valais)',
 'Sion (Valais Central)',
 'Zug',
 'Zürich']

###################################################################
#Example
###################################################################

#Open the browser in the zefix input mask, with visible browser
urlpage = 'https://www.zefix.ch/en/search/shab/welcome'
options = Options()
options.headless = False
time.sleep(0)
driver = webdriver.Firefox(options=options)
canton = 'Geneva'
mutation= 'lo'

#dowload the new firms registered in the canton of Geneve, from "01.01.2017" to "31.03.2017"
Geneva_neu=zefix_data(urlpage, canton='Geneve', mutation='neu', from_data="01.01.2017", to_data="31.03.2017")
#dowload the new firms registered in the canton of Ticino, from "01.10.2019" to "31.12.2019"
Ticino_neu=zefix_data(urlpage, canton='ticino', mutation='neu', from_data="01.10.2019", to_data="31.12.2019")
#dowload the firms deleted from the trade register in Ticino, from "01.10.2019" to "31.12.2019"
Ticino_canc=zefix_data(urlpage, canton='ticino', mutation='lo', from_data="01.10.2019", to_data="31.12.2019")
#dowload the firms in Ticino that changed adress from "01.10.2019" to "31.12.2019"
Ticino_trasf=zefix_data(urlpage, canton='ticino', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")
#dowload the firms in Ticino in liquidation due to bankruptcy from "01.10.2019" to "31.12.2019"
Ticino_fallim=zefix_data(urlpage, canton='ticino', mutation='k', from_data="01.10.2019", to_data="31.12.2019")

#download all the firms in Switzerland that changed the adress
#the first step is to define a dictionary for the name of canton (because Valais has multiple trade registers)
dic_canton={'Aargau':'AA',
 'Appenzell I. Rh.':'AI',
 'Appenzell A. Rh.':'AR',
 'Bern':'BE',
 'Basel-Landschaft':'BL',
 'Basel-Stadt':'BS',
 'Fribourg':'FR',
 'Genève':'GE',
 'Glarus':'GL',
 'Graubünden':'GR',
 'Jura':'JU',
 'Luzern':'LU',
 'Neuchâtel':'NE',
 'Nidwalden':'NW',
 'Obwalden':'OW',
 'St. Gallen':'SG',
 'Schaffhausen':'SH',
 'Solothurn':'SO',
 'Schwyz':'SZ',
 'Thurgau':'TG',
 'Ticino':'TI',
 'Uri':'UR',
 'Vaud':'VD',
 'Brig (Oberwallis)':'VS',
 'St-Maurice (Bas Valais)':'VS',
 'Sion (Valais Central)':'VS',
 'Zug':'ZG',
 'Zürich':'ZH'}

#here below the script that downloads all the Swiss firms that changed their adresses
adress_changed=pd.DataFrame()
for cant in list_cant:
    temp_data= zefix_data(urlpage, canton=cant, mutation='adress', from_data="01.10.2019", to_data="31.12.2019")
    try:
        temp_data['from_canton']=dic_canton[cant]
        print("canton {} appended".format(cant))
    except:
        print("canton {} search is empty".format(cant))
        continue
    adress_changed=adress_changed.append(temp_data)
driver.quit()

#save all the downloaded datasets as csv files, in the directory C:\Users\davide\Documents\lavoro\ (you can change the path)
Ticino_trasf_out= zefix_data(urlpage, canton='ticino', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")
Ticino_neu.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_aperture.csv', index=False, sep=';')
Ticino_canc.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_cancellazioni.csv', index=False, sep=';')
adress_changed.to_csv(r'C:\Users\davide\Documents\lavoro\adress_changed.csv', index=False, sep=';')
Ticino_fallim.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_fallim.csv', index=False, sep=';')
