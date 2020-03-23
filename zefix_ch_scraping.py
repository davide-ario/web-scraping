#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:04:43 2020

@author: davide
"""

from bs4 import BeautifulSoup as BSoup
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import ssl
from selenium.webdriver.firefox.options import Options
import urllib.request
import pandas as pd# specify the url
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import itertools
import time

def month_selection(month_to_select, cal_number):
#cal number is the calendar, 0 for from, 1 for to
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

#select_data("30.06.2018", 1)


def get_table_zefix():
##download table from opened page and select rows
    bs_obj = BSoup(driver.page_source, 'html.parser')
    body= bs_obj.find('tbody')
    rows= body.find_all('tr')
#    #create empty variables
#    file_data = []
#    file_header = []
#    ##download header (column names)
#    file_header = []
#    th_row=rows[0].find_all('th')
#    i=0
#    while i!= len(th_row):
#        col_name = th_row[i].get_text().strip()
#        file_header.append(col_name)
#        i+=1
#    i=0
    ##download data
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


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException






urlpage = 'https://www.zefix.ch/en/search/shab/welcome'
options = Options()
options.headless = False
time.sleep(0)
driver = webdriver.Firefox(options=options)
canton = 'Geneva'
mutation= 'lo'

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
#    try:
#        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/div[1]/span/a/i').clear()
#    except:
#        print('canton not selected')
    #select canton
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/div[1]/span').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/input[1]').send_keys(canton + Keys.ENTER)
    #select type of mutation (!!be aware!!! to use deutsch definition of type of mutation; differently the search does not return the right results )
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/div[1]/span').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/input[1]').send_keys(mutation + Keys.ENTER)
    ##prima di far partire qualsiasi cosa devo cancellare i due campi del calendario...
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input').clear()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[3]/fieldset/div/input').clear()
    #insert the date in the first datapicker (date from)
    select_data(from_data, "from")
    #insert the date in the second datapicker (date from), be aware, it need some second for insertion
    select_data(to_data, "to")
    #time.sleep(3)
    #click search button
    driver.find_element_by_id('submit-search-btn').click()
    #waiting the website give us an answer....
    time.sleep(7)
    #select 100 result for each page
    data = pd.DataFrame()
    try:
        cont=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[1]/zefix-pagination/nav/div[3]/div[2]/span[4]')))
        cont.click()
        number_pages= int(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[1]/zefix-pagination/nav/div[1]/span[2]').text[1:])
        ##da qui gli devo dire di leggere tutto i tr, poi per ogni elemento in tr leggere il td e prendere testo
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



Geneva_neu=zefix_data(urlpage, canton='Geneve', mutation='neu', from_data="01.01.2017", to_data="31.03.2017")

Ticino_neu=zefix_data(urlpage, canton='ticino', mutation='neu', from_data="01.10.2019", to_data="31.12.2019")

canton='ticino'
Ticino_canc=zefix_data(urlpage, canton='ticino', mutation='lo', from_data="01.10.2019", to_data="31.12.2019")

Ticino_trasf=zefix_data(urlpage, canton='ticino', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")

Ticino_fallim=zefix_data(urlpage, canton='ticino', mutation='k', from_data="01.10.2019", to_data="31.12.2019")


trans_into_tessin=pd.DataFrame()
for cant in list_cant:
    temp_data= zefix_data(urlpage, canton=cant, mutation='adress', from_data="01.10.2019", to_data="31.12.2019")
    try:
        temp_data['from_canton']=dic_canton[cant]
        print("canton {} appended".format(cant))
    except:
        print("canton {} search is empty".format(cant))
        continue
    trans_into_tessin=trans_into_tessin.append(temp_data)

Ticino_trasf_out= zefix_data(urlpage, canton='ticino', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")


Ticino_neu.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_aperture.csv', index=False, sep=';')
Ticino_canc.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_cancellazioni.csv', index=False, sep=';')
trans_into_tessin.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_trasf_in.csv', index=False, sep=';')
Ticino_fallim.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_fallim.csv', index=False, sep=';')
Ticino_trasf_out.to_csv(r'C:\Users\davide\Documents\lavoro\ticino_trasf_out.csv', index=False, sep=';')

for cant in list_cant:
    print("canton {} appended".format(cant))



temp_data= zefix_data(urlpage, canton='cant', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")

temp_data= zefix_data(urlpage, canton='Aargau', mutation='adress', from_data="01.10.2019", to_data="31.12.2019")
temp_data['from_canton']=dic_canton[list_cant[0]]
trans_into_tessin=data.append(temp_data)



list_canton=driver.find_element_by_id('ui-select-choices-0').text
list_mutation=driver.find_element_by_id('ui-select-choices-3').text

list_canton = list_canton.split('\n')
list_canton = [i[5:] for i in list_canton]

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

list_cant=['Aargau',
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
 'Uri',
 'Vaud',
 'Brig (Oberwallis)',
 'St-Maurice (Bas Valais)',
 'Sion (Valais Central)',
 'Zug',
 'Zürich']






list_mutation= list_mutation.split('\n')


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


##copy table

def get_table_zefix():
##download table from opened page and select rows
    bs_obj = BSoup(driver.page_source, 'html.parser')
    body= bs_obj.find('tbody')
    rows= body.find_all('tr')
#    #create empty variables
#    file_data = []
#    file_header = []
#    ##download header (column names)
#    file_header = []
#    th_row=rows[0].find_all('th')
#    i=0
#    while i!= len(th_row):
#        col_name = th_row[i].get_text().strip()
#        file_header.append(col_name)
#        i+=1
#    i=0
    ##download data
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









#select the second datapicker (date to)
data= "19.12.2018"
data.split('.')
def calendar_date(data, target):
    data_temp= data.split('.')
    driver.find_element_by_xpath(target).click()

/html/body/div[2]/div/div/div[1]/select
/html/body/div[3]/div/div/div[2]/select
driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/select')

m=driver.find_elements_by_class_name('pika-select-month')
m_option = m[0].find_elements_by_tag_name('option')
data_temp=[]
for m_elem in m_option:
    des = m_elem.text
#    link = result.find_element_by_tag_name('a')
    cod = m_elem.get_attribute("value")
    # append dict to array
    data_temp.append({"description" : des, "code": cod})
data_temp=pd.DataFrame(data_temp)



m=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/select')
m_option = m.find_elements_by_tag_name('option')
data_temp=[]
for m_elem in m_option:
    des = m_elem.text
#    link = result.find_element_by_tag_name('a')
    cod = m_elem.get_attribute("value")
    # append dict to array
    data_temp.append({"description" : des, "code": cod})
data_temp=pd.DataFrame(data_temp)







m=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/select')
m_option = m.find_elements_by_tag_name('option')
data_temp=[]
for m_elem in m_option:
    des = m_elem.text
#    link = result.find_element_by_tag_name('a')
    cod = m_elem.get_attribute("value")
    # append dict to array
    data_temp.append({"description" : des, "code": cod})
data_temp=pd.DataFrame(data_temp)









/html/body/div[2]/div/div/div[1]/select


<button class="pika-button pika-day" type="button" data-pika-year="2017" data-pika-month="2" data-pika-day="1">1</button>

    ab=driver.find_element_by_name(name)
    ab_option = ab.find_elements_by_tag_name('option')

<select class="pika-select pika-select-year" tabindex="-1"><option value="2016" selected="">2016</option><option value="2017">2017</option><option value="2018">2018</option><option value="2019">2019</option><option value="2020">2020</option></select>
/html/body/div[2]/div/div/div[2]/select

Select(driver.find_element_by_name('MERCE'))
    merce.select_by_value(product_code)


driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input').send_keys('74856' + Keys.ENTER)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input').clear()

driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input').click()



/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[2]/fieldset/div/input

send_keys('neu' + Keys.ENTER)



driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/div[1]/span').click()


driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/input[1]').send_keys('neu' + Keys.ENTER)

/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[8]/fieldset/div/input[1]









driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[5]/fieldset/div/input[1]').submit()

driver.find_elements_by_css_selector('html.js.flexbox.flexboxlegacy.canvas.canvastext.webgl.no-touch.geolocation.postmessage.no-websqldatabase.indexeddb.hashchange.history.draganddrop.websockets.rgba.hsla.multiplebgs.backgroundsize.borderimage.borderradius.boxshadow.textshadow.opacity.cssanimations.csscolumns.cssgradients.no-cssreflections.csstransforms.csstransforms3d.csstransitions.fontface.generatedcontent.video.audio.localstorage.sessionstorage.webworkers.applicationcache.svg.inlinesvg.smil.svgclippaths.ng-scope.Firefox-73 body div.zefix-app.ng-scope div#top.container-main.ng-scope.container.one-column-layout div.container-content.container div.ng-scope div.content-wrapper.ng-scope div#form-container.col-md-12 div.hidden-print.ng-scope form.ng-valid.ng-scope.advanced-search.ng-dirty.ng-valid-parse div.container div.row div.form-column.col-md-6.col-md-offset-3 div.form-field.ng-isolate-scope.col-xs-6 fieldset div.ui-select-container.ui-select-bootstrap.dropdown.ng-valid.ng-touched.ng-dirty.ng-valid-parse.ng-empty.open.direction-up input.form-control.ui-select-search.ng-valid.ng-touched.ng-dirty.ng-valid-parse.ng-not-empty')



/html/body/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div[12]/a/div[1]/span[2]


driver.find_element_by_link_text('IT').click()


driver.find_element_by_class_name("ng-binding").click()



driver.find_element_by_class_name("ng-binding")

    a = BSoup(driver.find_element_by_class_name("ng-binding"), 'html.parser')


/html/body/div[1]/div/header/div/div[1]/section/nav[2]/ul/li[3]/a
