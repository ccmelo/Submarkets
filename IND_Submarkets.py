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
    def getInventory(self):
        return self.Inventory
    def getAvg_Building_Size(self):
        return self.Avg_Building_Size 
    def getcode(self):
        return self.code 
    def AddNeighbor(self,submarket): 
        self.neighbors.append(submarket) 
    def PrintNeighbors(self):
        for neighbor in self.neighbors: 
            print '{0}: ({1},{2})'.format(neighbor.getcode(), str(self.Inventory), str(self.Avg_Building_Size))
    def PrintSubmarket(self):
        print "Submarket,", self.code
        self.PrintNeighbors()
    def Neighbors(self):
        return self.neighbors
        
def combine(submarket,targetsubmarket): 
    #combines two current submarkets into a new submarket 
    #all combines result in a new submarket 
    return Submarket(submarket.getcode()+targetsubmarket.getcode(),submarket.getInventory()+targetsubmarket.getInventory(),(submarket.getAvg_Building_Size()+targetsubmarket.getAvg_Building_Size())/2)

    
#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#data_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSAsubmarketdata.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)

#track submarkets keeps track of whether submarket has been combined and the "code" and Inventory of new submarket
#starts by reading in all codes 
track_submarkets=pandas.read_csv(submarkets_file, header=0, index_col=0)
track_submarkets['combine']=0
track_submarkets['new_submarket']=Submarket('Empty',0,0)
track_submarkets['Inventory']=0
submarkets=set() 
previous_index=0

#converts raw data to more useful structure


    
for index, row in neighbors_raw.iterrows(): 
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<10000000 and float(row['nbr_Inventory'])<15000000:
        if index!=previous_index: 
            current_sub=Submarket(index,int(row['src_Inventory']), int(row['src_Avg_Buiding_Size']))
        current_sub.AddNeighbor(Submarket(row['nbr_LOGCode'],int(row['nbr_Inventory']), int(row['nbr_Avg_Buiding_Size'])))
        previous_index=index
        submarkets.add(current_sub)

 
for submarket in submarkets:
    track_submarkets.loc[submarket.getcode(),'new_submarket']=submarket 
    combine_flag=0
    curr_diff=10000000
    s_Inventory=submarket.getInventory()
    s_avg=submarket.getAvg_Building_Size() 
    for neighbor in submarket.Neighbors():
        track_submarkets.loc[neighbor.getcode(),'new_submarket']=neighbor
        n_Inventory=neighbor.getInventory()
        n_avg=submarket.getAvg_Building_Size()
        #1. always combine submarket with any neigbors that have no Inventory that have not already been combined 
        if n_Inventory==0 and track_submarkets.loc[neighbor.getcode(),'combine']==0:
            # if its our first combination for this submarket, combine submarket and neighbor
            if track_submarkets.loc[submarket.getcode(),'combine']==0:
                track_submarkets.loc[submarket.getcode(),'combine']=1
                track_submarkets.loc[neighbor.getcode(),'combine']=1
                temp=combine(neighbor,track_submarkets.loc[submarket.getcode(),'new_submarket'])
                track_submarkets.loc[submarket.getcode(),'new_submarket']=temp
                track_submarkets.loc[neighbor.getcode(),'new_submarket']=temp
            #else, add neighbor to current cluster 
            else: 
                temp=combine(neighbor,track_submarkets.loc[submarket.getcode(),'new_submarket'])
                track_submarkets.loc[submarket.getcode(),'new_submarket']=temp
                track_submarkets.loc[neighbor.getcode(),'new_submarket']=temp
        #2.Of all the neighbors, track all those combinations which lead to ~10M SF and combine with submarket that has closest AVG BLDG SIZE
        if track_submarkets.loc[neighbor.getcode(),'combine']==0:
            if track_submarkets.loc[submarket.getcode(),'new_submarket'].getInventory()+s_Inventory<=15000000 and abs(s_avg-n_avg)<curr_diff:
                comb_neighbor=neighbor
                combine_flag=1
    if combine_flag==1: 
        temp=combine(comb_neighbor,track_submarkets.loc[submarket.getcode(),'new_submarket'])
        track_submarkets.loc[submarket.getcode(),'new_submarket']=temp
        track_submarkets.loc[comb_neighbor.getcode(),'new_submarket']=temp
            
codes=lambda x: x.getcode()     
print track_submarkets['new_submarket']  
track_submarkets['new_codes']=track_submarkets['new_submarket'].map(codes)
track_submarkets['Inventory']=track_submarkets['new_submarket'].map(lambda x: x.getInventory())
print track_submarkets

#for submarket in submarkets:
    #submarket.PrintSubmarket()