# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

@author: cmelo
"""

from collections import defaultdict
import pandas 
import numpy as np 
import json
import os 
import sys 

os.chdir('P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets') 

class Submarket(object): 
    def __init__(self,SubmarketCode="",Inventory=0,Avg_Building_Size=0): 
        self.orig_Inventory=Inventory
        self.orig_Avg_Building_Size=Avg_Building_Size
        self.originalcode=SubmarketCode 
        self.neighbors=[]
        self.combine_with=set([SubmarketCode])
        self.combine=0
        self.new_Inv=Inventory
        self.new_avg=Avg_Building_Size
    def getInventory(self):
        return self.orig_Inventory
    def getCurrentInventory(self):
        return self.new_Inv
    def getAvg_Building_Size(self):
        return self.orig_Avg_Building_Size 
    def getcode(self):
        return self.originalcode 
    def getcurrentcode(self):
        code=''
        for s in sorted(self.combine_with):
            code=code+s
        return code 
        return self.currentcode
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
    def update(self,combined_with_list,new_inv,new_avg):
        self.combine=1
        self.new_Inv=new_inv 
        self.new_avg=new_avg
        new_combine_list= self.combine_with.union(combined_with_list)
        self.combine_with=new_combine_list
    def combinestatus(self):
        return self.combine
    def printcombinelist(self):
        print self.combine_with

    
    
def combine(s1,s2): 
    #combines two current submarkets into a new submarket 
    
    print "combining", s1.getcode(), "with", s2.getcode()
    print s1.getcode(), "has the following in combine list", s1.printcombinelist()
    print s2.getcode(), "has the following in combine list", s2.printcombinelist()
    print s1.getcode(), ", combine set to 1"
    print s2.getcode(), ", combine set to 1"
    
    #s1 gets combined with everyone s2 is connected with b/c a)we add all elements in s2's combo list to s1 and b) we add their codes together 
    s1.update(set([s2.getcode()]).union(s2.getComboList()),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)
    s2.update(set([s1.getcode()]).union(s1.getComboList()),s1.getInventory()+s2.getInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)
    
   # print s1.getcode(), "NOW has the following in combine list", s1.printcombinelist(), "AND code of" s1.getcurrentcode()
   # print s2.getcode(), "NOW has the following in combine list", s2.printcombinelist(), "AND code of" s2.getcurrentcode()
    #now, we must update any submarkets they peviously combine with-> combo list of s1 is same as s2, so only need to iter through 1 list 
    if len(s1.getComboList())>2:
        for sub in s1.getComboList():
            print "updating", sub
            submarkets[sub].update(s1.getComboList(),s1.getCurrentInventory()+s2.getCurrentInventory(),(s1.getAvg_Building_Size()+s2.getAvg_Building_Size())/2)
            print "now has combine list of" , submarkets[sub].printcombinelist()
    
#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#submarkets_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/SubmarketList.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors.csv"
submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)


submarkets={}
previous_index=0

#convert raw data into submarkets  and store them in a DICTIONARY where key=submarketcode and value is submarket OBJECT
for index, row in neighbors_raw.iterrows(): 
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if float(row['src_Inventory'])<15000000 and float(row['nbr_Inventory'])<15000000:
        if index!=previous_index: 
            current_sub=Submarket(index,int(row['src_Inventory']), int(row['src_Avg_Buiding_Size']))
        current_sub.AddNeighbor(row['nbr_LOGCode'])
        previous_index=index
        submarkets[index]=current_sub 

for k,v in submarkets.iteritems(): 
    print k
    print v.Neighbors()

    
i=0
for submarket in submarkets.values():
    zero=0   
    if i<5:
        print "NEW SUBMARKET:In submarket", submarket.getcode(),"with inventory", submarket.getInventory()
        combine_flag=0
        curr_diff=10000000
        s_Inventory=submarket.getInventory()
        s_avg=submarket.getAvg_Building_Size() 
        for n in submarket.Neighbors():
            neighbor=submarkets[n]
            print "examining neighbor",neighbor.getcode(),"with", neighbor.getInventory(),"inventory"
            print "with combine code of",neighbor.combinestatus() 
            n_avg=neighbor.getAvg_Building_Size()
            #1. always combine submarket with any neigbors that have no Inventory that have not already been combined 
            if neighbor.getCurrentInventory()==0 and neighbor.combinestatus()==0 and zero<2:
                    print "calling combine from 0 if statement"
                    combine(neighbor,submarket)
                    zero+=1 
            #2.Of all the neighbors, track all those combinations which lead to ~10M SF and combine with submarket that has closest AVG BLDG SIZE
            if neighbor.combinestatus()==0:
                if submarket.getCurrentInventory()+neighbor.getCurrentInventory()<=15000000 and abs(s_avg-n_avg)<curr_diff:
                    print "combine flag set to 1"
                    comb_neighbor=neighbor
                    combine_flag=1
        if combine_flag==1: 
            combine(comb_neighbor,submarket)
    i+=1
        
#GET OUTPUT 
output=pandas.DataFrame.from_dict(submarkets, orient='index') 
output['final_code']='Unchanged'
output['final_inventory']=0 
for k,v in submarkets.iteritems(): 
   output.loc[k,'final_code']=v.getcurrentcode()
   output.loc[k,'final_inventory']=v.getCurrentInventory()
   
print zero
output.to_csv("output.csv") 
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