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
submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)
#neighbors data structure initialized 
neighbors=defaultdict(tuple)
previous_index=""
#new submarkets keep track of whether submarket has been combined and the "code" of new submarket
new_submarkets=pandas.read_csv(submarkets_file, header=0, index_col=0)
new_submarkets['combine']=0
new_submarkets['new_code']=""
new_submarkets['Inventory']=0
#print new_submarkets.head()
#converts raw data to more useful structure
"""
neighbors is a dictionary where key is submarket code and value is a TUPLE where [0] is a list of all neighbors, (where each neighbor is represented as 
a TUPLE [0] is the neighbor's submarket code [1] is nbr_Invesntory and [2] is nbr_Avg_BLDG_size); and [1] is src_inventory 
"""
    
for index, row in neighbors_raw.iterrows(): 
    if index!=previous_index: 
        templist=[]
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<10000000 and float(row['nbr_Inventory'])<15000000:
        neighbor_tuple=()
        neighbor_tuple=(row['nbr_LOGCode'],int(row['nbr_Inventory']), int(row['nbr_Avg_Buiding_Size']))
        #append a COPY of just created dict, not the actual dictionary 
        templist.append(neighbor_tuple)
        neighbors[index]=(templist,int(row['src_Inventory']))
        previous_index=index

#below line converts dictionary to json and back to dict, for priting help, but I don't think I need this    
#data_as_dict = json.loads(json.dumps(neighbors))

#test line 
print neighbors['LOG-LOSA-13']

#iterate through all neighbors in all submarkets 
for submarket in neighbors.keys():
    for neighbor in neighbors[submarket][0]:
        #test line: if submarket=='LOG-LOSA-01':
            #print n_tuple, '\n'
        #First try to combine with any neigbors that have no Inventory that have not already been combined 
        if neighbor[1]==0 and new_submarkets[neighbor[0]]['combine']==0:
            combine() 
            
def combine(old_sub,new_sub): 
    #where old_sub and new_sub are submarket 
