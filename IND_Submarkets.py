# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

@author: cmelo
"""

from collections import defaultdict
import pandas 
import numpy as np 

#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#data_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSAsubmarketdata.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
data_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSAsubmarketdata.csv"

neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0,na_values=[""], dtype=str)
neighbors=defaultdict(list)
submarket_data=pandas.read_csv(data_file, header=0, index_col=0)
submarket_data['match']=0



neighbors_raw.replace([""], np.nan, inplace=True)
print neighbors_raw['nbr_Inventory']
neighbors_raw.dtypes 
neighbors_raw


for index, row in neighbors_raw.iterrows(): 
    print row['nbr_Inventory']

    if float(row['src_Inventory'])<10000000 & float(row['nbr_Inventory'])<20000000:
        neighbors[row['src_LOGCode']].append(row['nbr_LOGCode'])
"""
neighbors is a dictionary where key is submarket code and value is a list of the 
#the submarket codes of all the neighbors 
"""

for submarket in neighbors.keys():
    for neighbor in neighbors[submarket]:
        print neighbor
        try:
            print submarket_data.loc[neighbor]['N_prop']
        except:
            pass