#!/usr/bin/env python
# coding: utf-8

# In[1]:


# general imports
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator


# In[3]:


"""
# Set the driver to Chrome
# In the bracket is the local path for chromedriver

detailed instruction on chromedriver @https://chromedriver.chromium.org/getting-started
"""

driver = webdriver.Chrome("E:\chromedriver\chromedriver")

# datasource DingXiangYuan
driver.get("http://ncov.dxy.cn/")


# In[4]:


"""
# To scrape the data, we need first understand the source-code

# We want to have the data for all the province in China
as well as the data for all the countries in the world

# In the source-code, there are two areaboxes of data while
they share the same class code

# So we need to seperate them apart first

detailed instruction on BeautifulSoup@https://www.crummy.com/software/BeautifulSoup/bs4/doc/#
"""

# set up the content to scrape
content = driver.page_source
soup = BeautifulSoup(content)

# redefined the condition to find the exact match of certain class code
chinaArea = soup.find(lambda tag: tag.name == 'div' and tag.get("class")==["areaBox___3jZkr"])
# find the next element that satisfy above condition
# div is the type of the tag in source-code
globalArea = chinaArea.find_next_sibling('div')


# In[7]:


"""start to scrape data"""
""" For all the Procinves in China"""

# initialize the list to store the data
province = []
chinaDiagnosed = []
chinaDeaths = []
chinaHealed = []

# This is for translating the Chinese characters to English
translator = Translator()

# redefined the condition to find the exact match of certain class code
for location in chinaArea.find_all(lambda tag: tag.name == 'div' and tag.get("class")==["areaBlock1___3V3UU"]):
    name = location.find('p',attrs={"class":"subBlock1___j0DGa"})
    diagnose = location.find('p',attrs={"class":"subBlock4___ANk6l"})
    death = location.find('p',attrs={"class":"subBlock3___3mcDz"})
    heal = location.find('p',attrs={"class":"subBlock5___2EkOU"})
    # translate the name
    name = translator.translate(name.text,src='zh-cn')
    # Since in Chinese, Province Shanxi and Shaanxi have similar pronouciation
    # When translating into English, Google will translate Shaanxi into 'Shanxi Province'
    # Below is to manually avoid such situation
    if name.text == 'Shanxi Province':
        name = 'Shaanxi'
    else:
        name = name.text.replace(' Province', '')
    # store the results to list
    province.append(name)
    chinaDiagnosed.append(diagnose.text)
    chinaDeaths.append(death.text)
    chinaHealed.append(heal.text)
    
"""Store the result in Dataframe and export to a csv file"""
china_df = pd.DataFrame({'Province':province, 'Diagnosed':chinaDiagnosed, 'Death':chinaDeaths, 'Healed':chinaHealed})
china_df.to_csv('Coronavirus_China.csv', index=False)


# In[8]:


china_df


# In[9]:


"""For all the Countries in the World"""
"""
Notice: 
the data of other affected countries are hidden in the source code
Hence, at the current stage, I will mannually add to the csv file
until I find better solutions (or they fixed the website)
"""
country = []
globalDiagnosed = []
globalDeaths = []
globalHealed = []

# redefined the condition to find the exact match of certain class code
for location in globalArea.find_all(lambda tag: tag.name == 'div' and tag.get("class")==["areaBlock2___27vn7"]):
    name = location.find('p',attrs={"class":"subBlock1___j0DGa"})
    diagnose = location.find('p',attrs={"class":"subBlock4___ANk6l"})
    death = location.find('p',attrs={"class":"subBlock3___3mcDz"})
    heal = location.find('p',attrs={"class":"subBlock5___2EkOU"})
    # translate the name
    name = translator.translate(name.text,src='zh-cn')
    # store the results to list
    country.append(name.text)
    globalDiagnosed.append(diagnose.text)
    globalDeaths.append(death.text)
    globalHealed.append(heal.text)
    
"""Store the result in Dataframe and export to a csv file"""
global_df = pd.DataFrame({'Country':country, 'Diagnosed':globalDiagnosed, 'Death':globalDeaths, 'Healed':globalHealed})
global_df.to_csv('Coronavirus_global.csv', index=False)


# In[10]:


global_df


# In[11]:


"""
Since the above way isn't working
I scrape the global data @ www.worldometers.info
"""
driver = webdriver.Chrome("E:\chromedriver\chromedriver")

# get global data
driver.get("https://www.worldometers.info/coronavirus/")

# set up the content to scrape
content = driver.page_source
soup = BeautifulSoup(content)


# In[12]:


"""For all the Countries in the World"""
"""
Since the data is stored as a table
We will scrape the table and edit it later
"""

globalData = []
table = soup.find('table', attrs={'id':'table3'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    globalData.append([ele for ele in cols]) 


"""Store the result in Dataframe and export to a csv file"""
global_df = pd.DataFrame(globalData)

# Drop unnecessary columns and rename the columns
global_df = global_df.drop([2,4,6,7], axis=1)
global_df.columns = ['Country','Diagnosed','Death','Healed']
# Export to csv
global_df.to_csv('Coronavirus_global.csv', index=False)


# In[13]:


global_df

