# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

@author: cmelo
"""

from collections import defaultdict
import pandas 
import numpy as np 
import json

#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#data_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSAsubmarketdata.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
data_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSAsubmarketdata.csv"

neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)
neighbors=defaultdict(tuple)
neighbor_dict={}
templist=[]
previous_index=""

i=0

for index, row in neighbors_raw.iterrows(): 
    if index!=previous_index and previous_index!="": 
        templist=[]
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<10000000 and float(row['nbr_Inventory'])<15000000:
        print index,"this is what Index I'm on" 
        neighbor_dict.clear()
        neighbor_dict[row['nbr_LOGCode']]=(int(row['nbr_Inventory']), int(row['nbr_Avg_Buiding_Size']))
        print neighbor_dict," this is dict I just created as neighbordict"
        templist.append(neighbor_dict.copy())
        print templist
        neighbors[index]=(templist,row['src_Inventory'])
        previous_index=index
        
data_as_dict = json.loads(json.dumps(neighbors))
print(data_as_dict['LOG-LOSA-01'])
"""
neighbors is a dictionary where key is submarket code and value is a TUPLE where [0] is a list of all neighbors, where each neighbor is represented as 
a dictionary where key is the neighbor's submarket code and value is a tuple containing (nbr_Invesntory, nbr_Avg_BLDG_size) and [1] is src_inventory 

    








for submarket in neighbors.keys():
    for neighbor in neighbors[submarket]:
        print neighbor
        try:
            print submarket_data.loc[neighbor]['N_prop']
        except:
            pass
            """