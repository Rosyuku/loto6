# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 21:50:59 2017

@author: Wakasugi Kazuyuki
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

#from joblib import Parallel, delayed
#
#def getValue(target):
#
#    url = "http://sougaku.com/loto6/data/detail/index" + str(target) + ".html"
#    
#    session = requests.session()
#    res = session.get(url)
#    
#    soup = BeautifulSoup(res.text, "html.parser")
#    soup = soup.find(class_='sokuho_tb1')
#    value = int(soup.find_all('td')[2].text.replace('\n', '').replace('\t', '')[:-3].replace(',', ''))
#
#    return value    

if __name__ == "__main__":
    
    last = 1195
    result = pd.DataFrame(index=range(1, last+1), columns=['販売実績額'])

    for i in result.index:
        
        target = i
        
        if target == last:
            url = "http://sougaku.com/loto6/data/detail/"
        else:
            url = "http://sougaku.com/loto6/data/detail/index" + str(target) + ".html"
        
        session = requests.session()
        res = session.get(url)
        
        soup = BeautifulSoup(res.text, "html.parser")
        soup = soup.find(class_='sokuho_tb1')
        value = int(soup.find_all('td')[2].text.replace('\n', '').replace('\t', '')[:-3].replace(',', ''))
        print(i, value)
        
        result.ix[i, 0] = value
                 
        result.to_csv("販売実績額.csv", encoding="cp932")