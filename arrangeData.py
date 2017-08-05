#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 16:55:27 2017

@author: kazuyuki
"""

import pandas as pd

if __name__ == "__main__":
    
    df = pd.read_csv('loto6.csv', encoding="cp932")

    adf = pd.DataFrame(index=df.index, columns=range(1, 44), data=0)
    
    for i in range(len(df.index)):
        
        tdf = df.iloc[i, 3:10]
        
        for j in range(len(tdf.index)):
            
            adf.loc[df.index[i], tdf.iloc[j]] = j+1
            
            
    df['キャリーオーバー_今回'] = df['キャリーオーバー'].shift(1).fillna(0).astype(int)
    
    sdf = pd.read_csv("salesData.csv", usecols=['販売実績額'])
    
    df = pd.concat([df, sdf, adf], axis=1)
    
    df.to_csv("loto6_allData.csv")
