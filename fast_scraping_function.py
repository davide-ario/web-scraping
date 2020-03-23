#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:53:50 2020

@author: davide
"""

from bs4 import BeautifulSoup as BSoup

driver = webdriver.Firefox()
# get web page
driver.get(urlpage)
# execute script to scroll down the page
#  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(1)

driver.find_element_by_css_selector("input[type='radio'][value='C']").click()
driver.find_element_by_name('B2').click()


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









def get_data3(product_code, year, country_code, quarter,  link, cumulated):
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
    #
#    time.sleep(1+random.randint(1,7))
   
    # copy table
  

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
 
#    time.sleep(5+random.randint(1,10))
    return(df)

















        
    
    file_row=[]
    for data in datas:
        data_text= data.get_text()
        file_row.append(data_text)
    file_data.append()
    
    
    
file_header = rows[0].find_all('th')
cells=ro
 [header.text for header in head_line.find_elements_by_tag_name('th')]

    file_data.append(",".join(file_header))
    body_rows = table.find_elements_by_tag_name('tr')
    for row in body_rows:
        data = row.find_elements_by_tag_name('td')
        file_row = []
        for datum in data:
            datum_text = datum.text
            file_row.append(datum_text)
        file_data.append(",".join(file_row))    #table is now copied in file_data; fields are separated by ,
