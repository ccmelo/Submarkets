# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

@author: cmelo
"""
from collections import defaultdict
import pandas 
neighbors_raw=pandas.read_csv("/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv", header=0, index_col=0)
neighbors=defaultdict(list)
submarket_data=pandas.read_csv("/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSAsubmarketdata.csv", header=0, index_col=0)
for index, row in neighbors_raw.iterrows(): 
    neighbors[row['src_LOGCode']].append(row['nbr_LOGCode'])
#neighbors is a dictionary where key is submarket code and value is a list of the 
#the submarket codes of all the neighbors 
for k in neighbors.keys():
    print k