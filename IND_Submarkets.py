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
    def __init__(self,SubmarketCode="",Inventory=0,Avg_Building_Size=0): 
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
        
def combine(c_submarket,targetsubmarket): 
    #combines two current submarkets into a new submarket 
    #all combines result in a new submarket 
    track_submarkets.loc[c_submarket.getcode(),'combine']=1
    track_submarkets.loc[targetsubmarket.getcode(),'combine']=1
    print c_submarket.getcode(), ", combine set to 1"
    print targetsubmarket.getcode(), ", combine set to 1"
    
    s1=track_submarkets.loc[c_submarket.getcode(),'new_submarket']
    s2=track_submarkets.loc[targetsubmarket.getcode(),'new_submarket']
    
    temp=Submarket(s1.getcode()+s2.getcode(),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)

    track_submarkets.loc[c_submarket.getcode(),'new_submarket']=temp
    track_submarkets.loc[targetsubmarket.getcode(),'new_submarket']=temp
    print "combinED", track_submarkets.loc[c_submarket.getcode(),'new_submarket'].getcode(), " with",targetsubmarket.getcode()



    
#HOME FILE PATHS 
neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
submarkets_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/SubmarketList.csv"

#WORK FILE PATHS
#neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
#submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)

#track submarkets keeps track of whether submarket has been combined and the "code" and Inventory of new submarket
#starts by reading in all codes 
track_submarkets=pandas.read_csv(submarkets_file, header=0, index_col=0)
track_submarkets['combine']=0
track_submarkets['new_submarket']=Submarket('Empty',0,0)
track_submarkets['Inventory']=0
#track_submarkets['combine_list']=[]
submarkets=set() 
previous_index=0

#convert raw data into submarkets  
for index, row in neighbors_raw.iterrows(): 
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<10000000 and float(row['nbr_Inventory'])<15000000:
        if index!=previous_index: 
            current_sub=Submarket(index,int(row['src_Inventory']), int(row['src_Avg_Buiding_Size']))
        current_sub.AddNeighbor(Submarket(row['nbr_LOGCode'],int(row['nbr_Inventory']), int(row['nbr_Avg_Buiding_Size'])))
        previous_index=index
        submarkets.add(current_sub)
        
#In the begining "new_submarket" is set to curretn submarket for everyone
for sub in submarkets:
    track_submarkets.loc[sub.getcode(),'new_submarket']=sub 
    for n in sub.Neighbors():
        track_submarkets.loc[n.getcode(),'new_submarket']=n
i=0
for submarket in submarkets:
    if i<10:
        print "In submarket", submarket.getcode(),"with inventory", submarket.getInventory()
        combine_flag=0
        curr_diff=10000000
        s_Inventory=submarket.getInventory()
        s_avg=submarket.getAvg_Building_Size() 
        for neighbor in submarket.Neighbors():
            print "examining neighbor",neighbor.getcode(),"with", neighbor.getInventory(),"inventory"
            print "with combine code of",track_submarkets.loc[neighbor.getcode(),'combine']
            n_Inventory=neighbor.getInventory()
            n_avg=submarket.getAvg_Building_Size()
            #1. always combine submarket with any neigbors that have no Inventory that have not already been combined 
            if n_Inventory==0 and track_submarkets.loc[neighbor.getcode(),'combine']==0:
                    combine(neighbor,submarket)
                    #2.Of all the neighbors, track all those combinations which lead to ~10M SF and combine with submarket that has closest AVG BLDG SIZE
            if track_submarkets.loc[neighbor.getcode(),'combine']==0:
                if track_submarkets.loc[submarket.getcode(),'new_submarket'].getInventory()+track_submarkets.loc[submarket.getcode(),'new_submarket'].getInventory()<=15000000 and abs(s_avg-n_avg)<curr_diff:
                    comb_neighbor=neighbor
                    combine_flag=1
        if combine_flag==1: 
            combine(comb_neighbor,submarket)
        i+=1
codes=lambda x: x.getcode()     
track_submarkets['new_codes']=track_submarkets['new_submarket'].map(codes)
track_submarkets['Inventory']=track_submarkets['new_submarket'].map(lambda x: x.getInventory())
track_submarkets.to_csv("output.csv")


#After initial combines, go throguh track submarkets and see which submarkets are still <10 M SF
#still_small=track_submarkets['Inventory']<10000000
#print still_small 
#for submarket in 
