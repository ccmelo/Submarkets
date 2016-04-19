# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

@author: cmelo
"""

from collections import defaultdict
import pandas 
import numpy as np 
import json

class Submarket(object): 
    def __init__(self,SubmarketCode,Inventory,Avg_Building_Size): 
        self.Inventory=Inventory
        self.Avg_Building_Size=Avg_Building_Size
        self.code=SubmarketCode 
        self.neighbors=[]
    def Inventory(self):
        return self.Inventory
    def Avg_Building_Size(self):
        return self.Avg_Building_Size 
    def Code(self):
        return self.code 
    def AddNeighbor(self,submarket): 
        self.neighbors.append(submarket) 
    def PrintNeighbors(self):
        for neighbor in self.neighbors: 
            print '{0}: ({1},{2})'.format(neighbor.Code(), str(self.Inventory), str(self.Avg_Building_Size))
    def PrintSubmarket(self):
        print "Submarket,", submarket.Code()
        self.PrintNeighbors()
#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#data_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSAsubmarketdata.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)
#neighbors data structure initialized 

previous_index=""
#new submarkets keep track of whether submarket has been combined and the "code" of new submarket
new_submarkets=pandas.read_csv(submarkets_file, header=0, index_col=0)
new_submarkets['combine']=0
new_submarkets['new_code']=""
new_submarkets['Inventory']=0
submarkets=set() 
#print new_submarkets.head()
#converts raw data to more useful structure


    
for index, row in neighbors_raw.iterrows(): 
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<10000000 and float(row['nbr_Inventory'])<15000000:
        if index!=previous_index: 
            current_sub=Submarket(index,int(row['src_Inventory']), int(row['src_Avg_Buiding_Size']))
        sub=Submarket(row['nbr_LOGCode'],int(row['nbr_Inventory']), int(row['nbr_Avg_Buiding_Size']))
        current_sub.AddNeighbor(sub)
        previous_index=index
        submarkets.add(current_sub)

#test line 


    
    
    
for submarket in submarkets:
    submarket.PrintSubmarket()



        
#def combine(old_sub,new_sub): 
    #where old_sub and new_sub are submarket 
