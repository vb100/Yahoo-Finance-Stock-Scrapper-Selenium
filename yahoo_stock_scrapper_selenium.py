# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 23:03:49 2018

@author: Vytautas
Downloader of RAW data : stage 01
"""

# ----------------------------------------------------------------------------
# Import main libraries and modules
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import numpy as np
import pandas as pd
from io import StringIO

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver

#------------------------------------------------------------------------------

#::::::::::::::::::::::::::::::::::::::::::::
def generateURLs(df):
    base_url = "https://finance.yahoo.com/quote/"
    
    l = []
    if len(df) > 0:
        for element in range(0, len(df), 1):
            l.append(base_url + str(df.iat[element, 0]) + "/history?p=" + str(df.iat[element, 0]))
        print("We have ", str(len(l)) , "elements as RAW data.") 
    return l
#::::::::::::::::::::::::::::::::::::::::::::            
    
qDF = pd.read_csv("ETFList.csv", header = None)
ql = generateURLs(qDF)

# Setting for Chrome Virtual User
options = webdriver.chrome.options.Options()
chromeOptions = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
   
chrome_path = r"C:\Users\Vytautas.Bielinskas\Desktop\Python\JSscrapping\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

#------------------------------------------------------------------------------
# Now it is the time to be ready for go through the pages!

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import unittest, time, re

# Define data structure
datastore = []                           # Records will be storage in a datastore

delay = 3 # seconds

def goThroughPages(ql):
    for query in range(0, len(ql), 1):
        
        try:   
            driver.implicitly_wait(9)
            my_url = ql[query]
            driver.get(my_url) 
            time.sleep(8)
            
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="render-target-default"]')))
            print("Page is ready!")
        
            print("Analyzing URL (", query, "):", my_url)
            
            record = {}                          # Each value will be saved to record as dictionary
            
            # Press Calendar:
            calendar_btn = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
            calendar_btn.click()
            time.sleep(10)
            print("Stop 01")
            
            # Set Max limit on Calendar
            max_btn = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[8]/span')
            max_btn.click()
            time.sleep(10)
            print("Stop 02: Set Max limit")
            
            # Click Done button
            done_btn = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]/span')
            done_btn.click()
            print("Stop 03: Click Done button")
            
            # Click Apply!
            apply_btn = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
            time.sleep(5)
            #apply_btn = driver.find_element_by_css_selector("#Col1-1-HistoricalDataTable-Proxy > section > div.Mt\28 15px\29.drop-down-selector.historical > div.Bgc\28 \23 f8f8f8\29.Bdrs\28 3px\29.P\28 10px\29 > button")
            apply_btn.click()
            time.sleep(6)
            print("Stop 04: Click Apply button")
        
            # Replace current URL
            current_url = driver.current_url
            month_url = current_url.replace("1d", "1mo")
            driver.get(month_url) 
            time.sleep(10)
            print("Stop 05: Change URL to month report")
            
            # Click Download
            download_btn = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
            time.sleep(8)
            download_btn.click()
            time.sleep(6)
            print("Stop 06: Click Download")
            
        except TimeoutException:
            print("Loading took too much time!")
            
        
        datastore.append(record)
    return(datastore)
#------------------------------------------------------------------------------
    
df = pd.DataFrame(goThroughPages(ql))
#df.to_csv()