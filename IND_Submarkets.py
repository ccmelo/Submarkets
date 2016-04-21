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
        self.orig_Inventory=Inventory
        self.orig_Avg_Building_Size=Avg_Building_Size
        self.originalcode=SubmarketCode 
        self.neighbors=[]
        self.combine_with=set()
        self.currentcode=SubmarketCode
        self.combine=0
        self.new_Inv=Inventory
        self.new_avg=Avg_Building_Size
    def getInventory(self):
        return self.orig_Inventory
    def getNewInventory(self):
        return self.new_Inv
    def getAvg_Building_Size(self):
        return self.orig_Avg_Building_Size 
    def getcode(self):
        return self.originalcode 
    def getcurrentcode(self):
        return self.getcurrentcode
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
    def getComboList(self):
        return self.combine_with
    def setNewCode(self,new_code):
        self.currentcode=new_code 
    def update(self,combined_with_list,newcode,new_inv,new_avg):
        self.currentcode=newcode
        self.combine=1
        self.new_Inv=new_inv 
        self.new_avg=new_avg
        self.combine_with=self.combine_with.union(combined_with_list)
    def combinestatus(self):
        return self.combine
        
    
    
def combine(s1,s2): 
    #combines two current submarkets into a new submarket 
    print s1.getcode(), ", combine set to 1"
    print s2.getcode(), ", combine set to 1"
    
    #s1 gets combined with everyone s2 is connected with b/c a)we add all elements in s2's combo list to s1 and b) we add their codes together 
    s1.update(s2.getComboList(),s1.getcode()+s2.getcode(),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)
    s2.update(s1.getComboList(),s1.getcode()+s2.getcode(),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)
    

    print "combinED", s1.getcode(), "with", s2.getcode()
    #now, we must update any submarkets they peviously combine with-> combo list of s1 is same as s2, so only need to iter through 1 list 
    if len(s1.getComboList())>0:
        for sub in s1.getComboList():
            sub.update(s1.getComboList(),s1.getcode()+s2.getcode(),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)

    
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
            print "with combine code of",neighbor.combinestatus() 
            n_avg=submarket.getAvg_Building_Size()
            #1. always combine submarket with any neigbors that have no Inventory that have not already been combined 
            if n_Inventory==0 and neighbor.combinestatus()==0:
                    combine(neighbor,submarket)
                    #2.Of all the neighbors, track all those combinations which lead to ~10M SF and combine with submarket that has closest AVG BLDG SIZE
            if neighbor.combinestatus==0:
                if submarket.getNewInventory()+submarket.getNewInventory()<=15000000 and abs(s_avg-n_avg)<curr_diff:
                    comb_neighbor=neighbor
                    combine_flag=1
        if combine_flag==1: 
            combine(comb_neighbor,submarket)
        i+=1
        
"""
codes=lambda x: x.getcode()     
track_submarkets['new_codes']=track_submarkets['new_submarket'].map(codes)
track_submarkets['Inventory']=track_submarkets['new_submarket'].map(lambda x: x.getInventory())
track_submarkets.to_csv("output.csv")


#After initial combines, go throguh track submarkets and see which submarkets are still <10 M SF
#still_small=track_submarkets['Inventory']<10000000
#print still_small 
#for submarket in 
"""